# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.consumer_control_code.ConsumerControlCode`
========================================================

* Author(s): Dan Halbert
"""


class ConsumerControlCode:
    """USB HID Consumer Control Device constants.

    This list includes a few common consumer control codes from
    https://www.usb.org/sites/default/files/hut1_21_0.pdf#page=118.
    """

    # pylint: disable-msg=too-few-public-methods

    RECORD = 0xB2
    """Record"""
    FAST_FORWARD = 0xB3
    """Fast Forward"""
    REWIND = 0xB4
    """Rewind"""
    SCAN_NEXT_TRACK = 0xB5
    """Skip to next track"""
    SCAN_PREVIOUS_TRACK = 0xB6
    """Go back to previous track"""
    STOP = 0xB7
    """Stop"""
    EJECT = 0xB8
    """Eject"""
    PLAY_PAUSE = 0xCD
    """Play/Pause toggle"""
    MUTE = 0xE2
    """Mute"""
    VOLUME_DECREMENT = 0xEA
    """Decrease volume"""
    VOLUME_INCREMENT = 0xE9
    """Increase volume"""
    BRIGHTNESS_DECREMENT = 0x70
    """Decrease Brightness"""
    BRIGHTNESS_INCREMENT = 0x6F
    """Increase Brightness"""

    INVOKE_CAPTURE_INTERFACE = 0xD0
    START_OR_STOP_GAME_RECORDING = 0xD1
    HISTORICAL_GAME_CAPTURE = 0xD2
    CAPTURE_GAME_SCREENSHOT = 0xD3
    SHOW_OR_HIDE_RECORDING_INDICATOR = 0xD4
    START_OR_STOP_MICROPHONE_CAPTURE = 0xD5
    START_OR_STOP_CAMERA_CAPTURE = 0xD6
    START_OR_STOP_GAME_BROADCAST = 0xD7