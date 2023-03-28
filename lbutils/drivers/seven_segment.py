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
        [False, False, False, False, False, False, True],
        [True, False, False, True, True, True, True],
        [False, False, True, False, False, True, False],
        [False, False, False, False, True, True, False],
        [True, False, False, True, True, False, False],
        [False, True, False, False, True, False, False],
        [False, True, False, False, False, False, False],
        [False, False, False, True, True, True, True],
        [False, False, False, False, False, False, False],
        [False, False, False, True, True, False, False],
    ]
    """
    Defines how characters are rendered, from zero ('0') in the first entry to nine ('9') as the last entry. Note that pins which are listed here as `False` will be _on_ using the default options to the `display` method.
    """

    def __init__(self, gpio_reqest: list):
        """
        Initialise a seven-segment display, using the user supplied
        list of GPIO pins in `gpio_request` as reference for pins to
        drive.

        This class also assume a common anode seven-segment display by default, and so will assume that pulling a GPIO pin _low_ will turn the relevant segment _on_. If you need to modify this behaviour, see the `inverted` parameter for the `display` method.

        .. Note::
            This list of entries in the `gpio_request` _must_ be exactly seven entries long, or the class will throw a `ValueError` in the constructor.

        Parameters
        ----------

        gpio_reqest: list
            The pin-ordered list of GPIO pins to use for the segment positions 'a' (as the first entry in the list) to 'f' (as the last entry in the list).

            **NOTE**: The `SegDisplay` class will also attempt to create the underlying GPIO object for each of the entries in the list. If the GPIO pins need to be Initialised, this must be done _before_ calling this constructor.
        """
        self.pin_list = []

        if (gpio_reqest is None) or (not gpio_reqest):
            raise ValueError("The GPIO Request List is empty")
        elif len(gpio_reqest) != 7:
            raise ValueError("The GPIO Request List must be EXACTLY seven entries long")
        else:
            for segment in range(7):
                self.pin_list.append(Pin(gpio_reqest[segment], Pin.OUT))

    def display(self, character: int, inverted: bool = False):
        """
        Display the given `character` on the seven-segment display,
        using the `char_list` as a guide for which pins to turn on or off. By default the `display` method will use the entries in the `char_list` directly: if you need to invert the 'normal' sense, set the `inverted` parameter to `True`.

        Parameters
        ----------

        character: int
            The value to be displayed on the seven segment display, which must be between zero ('0') and nine ('9')

        inverted: bool
            By default the `display` method assumes that pulling a GPIO pin _low_ will turn the relevant segment _on_; i.e. the typical behaviour for a common anode display. If the attached display needs to raise a GPIO pin _high_ to set the segment _on_ (i.e. the typical behaviour for a common cathode display), call the `display` method with `inverted` set to `True`.
        """
        if 0 <= character <= 9:
            if not inverted:
                for pin in range(7):
                    self.pin_list[pin].value(self.char_list[character][pin])
            else:
                for pin in range(7):
                    self.pin_list[pin].value(not self.char_list[character][pin])
        else:
            raise ValueError(
                "The display character must be between zero ('0') and nine ('9')"
            )
