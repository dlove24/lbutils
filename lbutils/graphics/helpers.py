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

"""Provides utility classes and functions which ease the abstraction of the main
graphics `Canvas` library. These are typically used to abstract and encapsulate
common concepts such as a `Pixel`: but which are small enough not a warrant a
separate library.

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)
"""

# Import the typing hints if available. Use our backup version
# if the offical library is missing
try:
    from typing import Type
except ImportError:
    from lbutils.typing import Type

from .colours import Colour, COLOUR_WHITE, COLOUR_BLACK

###
### Classes
###


class Pen:
    """Implements a convenience class for the graphics library, which represents
    a 'pen' with a specified foreground and background colour, and thickness.
    The primary purpose of this class is to make it easy to swap between common
    colour and line values; for instance using two pens to allow a swap between
    'highlight' and 'normal' text colours. This can be accomplished by defining
    the foreground and background colour of the
    [`Canvas`][lbutils.graphics.canvas] as needed: this class simply makes that
    switch easier.

    Example
    -------

    Two new pens can be defined for 'normal' and 'alert' text as

    ````python
    normal_text = Pen(COLOUR_WHITE)
    alter_text = Pen(COLOUR_RED)
    ````

    This defines a `normal_text` pen with a white foreground and default
    background and line thickness (black and 1 pixel byt default). A second pen
    for `alter_text` has a red foreground, and similarly a black background with
    1 pixel thickness. Text can then be written on the canvas using these two
    pens on a `Canvas` as

    ````python
    canvas = Canvas(width = 96, height = 48)

    canvas.write_text(0, 10, "This is normal text", pen = normal_text)
    canvas.write_text(0, 20, "and this is alert", pen = altert_text)
    canvas.write_text(0, 30, "Now everything is back to normal", pen = normal_text)
    ````

    Attributes
    ----------

    bg_colour: Type[Colour], optional
            The background colour of the pen. Defaults to black.
    fg_colour: Type[Colour], optional
            The foreground colour of the pen. Defaults to white.
    thickness: int, optional
            The line thickness of the pen. Defaults to 1 pixel.
    """

    def __init__(
        self,
        fg_colour: Type[Colour] = COLOUR_WHITE,
        bg_colour: Type[Colour] = COLOUR_BLACK,
        thickness: int = 1,
    ) -> None:
        """Creates a `Pen` instance, using the specified foreground and
        background colour, and line thickness."""

        self.bg_colour = bg_colour
        self.fg_colour = fg_colour

        self.thickness = int(thickness)


class Pixel:
    """Represents a Cartesian co-ordinate. Used as a convenience class for
    instances such as cursors where a relationship between a X and a Y co-
    ordinate must be maintained. This is also useful when two or more co-
    ordinates need to be tracked, or to be switched between. For instance an
    'origin' co-ordinate for a drawing, and a 'current' co-ordinate around the
    origin where lines are being drawn to and from.

    !!! note "Implementation Defined Origin"
            As for the [`Canvas`][lbutils.graphics.canvas] class, the
            interpretation of the point '(0, 0)' is defined by the underlying
            graphics implementation. For instance the '(0, 0)' point may
            represent the top-left corner or the canvas, or the bottom- left hand
            corner. For details of how this point will be chosen (or changed),
            see the implementation of the specified sub-class of `Canvas` that is
            implemented by the chosen display driver.

    Attributes
    ----------

    x: int
            The X co-ordinate value.
    y: int
            The Y co-ordinate value.
    x_y: int
            A tuple representing the co-ordinate (x ,y).

    Methods
    ----------

    * `move_to()`. Move the internal co-ordinate to the value (x, y).
    """

    ##
    ## Constructors
    ##

    def __init__(self, x: int, y: int) -> None:
        """Creates a `Pixel` instance holding the specified `x` and `y` co-
        ordinates, together representing the Cartesian point '(`x`, `y`)'.

        Parameters
        ----------

        x: int
                The initial X co-ordinate value.
        y: int
                The initial Y co-ordinate value
        """
        self.x = int(x)
        self.y = int(y)

    ##
    ## Properties
    ##

    @property
    def x_y(self) -> tuple:
        """Sets, or returns, the internal `x` and `y` co-ordinates as a tuple.

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
        return [self._x, self._y]

    @x_y.setter
    def x_y(self, xy: tuple) -> None:
        self.x = int(xy[0])
        self.y = int(xy[1])

    ##
    ## Methods
    ##

    def move_to(self, xy: tuple) -> None:
        """Sets the internal `x` and `y` co-ordinates as a tuple. An alias for
        the `x_y` property.

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
        self.x_y = xy


class BoundPixel(Pixel):
    """Represents a Cartesian co-ordinate between limits. Used as a convenience
    class for instances such as cursors where a relationship between a X and a Y
    co-ordinate must be maintained. This is also useful when two or more co-
    ordinates need to be tracked, or to be switched between. For instance an
    'origin' co-ordinate for a drawing, and a 'current' co-ordinate around the
    origin where lines are being drawn to and from.

    Unlike the [`Pixel`][lbutils.graphics.Pixel] class, the `BoundPxiel` will
    also ensure that the X and Y co-ordinates are maintained between minimum and
    maximum value for the `width` or `height`. This is useful for instances where a
    cursor, for instance, must only take values within the limits of a display. It
    can also be used where a clipping region is being defined to ensure that values
    cannot lie outside the clipped region.

    !!! note "Implementation Defined Origin"
            As for the [`Canvas`][lbutils.graphics.canvas] class, the
            interpretation of the point '(0, 0)' is defined by the underlying
            graphics implementation. For instance the '(0, 0)' point may
            represent the top-left corner or the canvas, or the bottom- left hand
            corner. For details of how this point will be chosen (or changed),
            see the implementation of the specified sub-class of `Canvas` that is
            implemented by the chosen display driver.

    Attributes
    ----------

    x: int
            The X co-oridinate value.
    y: int
            The Y co-ordinate value.
    min_x: int
            The minimum value allowed for the `x` co-ordinate. Defaults to
            `0`.
    min_y: int
            The minimum value allowed for the `y` co-ordinate. Defaults to
            `0`.`
    max_x: int
            The maximum value allowed for the `x` co-ordinate.
    max_y: int
            The maximum value allowed for the `y` co-ordinate.
    """

    ##
    ## Constructors
    ##

    def __init__(
        self,
        x: int,
        y: int,
        max_x: int,
        max_y: int,
        min_x: int = 0,
        min_y: int = 0,
        clip: bool = True,
    ) -> None:
        """Creates a `Pixel` instance holding the specified `x` and `y` co-
        ordinates, together representing the Cartesian point '(`x`, `y`)'. This
        `x` and `y` value is guaranteed to be maintained between `min_x` and
        `max_x` for the `x` co- ordinate, and `min_y` and `max_y` for the `y`
        co-ordinate.

        Parameters
        ----------

        x: int
                The initial X co-ordinate value.
        y: int
                The initial Y co-ordinate value.
        max_x: int
                The maximum value allowed for the `x` co-ordinate.
        max_y: int
                The maximum value allowed for the `y` co-ordinate.
        min_x: int, optional
                The minimum value allowed for the `x` co-ordinate. Defaults to
                `0`.
        min_y: int, optional
                The minimum value allowed for the `y` co-ordinate. Defaults to
                `0`.`
        clip: bool, optional
                If set to `True`, the default, silently clip the `x` and `y` co-
                ordinates to the specified limits. If set to `False`, instead
                raise a `ValueError` if the `x` or `y` co-ordinates do not fall
                into the allowed limits.

        Implementation
        --------------

        As the `x` and `y` attributes of this class are compared on each write,
        this class is by definition slower and potentially more resource intensive that
        the underlying `Pixel` class. If the costs of the bounds-check are not required,
        using the 'raw' `Pixel` class may be preferable.

        !!! note
                The parameter order is specified to allow easier definition
                in the common case where the lower limits for `x` and `y` are
                `0`, and the positional parameter order is being used. If all
                four limits are being used, consider the use of named
                parameters to avoid ambiguity.
        """

        # Set-up the maximum and minimum parameters first
        self.min_x = int(min_x)
        self.max_x = int(max_x)

        self.min_y = int(min_y)
        self.max_y = int(max_y)

        # Now attempt to set the actual `x` and `y` inside those
        # parameters
        self.x = int(x)
        self.y = int(y)

        # Set the clipping switch
        self.clip = clip

    ##
    ## Properties
    ##

    @property
    def x(self) -> int:
        """The `x` co-ordinate of the `BoundPxiel`, checking that it lies within
        the specified `min_x` and `max_x` limits.

        Raises
        ------

        `ValueError`:
                If `clip` is set to `False`
        """
        if self.min_x <= self._x <= self.max_x:
            return self._x
        else:
            if self.clip:
                if self._x > self.max_x:
                    self._x = self.max_x
                if self._x < self.min_x:
                    self._x = self.min_x

                return self._x

            else:
                raise (ValueError("Pixel limits exceeded"))

    @x.setter
    def x(self, value: int) -> None:
        if self.min_x <= value <= self.max_x:
            self._x = value
        else:
            if self.clip:
                if value > self.max_x:
                    self._x = self.max_x
                if value < self.min_x:
                    self._x = self.min_x

            else:
                raise (ValueError("Pixel limits exceeded"))

    @property
    def y(self) -> int:
        """The `y` co-ordinate of the `BoundPxiel`, checking that it lies within
        the specified `min_x` and `max_y` limits.

        Raises
        ------

        `ValueError`:
                If `clip` is set to `False`
        """
        if self.min_y <= self._y <= self.max_y:
            return self._y
        else:
            if self.clip:
                if self._y > self.max_y:
                    self._y = self.max_y
                if self._y < self.min_y:
                    self._y = self.min_y

                return self._y

            else:
                raise (ValueError("Pixel limits exceeded"))

    @y.setter
    def y(self, value: int) -> None:
        if self.min_y <= value <= self.max_y:
            self._y = value
        else:
            if self.clip:
                if value > self.max_y:
                    self._y = self.max_y
                if value < self.min_y:
                    self._y = self.min_y

            else:
                raise (ValueError("Pixel limits exceeded"))
