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
"""Provides a simple graphics library for the supported screen devices
(controllers) of the Pico H and Pico W. Most of this interface is provided
through a base class called [`Canvas`][lbutils.graphics.Canvas], which is
expected to be instantiated as sub-class of one of the driver classes, e.g.
[`lbutils.pmods.spi.OLEDrgb`][lbutils.pmods.spi.OLEDrgb]. The following
description therefore describes the methods and attributes common to all derived
drivers: but see the individual drivers for attributes and methods that may be
specific to the device in question.

### User and Library Cursors

The `Canvas` will maintain two internal drawing references

1. A [`cursor`]
[lbutils.graphics.Canvas.cursor], representing the current
[`x`][lbutils.graphics.Canvas.x] and [`y`][lbutils.graphics.Canvas.y]
drawing co-ordinates. This [`cursor`]
[lbutils.graphics.Canvas.cursor] should be assumed to be under the
control of the _library_ (`Canvas`). For instance, many of the drawing methods,
this internal state will be modified to point to the _next_ location which is
commonly used in sequence. For example the [`write_text`]
[lbutils.graphics.Canvas.write_text] updates the [`cursor`]
[lbutils.graphics.Canvas.cursor] to point to position at the end of the text
string. Or the [`draw_line`] [lbutils.graphics.Canvas.draw_line] method will
change the [`cursor`] [lbutils.graphics.Canvas.cursor] to the end of the
line just drawn. This behaviour makes it easier to sequence multiple drawing
methods: especially in the common case where a single origin is used to draw
multiple lines or other primitives in succession to create more complex shapes.
2. An [`origin`]
[lbutils.graphics.Canvas.origin], representing a reference point for
a sequence of drawing commands or drawing primitives. This [`origin`]
[lbutils.graphics.Canvas.origin] is assumed to be under the control of
the _user_, and will usually _not_ be modified by the internal drawing commands.
Instead an application can set the [`origin`]
[lbutils.graphics.Canvas.origin], then use the drawing primitives with the
addition of `from_origin` in the method name. Any internal change of state in
the [`cursor`]
[lbutils.graphics.Canvas.cursor] will not be reflected in a subsequent change
to the origin.

### Library Organisation and Helper Classes

The main aim of the `Canvas` class (and the graphics library generally is to
provide a basic set of capabilities which can be relied on by all users (and
higher-level libraries). Those common facilities can be divided into the
following categories, and are described in more detail in the following sections

* **[Colour Support and Representation][lbutils.graphics.colours]**. Classes
such as `Colour` which holds the internal colour representations used by the
graphics library. Also provides methods to convert between common colour formats
and representations, such as RGB565 and RGB588.
* **[Common Drawing Primitives][lbutils.graphics.Canvas]**. The drawing
primitives provided by the `Canvas` class of the library, such as circles,
rectangles and lines. These primitives are guaranteed to be available in all
graphics drivers: but depending on the driver may or may not be accelerated.
* **[Fonts and Font Handling][lbutils.graphics.fonts]**. Describes the internal
font representation used in this library, and the details of the fonts available
for use.
* **[Helper Classes][lbutils.graphics.helpers]**. Provides utility classes and
functions which ease the abstraction of the main graphics Canvas library, e.g.
[`Pixel`][lbutils.graphics.Pixel]. These are provided outside the main `Canvas`
class as being the most suitable classes for re-use in other drawing and graphics
routines.

Diagrammatically, the relationship between the  [`Canvas`]
[lbutils.graphics.Canvas] class and the helper classes listed above can be
shown as follows. Note that the [`fonts`][lbutils.graphics.fonts] package is
covered [separately][lbutils.graphics.fonts].

![Graphics Package Diagram](/media/lbutils_graphics.svg)

## Implementation

Much of the functionality of the [`Canvas`]
[lbutils.graphics.Canvas] class is provided by related
'helper' classes. Some of these helper classes such as [`Pen`]
[lbutils.graphics.Pen] or [`Colour`][lbutils.graphics.Colour] may be useful
more widely in graphics and drawing routines. Other helper classes such as
the [`BaseFont`][lbutils.graphics.fonts.BaseFont] are likely to be useful
only in the context of the `Canvas` class (and sub-classes).

The only methods _required_ to be implemented in sub-classes of [`Canvas`]
[lbutils.graphics.Canvas] are [`read_pixel`][lbutils.graphics.Canvas.read_pixel]
and [`write_pixel`][lbutils.graphics.Canvas.write_pixel]. All the drawing
primitives, including font support, can be implemented by `Canvas` using only
those two methods. However, in most cases the drawing speed is unacceptably slow,
and so in _most_ cases sub-classes will also choose to override methods such as
[`draw_line`][lbutils.graphics.Canvas.draw_line] where such facilities are
available. The details of the accelerated methods, including any changes to the
algorithms used by [`Canvas`][lbutils.graphics.Canvas] can be found in the
documentation for the sub-class itself.

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
"""

### Expose the `graphics` module interface as a full package
__all__ = ["colours", "canvas", "helpers"]

from .fonts.base_font import BaseFont

from .colours import DEVICE_WORD_ORDER, Colour
from .helpers import BoundPixel, Pen, Pixel
from .canvas import RECTANGLE_STYLE, Canvas, FrameBufferCanvas
