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
Implements an abstract [`Canvas`][lbutils.graphics.canvas.Canvas] class, used to
represent the drawing surface implemented by the underlying display drivers.
This class is close to a [`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html): but exposes more 'utility' methods for
drawing lines, rectangles, circles, etc. than the underlying [`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html). It
also provides support for colour representation on displays (through the
[`Colour`][lbutils.graphics.colours.Colour] class), as well as also font support
(through sub-classes of
[`BaseFont`][lbutils.graphics.fonts.base_font.BaseFont]).

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)

"""

# Import the ABC module if available. Use our backup version
# if the offical library is missing
try:
    from abc import ABC, abstractmethod
except ImportError:
    from lbutils.abc import ABC, abstractmethod

# Import the lbutils graphics library
try:
    import lbutils.graphics as graphics
except ImportError:
    raise RuntimeError("Error: Missing required LBUtils graphics library")


class Canvas(ABC):
    """
    A Base Class which implements a drawing surface, and which
    provides utility methods for those drawing surfaces. The aim is to
    make is easier to use the specific display drivers, such as [`OLEDrgb`][lbutils.pmods.spi.oledrgb.OLEDrgb]; and to provide basic drawing
    support for higher-level libraries.

    Attributes
    ----------

    bg_colour:
        The background [`Colour`][lbutils.graphics.colours.Colour] to use when drawing.
    font:
        The sub-class of [`BaseFont`][lbutils.graphics.fonts.base_font.BaseFont]
        to use when drawing characters.
    fg_colour:
        The foreground [`Colour`][lbutils.graphics.colours.Colour] to use when
        drawing.
    height:
        A read-only value for the height of the canvas in pixels.
    width:
        A read-only value for the width of the canvas in pixels.

    Methods
    ----------

    * `draw_line()`. Draw a line from two co-ordinates.

    * `draw_rectangle()`. Draw a rectangle at the co-ordinate (x, y) of height and width, using the linecolour for the frame of the rectangle and fillcolour as the interior colour.

    * `fill()`. Fill the entire `Canvas` with the background colour.

    * `read_pixel()`. Return the [`Colour`][lbutils.graphics.colours.Colour] of
    the specified pixel.

    * `write_char()`. Write a character (using the current font) starting at the stated pixel position.

    * `write_pixel()`. Set the pixel at the specified position to the foreground
    colour value.

    * `write_text()`. Write the a string (using the current font) starting at the
    specified pixel position in the specified colour.

    Implementation
    --------------

    Many of the drawing methods implemented here are provided in the
    most generic manner possible: i.e. they are not fully optimised
    for speed. In most cases the sub-classes can (and should) use the
    accelerated drawing primitives available on specific hardware to
    improve the routines provided here.
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

        # Set the Attribute Values. Note use the properties to ensure
        # that the type being set is correct
        self.bg_colour = graphics.colours.COLOUR_BLACK
        self.fg_colour = graphics.colours.COLOUR_WHITE

    ##
    ## Properties
    ##

    ##
    ## Methods
    ##

    @abstractmethod
    def fill(self, colour: int = 0) -> None:
        """
        Fill the entire display with the specified colour. By default this
        will set the display to black, if no `colour` is specified.

        Parameters
        ----------

        colour: int
             The packaged byte representation of the colour to be used
             when the interior of the rectangle. Defaults to black.
        """

    @abstractmethod
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, colour: int) -> None:
        """
        Draw a line from co-ordinates (`x2`, `y2`) to (`x2`, `y2`) using the
        specified RGB colour. Use the [`color565`] method to construct a suitable RGB
        colour representation.

        Parameters
        ----------

        x1: int
             The X co-ordinate of the pixel for the start point of the line.
        y1: int
             The Y co-ordinate of the pixel for the start point of the line.
        x2: int
             The X co-ordinate of the pixel for the end point of the line.
        y2: int
             The Y co-ordinate of the pixel for the end point of the line.
        colour: int
             The packaged byte representation of the colour to be used
             when drawing the line.
        """

    @abstractmethod
    def draw_rectangle(
        self, x: int, y: int, width: int, height: int, linecolour: int, fillcolour: int
    ) -> None:
        """
        Draw a rectangle at the co-ordinate (`x`, `y`) of `height` and `width`,
        using the `linecolour` for the frame of the rectangle and `fillcolour` as the
        interior colour.

        Parameters
        ----------

        x: int
             The X co-ordinate of the pixel for the start point of the rectangle.
        y: int
             The Y co-ordinate of the pixel for the start point of the rectangle.
        width: int
             The width of the rectangle in pixels.
        height: int
             The hight of the rectangle in pixels.
        linecolour: int
             The packaged byte representation of the colour to be used
             when drawing the frame of the rectangle.
        fillcolour: int
             The packaged byte representation of the colour to be used
             when the interior of the rectangle. May be `None` if no fill is
             to be used.
        """

    @abstractmethod
    def read_pixel(self, x: int, y: int) -> int:
        """
        Read the colour value of the pixel at position (`x`, `y`) and return to the caller.

        Returns
        -------

        int:
             The packaged byte representation of the colour at the pixel location
             (x, y).
        """

    @abstractmethod
    def write_char(self, x: int, y: int, utf8Char: str, colour: int) -> int:
        """
        Write a `utf8Char` character (using the current `font`) starting
        at the pixel position (`x`, `y`) in the specified `colour`.

        !!! note
             Whilst the `utf8Char` character _must_ be a valid UTF-8
             character, most fonts only support the equivalent of the (7-bit) ASCII character
             set. This method _will not_ display character values that cannot be supported by
             the underlying font. See the font description for the exact values that are
             valid for the specific font being used.

        Parameters
        ----------

        x: int
             The X co-ordinate of the pixel for the character start position.
        y: int
             The Y co-ordinate of the pixel for the character start position.
        utf8Char:
             The character to write to the display.
        colour: int
             The packaged byte representation of the colour to be used
             when drawing the character.

        Returns
        -------

        int:
             The X pixel co-ordinate immediately following the character written
             in the specified font. This can be used to easily locate multiple characters at
             a given Y position: see also `write_text()`.
        """

    @abstractmethod
    def write_pixel(self, x: int, y: int, colour: int = 0) -> None:
        """
        Set the pixel at position (`x`, `y`) to the specified colour value.

        Parameters
        ----------

        x: int
            The X co-ordinate of the pixel to set.
        y: int
            The Y co-ordinate of the pixel to set.
        colour: int
            The packaged byte representation of the colour to be used
            when setting the pixel. Defaults to black.
        """

    @abstractmethod
    def write_text(self, x: int, y: int, txt_str: str, colour: int) -> None:
        """
        Write the string `txt_str` (using the current `font`) starting
        at the pixel position (`x`, `y`) in the specified `colour` to
        the display.

        !!! note
             Whilst the `txt_str` character _must_ be a valid UTF-8
             string, most fonts only support the equivalent of the (7-bit) ASCII character
             set. This method _will not_ display character values that cannot be supported by
             the underlying font. See the font description for the exact values that are
             valid for the specific font being used.

        Parameters
        ----------

        x: int
             The X co-ordinate of the pixel for the text start position.
        y: int
             The Y co-ordinate of the pixel for the text start position.
        txt_str:
             The string of characters to write to the display.
        colour: int
             The packaged byte representation of the colour to be used
             when drawing the character.
        """
