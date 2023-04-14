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

"""Utilities and SPI Drivers for the Digilent Peripheral Modules. This library
is designed to provide drivers and support for the [Digilent peripheral
modules](https://digilent.com/reference/pmod/start). Not all boards are
supported: this module also only supports those with a dedicated SPI interface.

## SPI Conventions

!!! note "Modern SPI Name in Use"
     For this module, and all SPI references in the library, the [modern SPI
     names](https://www.oshwa.org/a-resolution-to-redefine-spi-signal-names/) are in
     use. However, most  of the PMod reference documentation (and the underlying
     hardware devices) still use the older terms.

![Modern Naming Conventions for the SPI Interfaces](docs/media/spi_interfaces.png)

**Figure 1: Modern Naming Conventions for the SPI Interfaces [CC0 – Public Domain]**

In general each module will require a minimum of four pins for the SPI
interface, as shown in Figure 1. For the SPI modes in the [PMod Interface
Specification Version
1.2.0](https://digilent.com/reference/_media/reference/pmod/pmod-interface-
specification-1_2_0.pdf) at least two pins are additionally required for +3.3V
(Pins 6 and 12) and 0V (Pin 5 and 11). This means that for most PMods using the
12-pin SPI jumper interface, the following basic pattern will hold (numbers
refer to the default GPIO pin assignment for the Pico H/W on the Leeds Beckett
micro-controller development board)

![PMod J1 Header Layout](https://digilent.com/reference/_media/reference/pmod/pmod-pinout-2x6.png)

|        | Pin Name      | Number       | Description                         |
|--------|---------------|--------------|-------------------------------------|
| Pin 1  | CS            |              | SPI Chip Select                     |
| Pin 2  | SDO           |              | SPI Serial Data Out                 |
| Pin 3  | SDI           |              | SPI Serial Data In                  |
| Pin 4  | SCK           |              | SPI Serial Clock                    |
| Pin 5  | GND           |              | Ground                              |
| Pin 6  | VCC           |              | VCC (+3.3V)                         |
| Pin 7  |               |              |                                     |
| Pin 8  |               |              |                                     |
| Pin 9  |               |              |                                     |
| Pin 10 |               |              |                                     |
| Pin 11 | GND           |              | Ground                              |
| Pin 12 | VCC           |              | VCC (+3.3V)                         |

Examples for specific pin interfaces for individual modules can be found in the
'`examples`' folder:
or [in the documentation](https://lbutils.readthedocs.io/en/latest/) for each
class below.
"""

### Expose the `pmod.spi` module interface as a full package
__all__ = ["olergb"]

from .oledrgb import OLEDrgb
