"""
Simple driver for a seven-segment display, requiring seven GPIO pins.

Overview
--------

This driver will only display characters in the range '0' to '9', and will raise a `ValueError` exception if the requested character is not in an appropriate range.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W

Licence
-------

This module, and all included code, is made available under the terms of the MIT Licence

> Copyright (c) 2023 Roz Wyatt-Millington, David Love

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import MicroPython libraries for GPIO access if available
try:
    from machine import ADC
    from machine import Pin
except ImportError:
    print("Ignoring MicroPython includes")


class SegDisplay:
    char_list = [
        [0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
    ]
    """

    """

    def __init__(self, gpio_reqest):
        self.pin_list = []

        if (gpio_reqest is None) or (not gpio_reqest):
            raise ValueError("The GPIO Request List is empty")
        elif len(gpio_reqest) != 7:
            raise ValueError("The GPIO Request List must be EXACTLY seven entries long")
        else:
            for segment in range(7):
                self.pin_list.append(Pin(gpio_reqest[segment], Pin.OUT))

    def display(self, character):
        if 0 <= character <= 9:
            for pin in range(7):
                self.pin_list[pin].value(self.char_list[character][pin])
        else:
            raise ValueError(
                "The display character must be between zero ('0') and nine ('9')"
            )
