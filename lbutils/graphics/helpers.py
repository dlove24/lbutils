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

The classes and methods provided by this library are described below, and organised as shown

![Helper Class Diagrams](/media/helpers.svg)

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)
"""

# Import the math library (needed for polar co-ordinates)
from math import cos, sin

from .colours import COLOUR_BLACK, COLOUR_WHITE, Colour

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
    [`Canvas`][lbutils.graphics.Canvas] as needed: this class simply makes that
    switch easier.

    Example
    -------

    Two new pens can be defined for 'normal' and 'alert' text as

    ````python
    normal_text = Pen(COLOUR_WHITE)
    alert_text = Pen(COLOUR_RED)
    ````

    This defines a `normal_text` pen with a white foreground and default
    background and line thickness (black and 1 pixel byt default). A second pen
    for `alert_text` has a red foreground, and similarly a black background with
    1 pixel thickness. Text can then be written on the canvas using these two
    pens on a `Canvas` as

    ````python
    canvas = Canvas(width = 96, height = 48)

    canvas.write_text(start= (0, 10), "This is normal text", pen = normal_text)
    canvas.write_text(start= (0, 20), "and this is alert", pen = alert_text)
    canvas.write_text(start= (0, 30), "Now everything is back to normal", pen = normal_text)
    ````

    Attributes
    ----------

    bg_colour: Colour, optional
            The background colour of the pen. Defaults to black.
    fg_colour: Colour, optional
            The foreground colour of the pen. Defaults to white.
    thickness: int, optional
            The line thickness of the pen. Defaults to 1 pixel.
    """

    def __init__(
        self,
        fg_colour: Colour = COLOUR_WHITE,
        bg_colour: Colour = COLOUR_BLACK,
        thickness: int = 1,
    ) -> None:
        """Create a `Pen` instance, using the specified foreground and
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
            As for the [`Canvas`][lbutils.graphics.Canvas] class, the
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
    x_y: tuple[int, int]
            A tuple representing the co-ordinate (x ,y).

    Methods
    -------

    * `move_to()`. Move the internal co-ordinate to the value (x, y). An alias
    for the [`x_y`][lbutils.graphics.Pixel.x_y] property.
    * `offset()`. Returns a `tuple` representing the (x, y) co-ordinate of the
    current `Pixel` with the specified Cartesian off-set applied.
    * `offset_polar()`. Returns a `tuple` representing the (x, y) co-ordinate of
    the current `Pixel` with the specified Polar off-set applied.
    """

    ##
    ## Internal Attributes
    ##

    _x: int
    _y: int

    ##
    ## Constructors
    ##

    def __init__(self, x: int, y: int) -> None:
        """Create a `Pixel` instance holding the specified `x` and `y` co-
        ordinates, together representing the Cartesian point '(`x`, `y`)'.

        Parameters
        ----------

        x: int
                The initial X co-ordinate value.
        y: int
                The initial Y co-ordinate value.
        """
        self.x = int(x)
        self.y = int(y)

    ##
    ## Properties
    ##

    @property
    def x_y(self) -> tuple[int, int]:
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
        return (self._x, self._y)

    @x_y.setter
    def x_y(self, xy: tuple[int, int]) -> None:
        self.x = int(xy[0])
        self.y = int(xy[1])

    ##
    ## Properties
    ##

    @property
    def x(self) -> int:
        """The `x` co-ordinate of the `Pixel`."""
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = int(value)

    @property
    def y(self) -> int:
        """The `y` co-ordinate of the `Pixel`."""
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = int(value)

    ##
    ## Methods
    ##

    def move_to(self, xy: tuple[int, int]) -> None:
        """Set the internal `x` and `y` co-ordinates as a tuple. An alias for
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

    def offset(self, x: int = 0, y: int = 0) -> tuple[int, int]:
        """Return a `tuple` representing the (x, y) co-ordinate of the current
        `Pixel` with the specified Cartesian off-set applied.

        Example
        -------

        Given a `Pixel` object called `origin` with representing the co-ordinates
        '(0, 10)'

        ````python
        origin = Pixel(0, 10)
        ````

        then calling

        ````python
        new_origin = origin.offset(10, 10)
        ````

        or better

        ````python
        new_origin = origin.offset(x = 10, y = 10)
        ````

        will return the tuple `[10, 20]` as `new_origin`.

        Parameters
        ----------

        x: int, optional
            The offset to apply to the x co-ordinate value of the `Pixel`.
        y: int, optional
            The offset to apply to the x co-ordinate value of the `Pixel`.

        Returns
        -------

        tuple:
            The (x, y) co-ordinate as a two value `tuple`  with the
            first value of the `tuple` representing the `x` co-ordinate and the
            second value of the `tuple` representing the `y` co-ordinate.
        """
        return (self.x + x, self.y + y)

    def offset_polar(self, r: int = 0, theta: int = 0) -> tuple[int, int]:
        """Return a `tuple` representing the (x, y) co-ordinate of the current
        `Pixel` with the specified Polar off-set applied as the radius `r` and
        angle `theta`.

        !!! Note "Floating Point Calculations"
            Although the _return_ values of the `offset_polar` function will be
            integers, floating point routines are used internally to calculate
            the sine and cosine of the angle `theta`. This may result in this
            routine being slower than expected on some platforms.

        Example
        -------

        Given a `Pixel` object called `origin` with representing the co-ordinates
        '(0, 10)'

        ````python
        origin = Pixel(0, 10)
        ````

        then calling

        ````python
        new_origin = origin.offset_polar(13, 22)
        ````

        or better

        ````python
        new_origin = origin.offset(r = 13, theta = 22)
        ````

        will return the tuple `[12, 5]` as `new_origin`.

        Parameters
        ----------

        r: int, optional
            The offset to apply to the x co-ordinate value of the `Pixel`,
            specified as the _radius_ of the Polar co-ordinate.
        theta: int, optional
            The offset to apply to the x co-ordinate value of the `Pixel`,
            specified as the _angle_ of the Polar co-ordinate.

        Returns
        -------

        tuple:
            The (x, y) co-ordinate as a two value `tuple`  with the
            first value of the `tuple` representing the `x` co-ordinate and the
            second value of the `tuple` representing the `y` co-ordinate.
        """
        return (int(self.x + (r * cos(theta))), int(self.y + (r * sin(theta))))


class BoundPixel(Pixel):
    """Represents a Cartesian co-ordinate between limits. Used as a convenience
    class for instances such as cursors where a relationship between a X and a Y
    co-ordinate must be maintained. This is also useful when two or more co-
    ordinates need to be tracked, or to be switched between. For instance an
    'origin' co-ordinate for a drawing, and a 'current' co-ordinate around the
    origin where lines are being drawn to and from.

    Unlike the [`Pixel`][lbutils.graphics.Pixel] class, the `BoundPixel` will
    also ensure that the X and Y co-ordinates are maintained between minimum and
    maximum value for the `width` or `height`. This is useful for instances where
    a cursor, for instance, must only take values within the limits of a display.
    It can also be used where a clipping region is being defined to ensure that
    values cannot lie outside the clipped region.

    !!! note "Implementation Defined Origin"
            As for the [`Canvas`][lbutils.graphics.Canvas] class, the
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
    ) -> None:
        """Create a `Pixel` instance holding the specified `x` and `y` co-
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

        Implementation
        --------------

        As the `x` and `y` attributes of this class are compared on each write,
        this class is by definition slower and potentially more resource
        intensive that the underlying `Pixel` class. If the costs of the bounds-
        check are not required, using the 'raw' `Pixel` class may be preferable.

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

    ##
    ## Properties
    ##

    @property
    def x(self) -> int:
        """The `x` co-ordinate of the `BoundPixel`, checking that it lies within
        the specified `min_x` and `max_x` limits.

        If the `x` co-ordinate does lie outside the specified region, set it to
        the `min_x` or `max_x` limit as appropriate.
        """
        if self.min_x <= self._x <= self.max_x:
            return self._x
        else:
            if self._x > self.max_x:
                self._x = self.max_x
            if self._x < self.min_x:
                self._x = self.min_x

            return self._x

    @x.setter
    def x(self, value: int) -> None:
        if self.min_x <= value <= self.max_x:
            self._x = value
        else:
            if value > self.max_x:
                self._x = self.max_x
            if value < self.min_x:
                self._x = self.min_x

    @property
    def y(self) -> int:
        """The `y` co-ordinate of the `BoundPixel`, checking that it lies within
        the specified `min_x` and `max_y` limits.

        If the `y` co-ordinate does lie outside the specified region, set it to
        the `min_y` or `may_y` limit as appropriate.
        """
        if self.min_y <= self._y <= self.max_y:
            return self._y
        else:
            if self._y > self.max_y:
                self._y = self.max_y
            if self._y < self.min_y:
                self._y = self.min_y

            return self._y

    @y.setter
    def y(self, value: int) -> None:
        if self.min_y <= value <= self.max_y:
            self._y = value
        else:
            if value > self.max_y:
                self._y = self.max_y
            if value < self.min_y:
                self._y = self.min_y
