# This module, and all included code, is made available under the terms of
# the MIT
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

"""Implements a helper library and `Colour` class which holds the internal
colour representations used by the graphics library. The `Colour` class aims to
achieve three goals.

1. To hold the internal (byte) representations of colours typically used by
small OLED and LED screens.
2. To convert between those internal representations, trading off space for
colour accuracy for instance
3. To provide a simple interface for the graphics library (and graphics routines)
which can make use of the colour representations: and without having to replicate
the detailed bit manipulation that colour storage and conversion involves.

## Colour Reference

In addition to the `Colour` class, a list of 16 'VGA' colours defined in the
HTML 4.01 specification is also provided. These provide common, named, colour
representations suitable for most displays, for instance as

````python
import lbutils.graphics as graphics

fg_colour = graphics.COLOUR_CYAN
````

A complete list of the 16 objects defined by the `lbutils.colours` module is
shown below

| Colour                                        | Colour Name | Hex Representation | Object Name        |
|-----------------------------------------------|-------------|--------------------|--------------------|
| <div style = "color:#000000"> &#9632; </div>  | Black       | `0x000000`         | COLOUR_BLACK       |
| <div style = "color:#C0C0C0"> &#9632; </div>  | Silver      | `0xC0C0C0`         | COLOUR_SILVER      |
| <div style = "color:#808080"> &#9632; </div>  | Grey        | `0x808080`         | COLOUR_GREY        |
| <div style = "color:#FFFFFF"> &#9632; </div>  | White       | `0xFFFFFF`         | COLOUR_WHITE       |
| <div style = "color:#800000"> &#9632; </div>  | Maroon      | `0x800000`         | COLOUR_MAROON      |
| <div style = "color:#FF0000"> &#9632; </div>  | Red         | `0xFF0000`         | COLOUR_RED         |
| <div style = "color:#800000"> &#9632; </div>  | Purple      | `0x800080`         | COLOUR_PURPLE      |
| <div style = "color:#FF00FF"> &#9632; </div>  | Fuchsia     | `0xFF00FF`         | COLOUR_FUCHSIIA    |
| <div style = "color:#008000"> &#9632; </div>  | Green       | `0x008000`         | COLOUR_GREEN       |
| <div style = "color:#00FF00"> &#9632; </div>  | Lime        | `0x00FF00`         | COLOUR_LIME        |
| <div style = "color:#808000"> &#9632; </div>  | Olive       | `0x808000`         | COLOUR_OLIVE       |
| <div style = "color:#FFFF00"> &#9632; </div>  | Yellow      | `0xFFFF00`         | COLOUR_YELLOW      |
| <div style = "color:#000080"> &#9632; </div>  | Navy        | `0x000080`         | COLOUR_NAVY        |
| <div style = "color:#0000FF"> &#9632; </div>  | Blue        | `0x0000FF`         | COLOUR_BLUE        |
| <div style = "color:#008080"> &#9632; </div>  | Teal        | `0x008080`         | COLOUR_TEAL        |
| <div style = "color:#00FFFF"> &#9632; </div>  | Aqua        | `0x00FFFF`         | COLOUR_AQUA        |

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)
"""

###
### Classes
###


class Colour:
    """A (packed) representation of a colour value, as `r` (red), `g` (green)
    and `b` (blue) components. The principle purpose of this class is to both
    hold the internal representation of the colour; and to make the manipulation
    of those colour values in other graphics routines as straightforward as
    possible.

    Attributes
    ----------
    bR: int, read-only
        The byte (`0..255`) of the red component of the colour
    bG: int, read-only
        The byte (`0..255`) of the green component of the colour
    bB: int, read-only
        The byte (`0..255`) of the blue component of the colour
    as_565: int, read-only
        Provides the colour value in the RGB565 format, using a single
        byte in the the standard platform representation.
    as_888: int, read-only
        Provides the colour value in the RGB888 format, using a
        double word for the colour value in the standard platform
        representation.
    isARM: bool, read-write
        Flag indicating if the colour value should use the ARM byte
        packing order in colour conversions. Defaults to `True` as
        set by the default constructor.

    Implementation
    --------------

    Where possible attribute values are cached, and so the first
    call of the attribute will be slightly slower than subsequent calls.

    !!! warning "Immutable Class"
        To ensure the accuracy of the returned value, the Colour is also
        assumed to be immutable once the constructor has completed. If
        the private (non-public) attributes are modified outside the
        constructor the behaviour of the class is undefined.
    """

    ##
    ## Constructors
    ##

    def __init__(self, r: int, g: int, b: int, isARM: bool = True) -> None:
        """Creates a representation of a colour value, from the three integers
        `r` (red), `g` (green) and `b` (blue). The class will accept anything
        which can be coerced to an integer as arguments: the access through the
        attributes will determine the representation used when displaying the
        colour.

        Parameters
        ----------

        r: int
            The integer representing the red component of the colour.
        g: int
            The integer representing the green component of the colour.
        b: int
            The integer representing the blue component of the colour.
        isARM: bool, optional
            Determines if the current platform is an ARM processor or not. This
            value is used to determine which order for the `word` representation
            of the colour returned to the caller. Defaults to `True` as required
            by the Pico H/W platform of the micro-controller development board.
        """
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)

        self.isARM = isARM

        # Cached values
        self._565 = None
        self._888 = None

        self._bR = None
        self._bG = None
        self._bB = None

    ##
    ## Properties
    ##

    @property
    def bR(self) -> int:
        """The red component of the colour value, packed to a single byte."""
        if self._bR is None:
            self._bR = self._r & 0xFF

        return self._bR

    @property
    def bG(self) -> int:
        """The green component of the colour value, packed to a single byte."""
        if self._bG is None:
            self._bG = self._g & 0xFF

        return self._bG

    @property
    def bB(self) -> int:
        """The blue component of the colour value, packed to a single byte."""
        if self._bB is None:
            self._bB = self._b & 0xFF

        return self._bB

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
        # Check for a cached value ...
        if self._565 is None:
            # ... if there isn't one, calculate what the byte representation
            #     should look like
            if self.isARM:
                self._565 = (
                    (self._g & 0x1C) << 1
                    | (self._b >> 3)
                    | (self._r & 0xF8)
                    | self._g >> 5
                )
            else:
                self._565(self._r & 0xF8) << 8 | (self._g & 0xFC) << 3 | self._b >> 3

        # Return the calculated value to the client
        return self._565

    @property
    def as_888(self) -> int:
        """
        Construct a packed double word from the internal colour representation,
        with 8 bits of red data, 8 bits of green, and 8 of blue. For non-ARM
        platforms this results in a byte order for the two colour words as
        follows

        ````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        R4 R3 R2 R1 R0 G5 G4 G3 G2 G1 G0 B4 B3 B2 B1 B0
        ````

        On ARM platforms the packed word representation has the high and low
        bytes swapped in each word, and so looks like

        ````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        G2 G1 G0 B4 B3 B2 B1 B0 R4 R3 R2 R1 R0 G5 G4 G3
        ````

        Returns
        -------

        int:
            A packed double word value of the colour representation.

        """
        # Check for a cached value ...
        if self._888 is None:
            # ... if there isn't one, calculate what the byte representation
            #     should look like
            if self.isARM:
                self._888 = (
                    (self._g & 0x1C) << 1
                    | (self._b >> 3)
                    | (self._r & 0xF8)
                    | self._g >> 5
                )
            else:
                self._888(self._r & 0xF8) << 8 | (self._g & 0xFC) << 3 | self._b >> 3

        # Return the calculated value to the client
        return self._888


###
### Named Colours
###

COLOUR_BLACK = Colour(0, 0, 0)
COLOUR_BLUE = Colour(0, 0, 255)
COLOUR_CYAN = Colour(0, 255, 255)
COLOUR_GREY = Colour(128, 128, 128)
COLOUR_GREEN = Colour(0, 128, 0)
COLOUR_LIME = Colour(0, 255, 0)
COLOUR_MAGENTA = Colour(255, 0, 255)
COLOUR_MAROON = Colour(128, 0, 0)
COLOUR_NAVY = Colour(0, 0, 128)
COLOUR_OLIVE = Colour(128, 128, 0)
COLOUR_PURPLE = Colour(128, 0, 128)
COLOUR_RED = Colour(255, 0, 0)
COLOUR_SILVER = Colour(192, 192, 192)
COLOUR_TEAL = Colour(0, 128, 128)
COLOUR_WHITE = Colour(255, 255, 255)
COLOUR_YELLOW = Colour(255, 255, 0)
