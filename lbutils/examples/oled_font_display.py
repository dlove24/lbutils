from machine import Pin, SPI
from display import SSD1331 as SSD
import display.fonts.font08 as font08
import display.fonts.font06 as font06
import display.fonts.org_01 as org01
import framebuf

# import font12

import gc

from time import sleep
import utime

spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
dc = Pin(17, Pin.OUT)
cs = Pin(16, Pin.OUT)
rst = Pin(20, Pin.OUT)
oled = SSD(spi, dc, cs, rst)
oled.fill(0)

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

# oled.setFont(font12)
oled.setFont(font08.font08())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)
oled.fill(0)
oled.setFont(font06.font06())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)
oled.fill(0)
oled.setFont(org01.org_01())
oled.putText(0, 20, "ABCDEFGHIJKLMN", 0xFFFF)
oled.putText(0, 30, "OPQRSTUVWXYZ", 0xFFFF)
oled.putText(0, 40, "abcdefghijklmn", 0xFFFF)
oled.putText(0, 50, "opqrstuvwxyz", 0xFFFF)
oled.putText(0, 60, "0123456789", 0xFFFF)
utime.sleep(10)

while True:
    for color in colors:
        fb.fill(color)
        oled.block(0, 0, 96, 64, buffer)
        utime.sleep(1)
