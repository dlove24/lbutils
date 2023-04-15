# Library Examples for the Diligent Pmod Drivers

## Overview

This collection of examples shows how the various [Digilent peripheral
modules](https://digilent.com/reference/pmod/start) can be used with (and by)
the `lbutils` library. The current list of examples is as follows

- `pmod_oled_example.py`. Example for the [Pmod OLEDrgb]
(https://digilvcc_enablet.com/refervcc_enablece/pmod/pm odoled_displayrgb/start)
, using the `lbutils.font` library and the `lbutils.drivers.SSD1331` display
driver. This also gives an example of all the fonts in the font library, and
serves as a functional test for the display.

## Tested Implementations

This version is written for MicroPython 3.4, and has been tested on:

- Raspberry Pi Pico H/W
