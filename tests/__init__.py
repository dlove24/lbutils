# This module, and all included code, is made available under the terms of the MIT Licence
#
# Copyright (c) 2022--2023 David Love
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
"""Test scripts for checking the library functionality. This module describes a
number of tests, designed to be run under the
[PyTest](https://docs.pytest.org/en/7.2.x/contents.html) harness. The standard
naming convention for the tests in the folder is

````python
test_<module_name>.py
````

All tests in this should also follow the standard PyTest rules for test
discovery so that running

```
$ py.test
```

will run all tests.

Each test is standalone, so that running

```
$ py.test test_colours.py
```

inside the `tests` folder should run the desired tests. Specific tests can also
be run programmaticaly through this module. Consult the PyTest documentation for
details.

Running the Tests
-----------------

These are principally unit, or module, level tests designed to exercise the
classes, methods and functions within them. In many cases a full test of these
modules requires specific hardware configurations: if this is the case then the
test will not be added to the standard test configuration.

Some limited support for hardware testing is provided though the [`FakePin`]
[lbutils.fake_pin] library. In other cases the detailed description of the
hardware required by the test is provided in the test description.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico W
"""