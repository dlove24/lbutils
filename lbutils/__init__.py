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

"""Utilities and Drivers for MicroPython used at Leeds Beckett University. The
library is organised into the following modules, which are designed to be stand-
alone.

* **[`drivers`][lbutils.drivers]**: Classes aimed at low-level support of I2C,
  SPI and other devices requiring board-level support.
* **[`fonts`][lbutils.graphics.fonts]**: Classes providing glyph and character
  support for display drivers.
* **[`helpers`][lbutils.helpers]**: Functions and classes which help replace
  boiler-plate code for tasks such as setting up network access.
* **[`pmod`][lbutils.pmods]**: Drivers and support for the
  [Digilent peripheral modules](https://digilent.com/reference/pmod/start).

Each module can be imported in its entirety to expose the individual drivers, for
instance as

````python
from lbutils.drivers import SegHexDisplay
````

In most cases the drivers are organised into 'sub-sets', e.g. those drivers
which deal with seven segment displays. These sub-sets are not exposed directly
as Python modules, but instead are for convenience to organise the library.
These sub-sets can be found linked in the side-bar under the '_Reference_' area.
In either case, see the individual module documentation for the specific classes
which the module exposes.

!!! Note
    In some cases loading the entire module into memory may not be a good idea, as
    some of the modules can consume significant memory resources. For production
    code it is better to import specific drivers directly, referencing the file
    the driver is contained in as

    ````python
    from lbutils.drivers.seven_segment import SegDisplay
    ````

## Known Implementations

*   Raspberry Pi Pico W (MicroPython 3.4)
*   CPython (3.10)
"""
