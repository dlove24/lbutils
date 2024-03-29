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
"""Do nothing 'implementation of the Python Abstract Base class.

Used to avoid import errors, and taken from the
[pcopy-lib](https://github.com/pfalcon/pycopy-lib/tree/master/abc) library.
"""

# Import the typing hints if available. Use our backup version
# if the official library is missing
try:
    from typing import Any
except ImportError:
    from lbutils.std.typing import Any


class ABCMeta:
    pass


class ABC:
    pass


def abstractmethod(f: Any) -> Any:
    return f
