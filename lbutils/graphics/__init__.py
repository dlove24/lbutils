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
Provides a simple graphics library for the supported screen devices
(controllers) of the Pico H and Pico W. Most of this interface provides abstract
base classes, which are then expected to be instantiated as sub-class of one of
the driver classes, e.g.
[`lbutils.pmods.spi.OLEDrgb`][lbutils.pmods.spi.OLEDrgb].

Note that font selection, and font representation is dealt with
[here][lbutils.graphics.fonts]. Other aspects of the library can be found in the
following sections

* **[Canvas and Drawing Primitives][lbutils.graphics.canvas]**. The core
`Canvas` class of the library, together with the drawing primitives implemented
by all graphics drivers.
* **[Colour Support and Representation][lbutils.graphics.colours]**. Classes such
as `Colour` which holds the internal colour representations used by the graphics
library. Also provides methods to convert beteween common colour formats
	and representations.
* **[Helper Classes][lbutils.graphics.helpers]**. Provides utility classes and
functions which ease the abstraction of the main graphics Canvas library, e.g.
`Pixel`.

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)

"""

### Expose the `graphics` module interface as a full package
from .colours import Colour
from .canvas import Canvas
from .helpers import Pen, Pixel, BoundPixel
