# The MIT License (MIT)
#
# Copyright (c) 2014-2021 Paul Sokolovsky
# Copyright (c) 2014-2020 pycopy-lib contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""A 'fake' version of the `machine.Pin` library, used to allow some (very
limited) 'hardware' testing for the library code."""

###
### Classes
###

class FakePin:
    """A version of the `machine.Pin` class which **does not** write to any
    hardware, but instead reports the state back as a `pin_array`.

    This allows some visibility into the 'internal' state of the Pin for
    hardware testing. Common methods from the `Pin` library are also provided to
    make this class drop-in compatible.
    """

    ##
    ## Attributes
    ##

    pin_array: dict[int, bool]
    """Exposes the internal state of the hardware."""

    ##
    ## Constructor
    ##

    ##
    ## Methods
    ##
