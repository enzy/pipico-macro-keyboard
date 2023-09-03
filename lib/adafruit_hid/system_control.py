import sys

if sys.implementation.version[0] < 3:
    raise ImportError(
        "{0} is not supported in CircuitPython 2.x or lower".format(__name__)
    )

# pylint: disable=wrong-import-position
import struct
import time
from . import find_device

try:
    from typing import Sequence
    import usb_hid
except ImportError:
    pass

class SystemControl:

    def __init__(self, devices: Sequence[usb_hid.Device]) -> None:
        # Generic Desktop Page (0x01)
        # 80 System Control
        self._device = find_device(devices, usage_page=0x01, usage=0x80)

        # Reuse this bytearray to send consumer reports.
        self._report = bytearray(1)

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.send(0x0)
        except OSError:
            time.sleep(1)
            self.send(0x0)

    def send(self, code: int) -> None:
        self.press(code)
        self.release()

    def press(self, code: int) -> None:
        self._report[0] = code
        self._device.send_report(self._report)

    def release(self) -> None:
        self._report[0] = 0x0
        self._device.send_report(self._report)
