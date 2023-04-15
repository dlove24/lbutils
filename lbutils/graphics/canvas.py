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

"""Implements an abstract [`Canvas`][lbutils.graphics.Canvas] class, used to
represent a drawing surface. The specific implemented of the drawing surface is
left to the derived display drivers, which sub-class
[`Canvas`][lbutils.graphics.Canvas]: see the _Examples_ section for details.

In most cases the use of the [`Canvas`][lbutils.graphics.Canvas] class is
similar to the
[`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html)
provided by MicroPython. Unlike the
[`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html)
class, however, the [`Canvas`][lbutils.graphics.Canvas] class _does not_
maintain a in-memory copy of the graphics display buffer, This means that the
[`Canvas`][lbutils.graphics.Canvas] class uses less memory by default (compared
to the
[`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html)
class): but at the cost of some flexibility. In particular it is **not**
possible to directly manipulate the display buffer of the
[`Canvas`][lbutils.graphics.Canvas] class. Instead _all_ drawing or changes to
the associated display buffer must be done through the
[`Canvas`][lbutils.graphics.Canvas] class itself.

The [`Canvas`][lbutils.graphics.Canvas] class also attempts to make as few
assumptions as possible about the underlying implementation: trading speed for
flexibility where necessary. In particular the
[`Canvas`][lbutils.graphics.Canvas] class makes no assumptions about the
underlying byte order of the display, not any assumptions about a specific
colour model. Instead these are abstracted into. Instead these are abstracted
into associated classes such as [`Colour`][lbutils.graphics.colours.Colour]
class). Those 'helper' classes will typically provide support for specific
implementations, or allow conversion between the internal representation of the
class and the underlying display protocols.

## Examples

The simplest derived class

````python
import lbutils.graphics as graphics

display = graphics.FrameBufferCanvas(width: int = 96,
        height: int = 64)
````

Once created, the [Canvas][lbutils.graphics.Canvas] drawing methods can be used
on the
[`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html).
For insance the
[`framebuffer`](https://docs.micropython.org/en/latest/library/framebuf.html)
can be cleared to black by

````python
display.fill_screen(graphics.colours.COLOUR_BLACK)
````

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
"""

# Import the ABC module if available. Use our backup version
# if the offical library is missing
try:
    from abc import ABC, abstractmethod
except ImportError:
    from lbutils.abc import ABC, abstractmethod

# Import the typing support
try:
    from typing import Type
except ImportError:
    from lbutils.typing import Type

# Import the lbutils graphics library
try:
    import lbutils.graphics as graphics
except ImportError:
    raise RuntimeError("Error: Missing required LBUtils graphics library")


class Canvas(ABC):
    """A Base Class which implements a drawing surface, and which provides
    utility methods for those drawing surfaces. The aim is to make is easier to
    use the specific display drivers, such as
    [`OLEDrgb`][lbutils.pmods.spi.oledrgb.OLEDrgb], and to provide basic drawing
    support for higher-level libraries.

    This drawing support is provided through the following categories of tools

    * **Drawing Primitives**: Provides basic support for drawing lines,
    rectangles, circles and triangles. This serves as a basic collection of
    primitives that can be relied upon by higher-level libraries.
    * **Font Support**: The `Canvas` maintains a record of the current font to
    use when writing text through the `font` attribute. This can be changed by
    users of the library, and defaults to [`Org_01`]
    [lbutils.graphics.fonts.Org_01].
    * **Colour Support**: Colours can be selected in different ways, and the
    `Canvas` maintains a foreground (`fg_color`) and background (`bg_color`)
    attribute: along with a common method to override these default colours
    quickly for individual drawing commands. Colours are selected by order of
    precedence, which is defined as

        1. The `Colour`s directly specified in the method call of the drawing
        primitive.
        2. The colours specified by the `Pen` in the method call of the drawing
        primitive.
        3. The colours specified by the `Pen` of the `Canvas` object.
        4. The colours specified by as the default (forground or background)
        colour of the `Canvas` object.
        5. As a default of white (`COLOUR_WHITE`) for the foreground, and black
        (`COLOUR_BLACK`) if all other selection methods fail.

    Attributes
    ----------

    bg_colour:
         The background [`Colour`][lbutils.graphics.colours.Colour] to use when
         drawing.
    cursor:
         The [`x`][lbutils.graphics.helpers.BoundPixel] and [`y`]
         [lbutils.graphics.helpers.BoundPixel] locations  of the current write
         (or read) operation.
    font:
         The sub-class of [`BaseFont`][lbutils.graphics.fonts.base_font.BaseFont]
         to use when drawing characters.
    fg_colour:
         The foreground [`Colour`][lbutils.graphics.colours.Colour] to use when
         drawing.
    pen:
         The [`Pen`][lbutils.graphics.Pen] to use when drawing on the canvas.
    height:
         A read-only value for the height of the canvas in pixels.
    width:
         A read-only value for the width of the canvas in pixels.
    x: int
            The X co-ordinate value of the `cursor`
    y: int
            The Y co-ordinate value of the `cursor`
    x_y: int
            A tuple representing the co-ordinate (x ,y) of the `cursor`

    Methods
    ----------

    * `draw_line()`. Draw a line from two co-ordinates.

    * `draw_rectangle()`. Draw a rectangle at the co-ordinate (x, y) of height
    and width, using the linecolour for the frame of the rectangle and fillcolour
    as the interior colour.

    * `fill_screen()`. Fill the entire `Canvas` with the background colour.

    * `move_to()`. Move the internal [`cursor`]
    [lbutils.graphics.helpers.BoundPixel]  to the co-ordinate values (x, y).

    * `read_pixel()`. Return the [`Colour`][lbutils.graphics.colours.Colour] of
    the specified pixel.

    * `write_char()`. Write a character (using the current font) starting at the
    stated pixel position.

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

    def __init__(self, width: int, height: int, isARM: bool = True) -> None:
        """Creates a (packed) representation of a colour value, from the three
        bytes `r` (red), `g` (green) and `b` (blue).

        Parameters
        ----------

        width: int
             The width in pixels of the display.
        height: int
             The height in pixels of the display.
        isARM: bool, optional
             Determines if the current platform is an ARM processor or not. This
             value is used to determine which order for the `word` representation
             of the colour returned to the caller. Defaults to `True` as required
             by the Pico H/W platform of the micro-controller development board.
        """
        # Set the Attribute Values. Note use the properties to ensure
        # that the type being set is correct
        if isARM:
            self.fg_colour = graphics.colours.COLOUR_WHITE
            self.bg_colour = graphics.colours.COLOUR_BLACK
        else:
            self.fg_color = graphics.color.Colour(255, 255, 255, isARM=False)
            self.bg_color = graphics.color.Colour(0, 0, 0, isARM=False)

        self.pen = None

        self.cursor = graphics.helpers.BoundPixel(
            0, 0, min_x=0, max_x=width, min_y=0, max_y=height, clip=True
        )

    ##
    ## Properties
    ##

    @property
    def x(self) -> int:
        """The `x` co-ordinate of the `cursor`; checking that it lies within the
        specified `width` of the `Canvas` when setting."""
        return self.cursor.x

    @x.setter
    def x(self, value: int) -> None:
        self.cursor.x = value

    @property
    def y(self) -> int:
        """The `y` co-ordinate of the `cursor`; checking that it lies within the
        specified `height` of the `Canvas` when setting."""
        return self.cursor.y

    @y.setter
    def y(self, value: int) -> None:
        self.cursor.y = value

    @property
    def x_y(self) -> tuple:
        """Sets, or returns, the internal `x` and `y` co-ordinates of the
        `cursor` as tuple.

        When _reading_ from this property, a tuple is returned with the first
        value of the tuple representing the `x` co-ordinate and the second
        value of the tuple representing the `y` co-ordinate.

        When _writing_ to this property the first value of the tuple represents
        the `x` co-ordinate, and the second value of the tuple represents the `y`
        co-ordinate. All other values in the tuple are ignored.

        Raises
        ------

        ValueError:
            If the `x` or `y` co-ordinate in the `xy` tuple cannot be converted
            to an integer.
        """
        return self.cursor.x_y

    @x_y.setter
    def x_y(self, xy: tuple) -> None:
        self.cursor.x = int(xy[0])
        self.cursor.y = int(xy[1])

    ##
    ## Abstract Methods. These must be defined in sub-classes.
    ##

    @abstractmethod
    def read_pixel(self, x: int, y: int) -> Type[graphics.Colour]:
        """Read the colour value of the pixel at position (`x`, `y`) and return
        to the caller.

        Parameters
        ----------

        x: int
            The x co-ordinate of the pixel to read
        y: int
            The y co-ordinate of the pixel to read

        Returns
        -------

        Type[Colour]:
             The [`Colour`][lbutils.graphics.Colour] representation of the pixel
             located at (x, y).
        """
        pass

    @abstractmethod
    def write_pixel(self, x: int, y: int, colour: Type[graphics.Colour]) -> None:
        """Set the pixel at position (`x`, `y`) to the specified colour value.

        Parameters
        ----------

        x: int
             The X co-ordinate of the pixel to set.
        y: int
             The Y co-ordinate of the pixel to set.
        colour: Type[Colour]
             The [`Colour`][lbutils.graphics.Colour] representation of the pixel
             located at (x, y).
        """
        pass

    @abstractmethod
    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        fg_colour: Type[graphics.Colour] = None,
        pen: Type[graphics.Pen] = None,
    ) -> None:
        """Draw a line from co-ordinates (`x2`, `y2`) to (`x2`, `y2`) using the
        specified RGB colour.

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
        fg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
             line. If not specified, use the preference order for the foreground
             colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
             The [`Pen`][lbutils.graphics.Pen] to be used when drawing the line.
             If not specified, use the preference order for the foreground colour
             of the `Canvas` to find a suitable colour.
        """
        pass

    @abstractmethod
    def draw_rectangle(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fg_colour: Type[graphics.Colour] = None,
        bg_colour: Type[graphics.Colour] = None,
        pen: Type[graphics.Pen] = None,
        filled: bool = True,
    ) -> None:
        """Draw a rectangle at the co-ordinate (`x`, `y`) of `height` and
        `width`, using the `linecolour` for the frame of the rectangle and
        `fillcolour` as the interior colour.

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
        fg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
             rectangle. If not specified, use the preference order for the
             foreground colour of the `Canvas` to find a suitable colour.
        bg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when filling the
             rectangle. If not specified, use the preference order for the
             background colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
             The [`Pen`][lbutils.graphics.Pen] to be used when drawing the
             rectangle, using the forground colour for the frame and the
             background colour for the fill. If not specified, use the preference
             order for the foreground and background colours of the `Canvas` to
             find suitable colours.
        filled: bool, optional
             If `True` (the default) the rectangle is filled with the background
             colour: otherwise the rectangle is not filled.
        """
        pass

    ##
    ## Methods
    ##

    def select_fg_color(
        self, fg_colour: Type[graphics.Colour] = None, pen: Type[graphics.Pen] = None
    ):
        """Return the colour to be used for drawing in the foreground, taking
        into account the (optional) overrides specified in `color` and `pen`.
        The selected colour will obey the standard colour selection precedence
        of the `Canvas` class, and is guaranteed to return a valid
        `Colour`][lbutils.graphics.colors.Colour] object.

        Paramaters
        ----------

        fg_colour: Type[graphics.Colour], optional
             Overrides the current `Canvas` forground colour, using the specified
             `fg_colour` instead.
        pen: Type[graphics.Pen], optional
             Overrides the current `Canvas` pen, using the forground colour of the specified
             `pen` to choose the returned `Colour`.

        Implementation
        --------------

        The returned [`Colour`][lbutils.graphics.Colour] object is selected
        according the defined precedence

             1. The `Colour` directly specified in the method call.
             2. The foreground colour specified by the `Pen` in the method call
             of the drawing primitive.
             3. The foreground colour specified by the `Pen` of the `Canvas`
             object.
             4. The colour specified by as the default forground colour of the
                  `Canvas` object.
             5. As a default of white (`COLOUR_WHITE`) for the foreground if all
             other selection methods fail.

        Returns
        -------

        Type[Colour]:
             A [`Colour`][lbutils.graphics.Colour] object representing the
             current foreground colour of the `Canvas`
        """

        if pen is not None:
            return fg_colour
        elif fg_colour is not None:
            return fg_colour
        elif self.pen is not None:
            return self.pen.fg_colour
        elif self.fg_colour is not None:
            return self.fg_colour
        else:
            return graphics.colours.COLOUR_WHITE

    def select_bg_color(
        self, bg_colour: Type[graphics.Colour] = None, pen: Type[graphics.Pen] = None
    ):
        """Return the colour to be used for drawing in the background, taking
        into account the (optional) overrides specified in `bg_color` and `pen`.
        The selected colour will obey the standard colour selection precedence
        of the `Canvas` class, and is guaranteed to return a valid
        `Colour`][lbutils.graphics.colors.Colour] object.

        Paramaters
        ----------

        bg_colour: Type[graphics.Colour], optional
             Overrides the current `Canvas` background [`Colour`][lbutils.graphics.Colour],
             using the specified `bg_colour` instead.
        pen: Type[graphics.Pen], optional
             Overrides the current `Canvas` pen, using the background colour of
             the specified `pen` to choose the returned [`Colour`][lbutils.graphics.Colour].

        Implementation
        --------------

        The returned [`Colour`][lbutils.graphics.Colour] object is selected
        according the defined precedence

        1. The `Colour` directly specified in the method call.
        2. The background colour specified by the `Pen` in the method call of the
        drawing primitive.
        3. The background colour specified by the `Pen` of the `Canvas` object.
        4. The colour specified by as the default background colour of
        the`Canvas` object.
        5. As a default of black (`COLOUR_BLACK`) if all other selection methods
        fail.

        Returns
        -------

        Type[Colour]:
             A [`Colour`][lbutils.graphics.Colour] object representing the
             current background colour of the `Canvas`.
        """

        if pen is not None:
            return bg_colour
        elif bg_colour is not None:
            return bg_colour
        elif self.pen is not None:
            return self.pen.bg_colour
        elif self.bg_colour is not None:
            return self.bg_colour
        else:
            return graphics.colours.COLOUR_BLACK

    def fill_screen(self, bg_colour: Type[graphics.Colour] = None) -> None:
        """Fill the entire display with the specified colour. By default this
        will use the colour preference order to find a background colour if
        `bg_colour` is `None`.

        Parameters
        ----------

        bg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used to fill the
             screen. Defaults to using the colour search order of the `Canvas`
             to find a colour.
        """
        fill_colour = self.select_bg_color(bg_colour=bg_colour)

        self.draw_rectangle(
            0,
            0,
            width=self.width,
            height=self.height,
            fg_colour=fill_colour,
            bg_colour=fill_colour,
            filled=True,
        )

    def move_to(self, xy: tuple) -> None:
        """Sets the internal `x` and `y` co-ordinates of the `cursor` as a
        tuple. An alias for the `x_y` property of `Canvas`.

        Parameters
        ----------

        xy: tuple
            The first value of the `xy` tuple represents the `x` co-ordinate, and
            the second value of the `xy` tuple represents the `y` co-ordinate.
            All other values in the `xy` tuple are ignored.

        Raises
        ------

        ValueError:
            If the `x` or `y` co-ordinate in the `xy` tuple cannot be converted
            to an integer.
        """
        self.cursor.x_y = xy

    def write_text(
        self,
        txt_str: str,
        fg_colour: Type[graphics.Colour] = None,
        pen: Type[graphics.Pen] = None,
    ) -> None:
        """Write the string `txt_str` (using the current `font`) starting at the
        the pixel position (`x`, `y`) of the `cursor` in the specified `colour`
        to the display.

        !!! note
             Whilst the `txt_str` character _must_ be a valid UTF-8 string, most
             fonts only support the equivalent of the (7-bit) ASCII character
             set. This method _will not_ display character values that cannot be
             supported by the underlying font. See the font description for the
             exact values that are valid for the specific font being used.

        Parameters
        ----------

        txt_str:
             The string of characters to write to the display.
        fg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
             line. If not specified, use the preference order for the foreground
             colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
             The [`Pen`][lbutils.graphics.Pen] to be used when drawing the line.
             If not specified, use the preference order for the foreground colour
             of the `Canvas` to find a suitable colour.
        """

        if self.font is not None:
            for character in txt_str:
                self.write_char(
                    character,
                    fg_colour=fg_colour,
                    pen=pen,
                )

    def write_char(
        self,
        utf8Char: str,
        fg_colour: Type[graphics.Colour] = None,
        pen: Type[graphics.Pen] = None,
    ) -> None:
        """Write a `utf8Char` character (using the current `font`) starting at
        the pixel position (`x`, `y`) of the `cursor` in the specified `colour`.

        !!! note
            Whilst the `utf8Char` character _must_ be a valid UTF-8 character,
            most fonts only support the equivalent of the (7-bit) ASCII character
            set. This method _will not_ display character values that cannot be
            supported by the underlying font. See the font description for the
            exact values that are valid for the specific font being used.

        Parameters
        ----------

        utf8Char:
            The character to write to the display.
        fg_colour: Type[graphics.Colour], optional
            The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
            character. If not specified, use the preference order for the
            foreground colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
            The [`Pen`][lbutils.graphics.Pen] to be used when drawing the line.
            If not specified, use the preference order for the foreground colour
            of the `Canvas` to find a suitable colour.
        """

        fg_colour = self.select_fg_color(fg_colour=fg_colour, pen=pen)

        self.font.set_position(utf8Char)
        _offset, _width, _height, _cursor, x_off, y_off = self.font.current_glyph

        for y1 in range(_height):
            for x1 in range(_width):
                if self.font.get_next():
                    self.write_pixel(
                        self.cursor.x + x1 + x_off,
                        self.cursor.y + y1 + y_off,
                        fg_colour,
                    )
        self.cursor.x += _cursor


class FrameBufferCanvas(Canvas):
    """A [Canvas][lbutils.graphics.Canvas] backed by a [`framebuffer`](https://d
    ocs.micropython.org/en/latest/library/framebuf.html)."""

    pass
