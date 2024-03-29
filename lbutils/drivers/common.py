# This module, and all included code, is made available under the terms of the
# MIT Licence
#
# Copyright (c) 2023 David Love
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
"""Common libraries and definitions for the for low-level devices. This module
contains mostly helper and other utility definitions that are used by more than
one driver. In most cases the services provided by this module are not meant to
be used directly by end-user code.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W
"""

# Import the enumerations library. Unfortunately the full version in not
# in MicroPython yet, so this is a bit of a hack
try:
    from enum import IntEnum
except ImportError:
    from urest.enum import IntEnum  # type: ignore

###
### Enumerations
###


class PIN_ON_SENSE(IntEnum):
    """Sets the device sense for 'ON'.

    When set to `HIGH` the GPIO pins need to be set 'high' ('1') for the device
    input to turn on. When set to `LOW` the GPIO pins need to be set 'low' ('0')
    for the device input to turn on.
    """

    LOW = 0
    HIGH = 1
