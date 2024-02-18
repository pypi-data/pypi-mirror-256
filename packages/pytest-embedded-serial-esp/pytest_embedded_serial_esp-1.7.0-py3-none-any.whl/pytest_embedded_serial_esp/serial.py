import contextlib
import functools
import logging
import subprocess
from typing import Optional

import esptool
from esptool import CHIP_DEFS, FatalError
from esptool import __version__ as ESPTOOL_VERSION
from esptool import detect_chip
from esptool.targets import CHIP_LIST as ESPTOOL_CHIPS
from pexpect import TIMEOUT
from pytest_embedded.log import MessageQueue, PexpectProcess, live_print_call
from pytest_embedded.utils import Meta
from pytest_embedded_serial.dut import Serial


def _is_port_mac_verified(pexpect_proc: PexpectProcess, port: str, port_mac: str, msg_queue) -> bool:
    try:
        live_print_call(['esptool.py', '--port', port, 'read_mac'], msg_queue=msg_queue)
    except subprocess.CalledProcessError:
        return False
    else:
        try:
            pexpect_proc.expect(f'MAC: {port_mac.lower()}', timeout=0.1)
        except TIMEOUT:
            return False
        else:
            return True


class EsptoolArgs(object):
    """
    fake args object, this is a hack until esptool Python API is improved
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class EspSerial(Serial):
    """
    Serial class for ports connected to espressif products
    """

    ESPTOOL_DEFAULT_BAUDRATE = 921600

    def __init__(
        self,
        pexpect_proc: PexpectProcess,
        msg_queue: MessageQueue,
        target: Optional[str] = None,
        beta_target: Optional[str] = None,
        port: Optional[str] = None,
        port_mac: str = None,
        baud: int = Serial.DEFAULT_BAUDRATE,
        esptool_baud: int = ESPTOOL_DEFAULT_BAUDRATE,
        skip_autoflash: bool = False,
        erase_all: bool = False,
        meta: Optional[Meta] = None,
        **kwargs,
    ) -> None:
        self._meta = meta

        esptool_target = beta_target or target or 'auto'
        if port is None:
            available_ports = esptool.get_port_list()
            ports = list(set(available_ports) - set(self.occupied_ports.keys()))

            # sort to make /dev/ttyS* ports before /dev/ttyUSB* ports
            # esptool will reverse the list
            ports.sort()
            if port_mac:
                for port in ports:
                    if _is_port_mac_verified(pexpect_proc, port, port_mac, msg_queue):
                        ports = [port]
                        break
                else:
                    raise ValueError(f'The specified MAC address {port_mac} cannot be found.')

            # prioritize the cache recorded target port
            if esptool_target and self._meta:
                ports.sort(key=lambda x: self._meta.hit_port_target_cache(x, esptool_target))

            logging.debug(f'Detecting ports from {", ".join(ports)}')
        else:
            if port_mac:
                if _is_port_mac_verified(pexpect_proc, port, port_mac, msg_queue):
                    ports = [port]
                else:
                    raise ValueError(f'The specified MAC address {port_mac} binds with different port, not with {port}')
            else:
                ports = [port]

        # normal loader
        if esptool_target not in (['auto'] + ESPTOOL_CHIPS):
            raise ValueError(
                f'esptool version {ESPTOOL_VERSION} not support target {esptool_target}\n'
                f'Supported targets: {ESPTOOL_CHIPS}'
            )

        with contextlib.redirect_stdout(msg_queue):
            # Temp workaround for esptool
            # on windows have to close the unused scanned ports manually
            #
            # could revert to the following code blocks after fixing it
            #
            # esp: esptool.ESPLoader = esptool.get_default_connected_device(
            #     ports,
            #     port=port,
            #     connect_attempts=3,
            #     initial_baud=baud,
            #     chip=esptool_target,
            # )
            _esp = None
            for each_port in reversed(ports):
                print(f'Serial port {each_port}')
                try:
                    if esptool_target == 'auto':
                        _esp = detect_chip(each_port, baud, connect_attempts=3)
                    else:
                        chip_class = CHIP_DEFS[esptool_target]
                        _esp = chip_class(each_port, baud)
                        _esp.connect(attempts=3)
                    break
                except (FatalError, OSError) as err:
                    if port is not None:
                        raise
                    print(f'{each_port} failed to connect: {err}')
                    if _esp:
                        # ensure unused port is closed.
                        _esp._port.close()
                    _esp = None
            esp = _esp

        if not esp:
            raise ValueError('Couldn\'t auto detect chip. Please manually specify with "--port"')

        self.esp: esptool.ESPLoader = None  # type: ignore
        self.stub: esptool.ESPLoader = None  # type: ignore

        target = esp.CHIP_NAME.lower().replace('-', '')
        logging.info('Target: %s, Port: %s', target, esp.serial_port)

        self.target = target

        self.skip_autoflash = skip_autoflash
        self.erase_all = erase_all
        self.esptool_baud = esptool_baud

        super().__init__(msg_queue=msg_queue, port=esp._port, baud=baud, meta=meta, **kwargs)

    def _post_init(self):
        if self._meta:
            self._meta.set_port_target_cache(self.port, self.target)

        if self.erase_all:
            self.erase_flash()

        super()._post_init()

    def use_esptool(hard_reset_after: bool = True, no_stub: bool = False):
        """
        1. tell the redirect serial thread to stop reading from the `pyserial` instance
        2. esptool reuse the `pyserial` instance and call `run_stub()`
        3. call to the decorated function, could use `self.stub` inside the function as the stubbed loader
        4. call `hard_reset()`, if `hard_reset_after` is True
        5. tell the redirect serial thread to continue reading from serial

        Args:
            hard_reset_after: run hard reset after
            no_stub: disable launching the flasher stub
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                with self.disable_redirect_thread():
                    with contextlib.redirect_stdout(self._q):
                        settings = self.proc.get_settings()
                        try:
                            self.esp = esptool.detect_chip(self.proc, self.baud)
                            self.esp.connect('hard_reset')

                            if not no_stub:
                                self.stub = self.esp.run_stub()

                            ret = func(self, *args, **kwargs)
                        finally:
                            if hard_reset_after:
                                self.esp.hard_reset()

                            self.proc.apply_settings(settings)

                return ret

            return wrapper

        return decorator

    def _start(self):
        self.hard_reset()

    @use_esptool(hard_reset_after=True, no_stub=True)
    def hard_reset(self):
        """Hard reset your espressif device"""
        pass

    @use_esptool()
    def erase_flash(self):
        """Erase the complete flash"""
        logging.info('Erasing the flash')
        self.stub.erase_flash()

        if self._meta:
            self._meta.drop_port_app_cache(self.port)
