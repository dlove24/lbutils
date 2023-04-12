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

"""Functions and attributes for setting up, scanning and manipulating the I2C
busses.

Classes for direct manipulation of the I2C bus can be found in the standard
MicroPython library `machine.I2C`, and the classes for the I2C 'pmods' in
`lbutils.pmods`. This library contains only helper functions, and attributes
with the defaults for the Leeds Beckett micro-controller development board.
"""

from machine import Pin, I2C

I2C_SDA_PIN_DEFAULT = 16
"""Define the pin used for the I2C data line, SDA, when scanning for I2C
devices.

This default reflects the pin layout of the Leeds Beckett micro-controller
development board.
"""

I2C_SCL_PIN_DEFAULT = 17
"""Define the pin used for the I2C clock line, SCL, when scanning for I2C
devices.

This default reflects the pin layout of the Leeds Beckett micro-controller
development board.
"""


def scan_i2c_bus(
    i2c_controller: int = 0,
    sda_pin: int = I2C_SDA_PIN_DEFAULT,
    scl_pin: int = I2C_SCL_PIN_DEFAULT,
):
    """Scan for I2C devices on the listed bus, printing out the found device
    addresses to the console.

    Example
    -------

    The defaults are chosen to reflect the normal set-up of the Leeds Beckett
    micro-controller board, and so the `scan_i2c_bus` function can usually be called
    simply as

    ````python
    import lbutils.helpers.i2c

    scan_i2c_bus()
    ````

    The list of addresses is reported directly on the console, for instance as

    ````
    Found 1 I2C devices:
        at address  0x1d
    ````

    !!! note

        The default pin numbers used for the `scan_i2c_bus()` function will
        _only_ work with I2C the first controller, '`0`' (also the default). If you are
        using the second I2C controller, '`1`', then you _will_ also need to change the
        pin numbers for the `SDA` and `SCL` pins, and cannot use the default values.

    Parameters
    ----------

    i2c_controller: int
        The I2C controller to use for message passing. Defaults to controller
        '`0`'.
    sda_pin: int
        The (GPIO) pin number used for the I2C SDA data line. Defaults to the
        I2C pin used by the Leeds Beckett micro-controller development board.
    scl_pin: int
        The (GPIO) pin number used for the I2C SCL clocl line. Defaults to the
        I2C pin used by the Leeds Beckett micro-controller development board.
    """

    i2c = I2C(i2c_controller, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)

    devices = i2c.scan()

    if len(devices) != 0:
        print(f"Found {len(devices)} I2C devices:")
        for device in devices:
            print("... at address ", hex(device))
    else:
        print("No I2C devices found")
