# This example, and all included code, is made available under the terms of the
# MIT License
#
# Copyright (c) 2023 David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""Example light sequencer for the [Pmod
LED](https://digilent.com/reference/pmod/pmodled/start). This example
demonstrates different ways of using the method of the
[`LED`][lbutils.pmods.gpio.led] interface class to set (and test) the LED state.

NOTE: This example expects the LED Pmod to be installed on the _upper_
      row of header pins. It **will not** appear to work if installed
      on the lower pins!

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W
"""

# Import the LB Utils driver for the Pmod LED
try:
    from lbutils.pmods.gpio import LED, PMOD_ROW
except ImportError:
    msg = "Error: Cannot find the Pmod LED driver!"
    raise RuntimeError(msg) from ImportError

# Import the core libraries
import utime

##
## Setup
##

# Create the controller (on the UPPER pins!)
led_controller = LED(pmod_row=PMOD_ROW.LOWER)

# Turn all LEDs off
led_controller.set_state(leds=[False, False, False, False])

##
## Setup the LEDs as a simple test sequence. This is the most basic
## access method and is designed for simple 'set/check' tests only
##

print("Turning all LEDs on in sequence...")

led_controller.led0 = True
utime.sleep(1)
led_controller.led1 = True
utime.sleep(1)
led_controller.led2 = True
utime.sleep(1)
led_controller.led3 = True
utime.sleep(1)

print("Turning all LEDs off in sequence...")

led_controller.led3 = False
utime.sleep(1)
led_controller.led2 = False
utime.sleep(1)
led_controller.led1 = False
utime.sleep(1)
led_controller.led0 = False
utime.sleep(1)

##
## Alternate Flashing: showing two different access methods
##

print("Flashing for 10 seconds...")

for index in range(1, 10):
    if index % 2 == 0:
        led_controller.set_state(leds=[True, False, True, False])
    else:
        led_controller.set_state(False, True, False, True)  # noqa: FBT003

    utime.sleep(1)

##
## Turn all LEDs off
##

print("Shutting down.")

led_controller.set_state(leds=[False, False, False, False])
