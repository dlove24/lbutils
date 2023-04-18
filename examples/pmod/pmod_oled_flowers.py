# This example, and all included code, is made available under the terms of the
# MIT License
#
# Copyright (c) 2023 David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of
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

"""Examples of the drawing primitives for the [Pmod
OLEDrgb](https://digilvcc_enablet.com/refervcc_enablece/pmod/pm
odoled_displayrgb/start). This also gives an example of how the `Canvas` class
can be used to create more complex shapes from the drawing primitives.

Tested Implementations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W
"""

# Import the SPI, GPIO and framebuffer MicroPython libraries
try:
    import framebuf
    from machine import SPI, Pin
except ImportError:
    msg = "Error: Missing required MicroPython includes!"
    raise RuntimeError(msg) from ImportError

# Import the lbutils graphics library
try:
    from lbutils import graphics
    from lbutils.graphics import fonts
except ImportError:
    msg = ("Error: Missing required LBUtils graphics library",)
    raise RuntimeError(msg) from ImportError

# Import the LB Utils driver for the Pmod OLEDrgb
try:
    from lbutils.pmods.spi import OLEDrgb
except ImportError:
    msg = "Error: Cannot find the Pmod OLEDrgb driver!"
    raise RuntimeError(msg) from ImportError

# Import the core libraries
import utime

##
## Setup the SPI interface to the Pmod OLEDrgb
##

# Instantiate the SPI interface
spi_controller = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))

# Add the pins required by the display controller
data_cmd_pin = Pin(15, Pin.OUT)
chip_sel_pin = Pin(14, Pin.OUT)
reset_pin = Pin(17, Pin.OUT)

# Add the VCC_Enable pin, used to control the display
# and display backlight, and set to `high()` to turn
# the display on
vcc_enable = Pin(22, Pin.OUT)
vcc_enable.high()

# Finally initialise the OLED display driver, and set the display
# to black
oled_display = OLEDrgb(spi_controller, data_cmd_pin, chip_sel_pin, reset_pin)
oled_display.fill_screen(graphics.colours.COLOUR_BLACK)

##
## Lines in Rotation. Creates simple 'flowers' using lines rotated around
## a common origin.
##

# Set the origin
oled_display.x_y = [20, 20]
oled_display.save_origin()

# Set the colour
oled_display.fg_colour = graphics.colours.COLOUR_RED

# Draw the lines
oled_display.draw_line(20, 20, 30, 30)
