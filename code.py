# SPDX-FileCopyrightText: 2021 Sandy Macdonald

# Modified by Frank Smith 2021 all the keys bar the modifier key
# can now be used as layer select and input keys
# prints debug messages via debug serial port (USB)
# sudo cat /dev/ttyACM0

# SPDX-License-Identifier: MIT

# An advanced example of how to set up a HID keyboard.

# There are four layers defined out of fifteen possible,
# selected by pressing and holding key 0 (bottom left),
# then tapping one of the coloured layer selector keys to switch layer.

# The defined layer colours are as follows:

#  * layer 1: pink: numpad-style keys, 0-9, delete, and enter.
#  * layer 2: blue: sends strings on each key press
#  * layer 3: yellow: media controls, rev, play/pause, fwd on row one, vol. down, mute,
#             vol. up on row two
#  * layer 4: white: sends mixxx controls

# NOTES:
# https://www.usb.org/sites/default/files/hutrr110-systemmicrophonemute.pdf

import board
import digitalio
import time
import usb_hid

from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware # for Pico RGB Keypad Base

import keyboard_layout_win_cz1
from keycode_win_cz1 import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.system_control import SystemControl
from adafruit_hid.system_control_code import SystemControlCode

systemLed = digitalio.DigitalInOut(board.LED)
systemLed.direction = digitalio.Direction.OUTPUT

# Set up Keybow
keybow = PMK(Hardware())
keys = keybow.keys

keybow.led_sleep_enabled = True
keybow.led_sleep_time = 5

keyboard = Keyboard(usb_hid.devices)
layout = keyboard_layout_win_cz1.KeyboardLayout(keyboard)

consumer_control = ConsumerControl(usb_hid.devices)
system_control = SystemControl(usb_hid.devices)

# Our layers. The key of item in the layer dictionary is the key number on
# Keybow to map to, and the value is the key press to send.

# Note that key 0 is reserved as the modifier

# purple - numeric keypad
layer_1 = {
    4: (Keycode.ZERO,),
    5: (Keycode.ONE,),
    6: (Keycode.FOUR,),
    7: (Keycode.SEVEN,),
    8: (Keycode.DELETE,),
    9: (Keycode.TWO,),
    10: (Keycode.FIVE,),
    11: (Keycode.EIGHT,),
    12: (Keycode.ENTER,),
    13: (Keycode.THREE,),
    14: (Keycode.SIX,),
    15: (Keycode.NINE,)
}

# blue - words
layer_2 = {
    7: "pack ",
    11: "my ",
    15: "box ",
    6: "with ",
    10: "five ",
    14: "dozen ",
    5: "liquor ",
    9: "jugs "
}

# yellow - media controls
layer_3 = {
    3: ConsumerControlCode.RECORD, # 0xA9, # System Microphone Mute, under Keyboard HID
    6: ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    9: ConsumerControlCode.VOLUME_DECREMENT,
    8: ConsumerControlCode.MUTE,
    10: ConsumerControlCode.PLAY_PAUSE,
    11: ConsumerControlCode.VOLUME_INCREMENT,
    14: ConsumerControlCode.SCAN_NEXT_TRACK
}

# white - mixxx
layer_4 = {
    2: (Keycode.CONTROL, Keycode.SHIFT, Keycode.M),
    5: (Keycode.D,),
    7: (Keycode.T,),
    8: (Keycode.SPACE,),
    13: (Keycode.L,),
    15: (Keycode.Y,)
}

# red - system control
layer_5 = {
    3: SystemControlCode.SYSTEM_MICROPHONE_MUTE,
    4: SystemControlCode.SYSTEM_MAIN_MENU,
    5: SystemControlCode.SYSTEM_APP_MENU,
    6: SystemControlCode.SYSTEM_DISMISS_NOTIFICATION,
    7: SystemControlCode.SYSTEM_DO_NOT_DISTURB,
    8: SystemControlCode.SYSTEM_SETUP,
    9: SystemControlCode.SYSTEM_SPEAKER_MUTE
}

layers = {
    1: layer_1,
    2: layer_2,
    3: layer_3,
    4: layer_4,
    5: layer_5
}

selectors = {
    1: keys[1],
    2: keys[2],
    3: keys[3],
    4: keys[4],
    5: keys[5],
}

# Define the modifier key and layer selector keys
modifier = keys[0]

# Start on layer 1
current_layer = 4

# The colours for each layer
colours = {
    1: (255, 0, 255),
    2: (0, 255, 255),
    3: (255, 255, 0),
    4: (128, 128, 128),
    5: (255, 0, 0)
}

layer_keys = range(0, 16)

# dictionary of sets (sets cannot be changed but can be replaced)
LEDs = {0: (64, 0, 0),
        1: (128, 0, 0),
        2: (196, 0, 0),
        3: (255, 0, 0),
        4: (0, 4, 0),
        5: (0, 128, 0),
        6: (0, 12, 0),
        7: (0, 196, 0),
        8: (0, 0, 64),
        9: (0, 0, 128),
        10: (0, 0, 196),
        11: (0, 0, 255),
        12: (64, 64, 0),
        13: (128, 128, 0),
        14: (196, 196, 0),
        15: (255, 255, 0)}

# Set the LEDs for each key in the current layer
for k in layers[current_layer].keys():
    keys[k].set_led(*colours[current_layer])

print("Starting!")
mode = 0
count = 0

# To prevent the strings (as opposed to single key presses) that are sent from
# refiring on a single key press, the debounce time for the strings has to be
# longer.

short_debounce = 0.03
long_debounce = 0.15
debounce = 0.03
fired = False

while True:
    # Always remember to call keybow.update()
    keybow.update()

    # if no key is pressed ensure not locked in layer change mode
    if ((mode == 2) & keybow.none_pressed()):
        mode = 0

    if modifier.held:
        # set to looking to change the keypad layer
        for layer in layers.keys():
            # If the modifier key is held, light up the layer selector keys
            if mode == 1:
                print("Looking for layer select")
                # Set the LEDs for each key in selectors
                for k in layer_keys:
                    keys[k].set_led(0, 0, 0)
                for k in selectors.keys():
                    keys[k].set_led(*colours[k])
                keys[0].set_led(0, 255, 0)
                mode = 2

            # Change current layer if layer key is pressed
            if selectors[layer].pressed:
                if mode >= 1:
                    mode = 0
                    current_layer = layer
                    print("Layer Changed:", current_layer)
                    # Set the LEDs for each key in the current layer
                    for k in layer_keys:
                        keys[k].set_led(0, 0, 0)
                    for k in layers[current_layer].keys():
                        keys[k].set_led(*colours[current_layer])
    else:
        # set to look for a key presses
        if mode == 0:
            print("Looking for key press on layer:", current_layer)
            mode = 1

            # Set the LEDs for each key in the current layer
            for k in layer_keys:
                keys[k].set_led(0, 0, 0)
            for k in layers[current_layer].keys():
                keys[k].set_led(*colours[current_layer])

    # Loop through all of the keys in the layer and if they're pressed, get the
    # key code from the layer's key map
    for k in layers[current_layer].keys():
        if keys[k].pressed:
            key_press = layers[current_layer][k]
            keys[k].set_led(*colours[current_layer])

            # If the key hasn't just fired (prevents refiring)
            if not fired:
                fired = True
                systemLed.value = True


                # Send the right sort of key press and set debounce for each
                # layer accordingly (layer 2 needs a long debounce)
                if current_layer == 1 or current_layer == 4:
                    debounce = short_debounce
                    keyboard.send(*key_press)
                elif current_layer == 2:
                    debounce = long_debounce
                    layout.write(key_press)
                elif current_layer == 3:
                    debounce = short_debounce
                    consumer_control.send(key_press)
                elif current_layer == 5:
                    debounce = short_debounce
                    system_control.send(key_press)

                keys[k].set_led(0, 0, 0)

    # If enough time has passed, reset the fired variable
    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False
        systemLed.value = False
