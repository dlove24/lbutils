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

# Import the typing hints if available. Use our backup version
# if the official library is missing
try:
    from typing import Literal, Optional
except ImportError:
    from lbutils.std.typing import Literal, Optional  # type: ignore

# Import the official Python 3 library if we can, or the MicroPython version
# if that fails
try:
    from platform import uname
except ImportError:
    from os import uname  # type: ignore

# Import the enumerations library. Unfortunately the full version in not
# in MicroPython yet, so this is a bit of a hack
try:
    from enum import IntEnum
except ImportError:
    from urest.enum import IntEnum  # type: ignore

###
### Enumerations
###


class DEVICE_BIT_ORDER(IntEnum):
    """Set the bit order to be used (mostly in graphics code) for low-level
    manipulation of bits send to, and received from, devices."""

    ARM = 0
    INTEL = 1

    ##
    ## Methods
    ##
    @staticmethod
    def platform() -> "DEVICE_BIT_ORDER":
        """Attempt to determine the platform automatically:

        defaulting to the ARM bit order if the native order cannot be
        determined.
        """
        machine = uname()

        if machine[4].find("x86") != -1:
            return DEVICE_BIT_ORDER.INTEL
        else:
            return DEVICE_BIT_ORDER.ARM


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
    red: int, read-only
        The byte (`0..255`) of the red component of the colour
    green: int, read-only
        The byte (`0..255`) of the green component of the colour
    blue: int, read-only
        The byte (`0..255`) of the blue component of the colour
    as_rgb565: int, read-only
        Provides the colour value in the RGB565 format, using a single
        byte in the the standard platform representation.
    as_rgb888: int, read-only
        Provides the colour value in the RGB888 format, using a
        double word for the colour value in the standard platform
        representation.
    bit_order: DEVICE_BIT_ORDER, read-write
        Argument indicating if the underlying bit order used for
        the bit packing order in colour conversions. Defaults to
        auto-detect the bit order in the default constructor.

    Methods
    -------

    from_565: Color
        Create a [`Colour`][lbutils.graphics.Colour] object from the byte
        passed in as a parameter: assuming the byte is an RGB 565 packed
        byte.

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
    ## Internal Attributes
    ##

    _r: int
    _g: int
    _b: int

    _565: Optional[int]
    _888: Optional[int]

    _red: Optional[int]
    _green: Optional[int]
    _blue: Optional[int]

    ##
    ## Constructors
    ##

    def __init__(
        self,
        r: int,
        g: int,
        b: int,
        bit_order: DEVICE_BIT_ORDER = DEVICE_BIT_ORDER.platform(),
    ) -> None:
        """Create a representation of a colour value, from the three integers
        `r` (red), `g` (green) and `b` (blue). The class will accept anything
        which can be coerced to an integer as arguments: the methods used to
        access the colour (and the `bit_order`) will determine the byte order
        used as the final representation used when displaying the colour.

        Parameters
        ----------

        r: int
            The integer representing the red component of the colour.
        g: int
            The integer representing the green component of the colour.
        b: int
            The integer representing the blue component of the colour.
        bit_order: DEVICE_BIT_ORDER, read-write
            Argument indicating if the underlying bit order used for
            the bit packing order in colour conversions. Defaults to
            the platform bit order.
        """

        # Set the colour to the RGB value specified
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)

        # Record the bit order
        self.bit_order = bit_order

        # Cached values
        self._565 = None
        self._888 = None
        self._red = None
        self._green = None
        self._blue = None

    ##
    ## Properties
    ##

    @property
    def red(self) -> int:
        """The red component of the colour value, packed to a single byte."""
        if self._red is None:
            self._red = self._r & 0xFF

        return self._red

    @property
    def green(self) -> int:
        """The green component of the colour value, packed to a single byte."""
        if self._green is None:
            self._green = self._g & 0xFF

        return self._green

    @property
    def blue(self) -> int:
        """The blue component of the colour value, packed to a single byte."""
        if self._blue is None:
            self._blue = self._b & 0xFF

        return self._blue

    @property
    def as_rgb565(self) -> Optional[int]:
        """Construct a packed double word from the internal colour
        representation, with 8 bits of red data, 8 bits of green, and 8 of blue.
        For non-ARM platforms this results in a byte order for the two colour
        words as follows.

        ![````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        R4 R3 R2 R1 R0 G5 G4 G3 G2 G1 G0 B4 B3 B2 B1 B0
        ````](/media/colours_as_rgb565_fig1.svg)

        On ARM platforms the packed word representation has the high and low
        bytes swapped in each word, and so looks like

        ![
        ````
        F  E  D  C  B  A  9  8  7  6  5  4  3  2  1  0
        G2 G1 G0 B4 B3 B2 B1 B0 R4 R3 R2 R1 R0 G5 G4 G3
        ````](/media/colours_as_rgb565_fig2.svg)

        Returns
        -------

        int:
            A packed byte value of the colour representation.
        """
        # Check for a cached value ...
        if self._565 is None:
            # Set-up the 565 bit representation
            bits565 = (self._r & 0xF8) << 8 | (self._g & 0xFC) << 3 | self._b >> 3

            # For Intel that is all we need...
            if self.bit_order == DEVICE_BIT_ORDER.INTEL:
                self._565 = bits565
            # For ARM we need to swap the 'high' and 'low' bytes
            else:
                self._565 = (bits565 & 0xFF) << 8 | (bits565 >> 8)

        # Return the calculated value to the client
        return self._565

    @property
    def as_rgb888(self) -> Optional[int]:
        """Construct a packed double word from the internal colour
        representation, with 8 bits of red data, 8 bits of green, and 8 of blue.
        For non-ARM platforms this results in a byte order for the two colour
        words as follows.

        ![Intel Byte Order for RGB888 Structure](/media/colours_as_rgb888_fig1.svg)

        On ARM platforms the packed word representation has the high and low
        bytes swapped in each word, and so looks like

        ![ARM Byte Order for RGB888 Structure](/media/colours_as_rgb888_fig2.svg)

        Returns
        -------

        int:
            A packed double word value of the colour representation.
        """
        # Check for a cached value ...
        if self._888 is None:
            # ... if there isn't one, calculate what the byte representation
            #     should look like

            # Set-up the 888 bit representation as a double word with the
            # high byte of the high word 0x00 (all zeroes)
            bits888 = self._r << 16 | self._g << 8 | self._b

            # For Intel that is all we need...
            if self.bit_order == DEVICE_BIT_ORDER.INTEL:
                self._888 = bits888
            # For ARM we need to swap the 'high' and 'low' bytes in each word
            else:
                self._888 = (
                    ((bits888 & 0x00FF0000) << 8)
                    | ((bits888 & 0x000000FF) << 8)
                    | ((bits888 & 0x0000FF00) >> 8)
                )

        # Return the calculated value to the client
        return self._888

    ##
    ## Methods
    ##

    @staticmethod
    def from_565(rgb: int) -> "Colour":
        """Create a [`Colour`][lbutils.graphics.Colour] object from the byte
        passed in as a parameter: assuming the byte is an RGB 565 packed
        byte."""
        red = rgb & 0xF800
        green = rgb & 0x07E0
        blue = rgb & 0x001F

        new_colour = Colour(red, green, blue)

        return new_colour


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
