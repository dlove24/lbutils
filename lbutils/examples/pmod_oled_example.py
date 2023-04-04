# This module, and all included code, is made available under the terms of the MIT Licence
#
# Copyright (c) 2023 Roz Wyatt-Millington, David Love
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

"""

Example for the [Pmod OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/start) , using the `lbutils.font` library and the `lbutils.drivers.SSD1331` display driver. This also gives an example of all the fonts in the font library, and serves as a functional test for the display.

Tested Implementations
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

# Import the LB Utils driver for the Pmod OLEDrgb
try:
    from lbutils.pmod.spi import OLEDrgb as SSD
except ImportError:
    raise RuntimeError("Error: Cannot find the Pmod OLEDrgb driver!")

# Import the lbutils fonts (and font handler)
try:
    import lbutils.fonts as fonts
except ImportError:
    raise RuntimeError("Error: Missing required font libraries")

# Import the core libraries
import gc

from time import sleep
import utime

##
## Setup the SPI interface to the Pmod OLEDrgb
##

spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
dc = Pin(15, Pin.OUT)
cs = Pin(14, Pin.OUT)
rst = Pin(17, Pin.OUT)
en = Pin(22, Pin.OUT)  # Connected VCCEN so can turn screen off
en.high()
oled = SSD(spi, dc, cs, rst)
oled.fill(0)

##
## Setup the frame buffer
##

buffer = bytearray(oled.width * oled.height * 2)
fb = framebuf.FrameBuffer(buffer, oled.width, oled.height, framebuf.RGB565)

# test frame buffer
white = oled.color565(255, 255, 255)
colors = []
for i in range(8):
    r = (i & 1) * 255
    g = ((i >> 1) & 1) * 255
    b = ((i >> 2) & 1) * 255
    colors.append(oled.color565(r, g, b))

##
## Font Examples
##

# Display the `Font_08` font class
print("Running the screen test for the `Font_08` font...")

oled.fill(0)
oled.setFont(fonts.Font_08())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)

# Display the `Font_06` font class
print("Running the screen test for the `Font_06` font...")

oled.fill(0)
oled.setFont(fonts.Font_06())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)

# Display the `Org_01` font class
print("Running the screen test for the `Org_01` font...")

oled.fill(0)
oled.setFont(fonts.Org_01())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)

# Display a full screen of rotating colours
print("Running the colour test...")
while True:
    for color in colors:
        fb.fill(color)
        oled.block(0, 0, 96, 64, buffer)
        utime.sleep(1)
