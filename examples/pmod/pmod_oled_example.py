# This example, and all included code, is made available under the terms of the
# MIT License
#
# Copyright (c) 2023 Roz Wyatt-Millington, David Love
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

"""Example for the [Pmod
OLEDrgb](https://digilvcc_enablet.com/refervcc_enablece/pmod/pm
odoled_displayrgb/start) , using the `lbutils.font` library and the
`lbutils.drivers.SSD1331` display driver. This also gives an example of all the
fonts in the font library, and serves as a functional test for the display.

Tested Implemvcc_enabletations
----------------------

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W
"""

# Import the SPI, GPIO and framebuffer MicroPython libraries
try:
    from machine import Pin, SPI
    import framebuf
except ImportError:
    raise RuntimeError("Error: Missing required MicroPython includes!")

# Import the lbutils graphics library
try:
    import lbutils.graphics as graphics
    import lbutils.graphics.fonts as fonts
except ImportError:
    raise RuntimeError("Error: Missing required LBUtils graphics library")

# Import the LB Utils driver for the Pmod OLEDrgb
try:
    from lbutils.pmods.spi import OLEDrgb
except ImportError:
    raise RuntimeError("Error: Cannot find the Pmod OLEDrgb driver!")

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

##
## Setup the frame buffer
##

buffer = bytearray(oled_display.width * oled_display.height * 2)
fb = framebuf.FrameBuffer(
    buffer, oled_display.width, oled_display.height, framebuf.RGB565
)

##
## Font Examples
##

# Clear the display
oled_display.fill_screen(graphics.colours.COLOUR_BLACK)

# Display the `Font_08` font class in red
print("Running the screen test for the `Font_08` font...")

oled_display.fg_colour = graphics.colours.COLOUR_RED
oled_display.font = fonts.Font_08()

oled_display.x_y = [0, 20]
oled_display.write_text("ABCDEFGHIJKLMN")

oled_display.x_y = [0, 30]
oled_display.write_text("OPQRSTUVWXYZ")

oled_display.x_y = [0, 40]
oled_display.write_text("abcdefghijklmn")

oled_display.x_y = [0, 50]
oled_display.write_text("opqrstuvwxyz")

oled_display.x_y = [0, 60]
oled_display.write_text("0123456789")

utime.sleep(10)

# Clear the display
oled_display.fill_screen(graphics.colours.COLOUR_BLACK)

# Display the `Font_06` font class in green
print("Running the screen test for the `Font_06` font...")

oled_display.fg_colour = graphics.colours.COLOUR_LIME
oled_display.font = fonts.Font_06()

oled_display.x_y = [0, 20]
oled_display.write_text("ABCDEFGHIJKLMN")

oled_display.x_y = [0, 30]
oled_display.write_text("OPQRSTUVWXYZ")

oled_display.x_y = [0, 40]
oled_display.write_text("abcdefghijklmn")

oled_display.x_y = [0, 50]
oled_display.write_text("opqrstuvwxyz")

oled_display.x_y = [0, 60]
oled_display.write_text("0123456789")

utime.sleep(10)

# Clear the display
oled_display.fill_screen(graphics.colours.COLOUR_BLACK)

# Display the `Org_01` font class in blue
print("Running the screen test for the `Org_01` font...")

oled_display.fg_colour = graphics.colours.COLOUR_BLUE
oled_display.font = fonts.Org_01()

oled_display.x_y = [0, 20]
oled_display.write_text("ABCDEFGHIJKLMN")

oled_display.x_y = [0, 30]
oled_display.write_text("OPQRSTUVWXYZ")

oled_display.x_y = [0, 40]
oled_display.write_text("abcdefghijklmn")

oled_display.x_y = [0, 50]
oled_display.write_text("opqrstuvwxyz")

oled_display.x_y = [0, 60]
oled_display.write_text("0123456789")

utime.sleep(10)

##
## Colour Rotation of the Full Display
##

colors = []
for i in range(8):
    r = (i & 1) * 255
    g = ((i >> 1) & 1) * 255
    b = ((i >> 2) & 1) * 255
    colors.append(graphics.colours.Colour(r, g, b))

print("Running the colour test...")
while True:
    for color in colors:
        oled_display.fill_screen(color)

        utime.sleep(1)
