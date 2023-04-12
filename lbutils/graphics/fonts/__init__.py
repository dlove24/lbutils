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

"""Fonts for the LED and OLED displays; especially the those using the 'pmod'
packages. These fonts are based on open-source font files, and converted with
the [`fontconvert`](https://github.com/danjperron/ssd1331_micropython) utility
written by Daniel Perron.S.

Most of the work of this library consists of rebuilding the font representation as
described below. This reconstruction is undertaken by the [`BaseFont`]
[lbutils.graphics.fonts.base_font.BaseFont] class, and abstract class which must
be sub-classed for a specific font. Currently the fonts (and subclasses) exposed
in this library are

  * [`Font06`][lbutils.graphics.fonts.font06.Font_06]. 6x6 pixel sans-serif font.
  * [`Font08`][lbutils.graphics.fonts.font08.Font_08]. 8x8 pixel sans-serif font.
  * [`Org_01`][lbutils.graphics.fonts.org_01.Org_01]. A tiny, stylized font with
  all characters within a 6 pixel height. Created by fontconvert, from the Org_v01
  by Orgdot.

## Rebuilding the Fonts

Rebuilding the fonts requires the [`fontconvert`](https://github.com/danjperron/ssd1331_micropython)
utility to be built in C **with** [the FreeType library] (https://freetype.org).
Once built the fonts can be converted using `fontconvert`
as

    ./fontconvert ~/Library/Fonts/FreeSans.ttf 18 > FreeSans18pt7b.py

Currently the `fontconvert` utility only extracts the printable 7-bit ASCII
characters of a font: for the exact character set extracted see the resulting
Python file.

## Tested Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)
"""

### Expose the `fonts` module interface as a full package
from .base_font import BaseFont

from .font06 import Font_06
from .font08 import Font_08
from .org_01 import Org_01
