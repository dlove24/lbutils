# This module, and all included code, is made available under the terms of the MIT
# Licence
#
# Copyright 2022-2023, David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
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

"""
Implements a helper library and `Colour` class which holds the internal colour
representations used by the graphics library. The `Colour` class aims to
achieve three goals

1. To hold the internal (byte) representations of colours typically used by
small OLED and LED screens.
2. To convert between those internal representations, trading off space for
colour accuracy for instance
3. To provide a simple interface for the graphics library (and graphics routines)
which can make use of the colour representations: and without having to replicate
the detailed bit manipulation that colour storage and conversion involves.

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)

"""


class Colour:
    """
    A (packed) representation of a colour value, as `r` (red), `g` (green)
    and `b` (blue) components. The principle purpose of this class is to
    both hold the internal representation of the colour; and to make the
    manipulation of those colour values in other graphics routines as
    straightforward as possible.

    Attributes
    ----------

    as_565: int

        Provides the colour value in the RGB565 format, using the
        standard representation.

    """

    ##
    ## Constructors
    ##

    def __init__(self, r: int, g: int, b: int, isARM: bool = True) -> None:
        """
        Creates a (packed) representation of a colour value, from the
        three bytes `r` (red), `g` (green) and `b` (blue).

        Parameters
        ----------

        r: int
            The red component of the packed byte value, of which the lower five bytes are selected.
        g: int
            The green component of the packed byte value, of which the lower six bytes are selected.
        b: int
            The red component of the packed byte value, of which the lower five bytes are selected.
        isARM: bool
            Determines if the current platform is an ARM processor or not. This
            value is used to determine which order for the `word` representation
            of the colour returned to the caller. Defaults to `True` as required
            by the Pico H/W platform of the micro-controller development board.
        """
        self._r = r
        self._g = g
        self._b = b

    ##
    ## Properties
    ##

    @property
    def as_565(self) -> int:
        """
        Construct a packed word from the internal colour representation, with
        5 bits of red data, 6 of green, and 5 of blue. On ARM platforms
        the packed word representation has the high and low bytes swapped,
        and so looks like

        ````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        G2 G1 G0 B4 B3 B2 B1 B0 R4 R3 R2 R1 R0 G5 G4 G3
        ````

        On non-ARM platform, the internal representation follows the
        normal bit sequence for a 565 representation and looks like

        ````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        R4 R3 R2 R1 R0 G5 G4 G3 G2 G1 G0 B4 B3 B2 B1 B0
        ````

        Returns
        -------

        int:
            A packed byte value of the colour representation.

        """

        if self._is_ARM:
            return (
                (self._g & 0x1C) << 1 | (self._b >> 3) | (self._r & 0xF8) | self._g >> 5
            )
        else:
            return (self._r & 0xF8) << 8 | (self._g & 0xFC) << 3 | self._b >> 3
