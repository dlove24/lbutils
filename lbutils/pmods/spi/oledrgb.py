# Copyright (c) 2021 Daniel Perron; 2023 David Love
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Simple display driver for the [Pmod
OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/start), based on the
['ssd1331'](https://github.com/danjperron/pico_mpu6050_ssd1331) driver by
Daniel Perron. The [Pmod
OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/start) provides an OLED
screen with a 96×64 pixel display capable of 16-bit RGB colour resolution.

!!! note

    Enabling the functionality of this module requires an extensive set-up
    routine detailed in the [official reference
    documentation](https://digilent.com/reference/pmod/pmodoledrgb/reference-manual)
    . In the normal use of this driver, the initialising command sequence is sent as
    part of the class construction. It therefore recommended to keep (or call) the
    constructor of this class in any sub-classes.

## Pin Layout

The table below shows the standard GPIO pin numbers for the Pico H/W on the the
Leeds Beckett micron-controller development board, using the standard PMod
header below.

![PMod J1 Header Layout](https://digilent.com/reference/_media/reference/pmod/pmod-pinout-2x6.png)

|        | Pin Name      | Number       | Description                         |
|--------|---------------|--------------|-------------------------------------|
| Pin 1  | CS            | 14           | SPI Chip Select                     |
| Pin 2  | SDO           | 19           | SPI Serial Data Out                 |
| Pin 3  | Not Connected | No Connection| Not Connected                       |
| Pin 4  | SCK           | 18           | SPI Serial Clock                    |
| Pin 5  | GND           | 3            | Ground                              |
| Pin 6  | VCC           | 5            | VCC (+3.3V)                         |
| Pin 7  | D/C           | 15           | Data/Commands. Display Data.        |
| Pin 8  | RES           | 17           | Reset the display controller        |
| Pin 9  | VCC_EN        | 22           | VCC Enable (Enable/Disable Display) |
| Pin 10 | PMODEN        | No Connection| Power Supply to GND. Low-Power Mode |
| Pin 11 | GND           | 3            | Ground                              |
| Pin 12 | VCC           | 5            | VCC (+3.3V)                         |

## Examples

  * Set-up, font display and rotating colours: `examples/pmods/pmod_oled_example.py`

## References

* **Reference Manual:**
[OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/reference-manual)
* **Primary IC:**
[ssd1331](https://cdn-shop.adafruit.com/datasheets/SSD1331_1.2.pdf)

"""

# Import the typing hints if available
try:
    from typing import Type
except ImportError:
    print("Cannot find the type library")

# Import the core libraries
import ustruct
import utime

# Allow the use of MicroPython constants
from micropython import const

##
## Display Commands. Internal list of the command code required by the SSD1331
## display driver. These are only used by the `OLEDrgb` class and are not part
## of the user-facing specification. See the [SSD1331 datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1331_1.2.pdf) for a detailed description of
## these commands
##

_DRAWLINE = const(0x21)
_DRAWRECT = const(0x22)
_NO_SCROLL = const(0x2E)
_FILL = const(0x26)
_PHASEPERIOD = const(0x12)
_SETCOLUMN = const(0x15)
_SETROW = const(0x75)
_CONTRASTA = const(0x81)
_CONTRASTB = const(0x82)
_CONTRASTC = const(0x83)
_MASTERCURRENT = const(0x87)
_SETREMAP = const(0xA0)
_STARTLINE = const(0xA1)
_DISPLAYOFFSET = const(0xA2)
_NORMALDISPLAY = const(0xA4)
_DISPLAYALLON = const(0xA5)
_DISPLAYALLOFF = const(0xA6)
_INVERTDISPLAY = const(0xA7)
_SETMULTIPLEX = const(0xA8)
_SETMASTER = const(0xAD)
_DISPLAYOFF = const(0xAE)
_DISPLAYON = const(0xAF)
_POWERMODE = const(0xB0)
_PRECHARGE = const(0xB1)
_CLOCKDIV = const(0xB3)
_PRECHARGEA = const(0x8A)
_PRECHARGEB = const(0x8B)
_PRECHARGEC = const(0x8C)
_PRECHARGELEVEL = const(0xBB)
_VCOMH = const(0xBE)
_LOCK = const(0xFD)

###
### Classes
###


class OLEDrgb:
    _INIT = (
        (_DISPLAYOFF, b""),
        (_LOCK, b"\x0b"),
        (_SETREMAP, b"\x72"),  # RGB Colour
        (_STARTLINE, b"\x00"),
        (_DISPLAYOFFSET, b"\x00"),
        (_NORMALDISPLAY, b""),
        (_PHASEPERIOD, b"\x31"),
        (_SETMULTIPLEX, b"\x3f"),
        (_SETMASTER, b"\x8e"),
        (_POWERMODE, b"\x0b"),
        (_PRECHARGE, b"\x31"),  # ;//0x1F - 0x31
        (_CLOCKDIV, b"\xf0"),
        (_VCOMH, b"\x3e"),  # ;//0x3E - 0x3F
        (_MASTERCURRENT, b"\x0c"),  # ;//0x06 - 0x0F
        (_PRECHARGEA, b"\x64"),
        (_PRECHARGEB, b"\x78"),
        (_PRECHARGEC, b"\x64"),
        (_PRECHARGELEVEL, b"\x3a"),  # 0x3A - 0x00
        (_CONTRASTA, b"\x91"),  # //0xEF - 0x91
        (_CONTRASTB, b"\x50"),  # ;//0x11 - 0x50
        (_CONTRASTC, b"\x7d"),  # ;//0x48 - 0x7D
        (_NO_SCROLL, b""),
        (_DISPLAYON, b""),
    )

    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">BB"
    _ENCODE_LINE = ">BBBBBBB"
    _ENCODE_RECT = ">BBBBBBBBBB"

    ##
    ## Constructors
    ##

    def __init__(
        self,
        spi_controller,
        data_cmd_pin: int = 15,
        chip_sel_pin: int = 14,
        reset_pin: int = 17,
        width=96,
        height=64,
    ) -> None:
        """
        Initialise the SPI interface, and sent the sequence of commands required
        for the device startup. The full command sequence is documented
        [here](https://digilent.com/reference/pmod/pmodoledrgb/reference-manual), and is
        recorded in the (private) `_INIT` array.

        Client are not expected to modify the contents of the `INIT` array,
        but instead provide the details of specific devices in the `width`
        and `height` parameters. Both the `width` and the `height` are set
        to the defaults of the OLEDrgb Pmod: but this driver may be useful
        for other variations of the underlying display controller.

        !!! note "Parameter Defaults for Pico H/W Dev Board"
            The defaults for the constructor are chosen to reflect the
            normal usage for the Leeds Beckett micro-controller development
            boards. On other boards, and for other micro-controllers, these
            will need to be changed.

        Example
        -------

        A detailed example can be found in the `examples/pmods/pmod_oled_example.py` folder; which also includes details of the
        font set-up and selection. The example below covers the _set-up_
        required by the display driver, and for use either consult the
        example or see the drawing methods provided by this class below.

        At a minimum, a client will need to
        instantiate an appropriate object from the [`machine.SPI`](https://docs.micropython.org/en/latest/library/machine.SPI.html) class

        ````python
        # Instantiate the SPI interface
        spi_controller = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
        ````

        The display driver also requires three control pins outside the
        SPI interface: the `data_cmd_pin`, `chip_sel_pin` and `reset_pin`.
        Select appropriate GPIO pins for the interface, and create
        appropriate objects from the [`machine.Pin`](https://docs.micropython.org/en/latest/library/machine.Pin.html) class

        ````python
        # Add the pins required by the display controller
        data_cmd_pin = Pin(15, Pin.OUT)
        chip_sel_pin = Pin(14, Pin.OUT)
        reset_pin = Pin(17, Pin.OUT)
        ````

        The display backlight, and the low-power mode of the display
        driver, are controlled by a `vcc_enable` GPIO pin. In normal use
        this GPIO pin is set 'high': for low-power mode this pin should
        be set 'low'. During initialisation it is normal to set this pin
        high to turn the display on

        ````python
        # Add the VCC_Enable pin, used to control the display
        # and display backlight, and set to `high()` to turn
        # the display on
        vcc_enable = Pin(22, Pin.OUT)
        vcc_enable.high()
        ````

        Once the GPIO pins have been enabled, and set to the appropriate
        values, a object from the `OLEDrgb` can be instantiated to drive
        the display itself

        ````python
        # Finally initialise the OLED display driver, and set the display
        # to black
        oled_display = OLEDrgb(spi_controller, data_cmd_pin, chip_sel_pin, reset_pin)
        oled_display.fill(0
        ````

        Once a suitable object has been instantiated, the drawing methods
        provided by the rest of this class can be used.

        Attributes
        ----------

        font: Type[PFx_Font]
            The current font in use for the display, which will be
            an instance of [`lbutils.graphics.fonts.pfx_font`][lbutils.graphics.fonts.pfx_font.PFx_Font].
            All subsequent text methods (e.g. `write_text`) will make use of
            the specified `font` until this attribute is changed.


        Parameters
        ----------
        spi_controller: Type[SPI]
            An instance of the
            [`machine.SPI`](https://docs.micropython.org/en/latest/library/machine.SPI.html)
            class, used to specify the SPI interface that should be used by this driver to
            interface to the display controller.
        data_cmd_pin: int
            The '`D/C`' or 'Data/Command' pin; used to send low-level
            instructions to the display driver.
        chip_sel_pin: int
            SPI `CS` (Chip Select) pin.
        reset_pin: int = 17,
            Normally 'low': when held 'high', clears the current display buffer.
            Used to clear the display without having to rewrite each pixel.
        width=96
            The width in pixels of the display.
        height=64
            The height in pixels of the display.
        """

        self.spi_controller = spi_controller
        self.data_cmd_pin = data_cmd_pin
        self.chip_sel_pin = chip_sel_pin
        self.reset_pin = reset_pin
        self.width = width
        self.height = height
        self.reset()
        for command, data in self._INIT:
            self._write(command, data)
        self.font = None

    ##
    ## Private (Non-Public) Methods
    ##

    def _write(self, command=None, data=None):
        """
        Write a command over the `data_cmd_pin` to the display
        driver.
        """
        if command is None:
            self.data_cmd_pin.value(1)
        else:
            self.data_cmd_pin.value(0)

        self.chip_sel_pin.value(0)

        if command is not None:
            self.spi_controller.write(bytearray([command]))
        if data is not None:
            self.spi_controller.write(data)

        self.chip_sel_pin.value(1)

    def _read(self, command=None, count=0):
        """
        Decode a command read on the `data_cmd_pin` from the display
        driver.
        """

        self.data_cmd_pin.value(0)
        self.chip_sel_pin.value(0)

        if command is not None:
            self.spi_controller.write(bytearray([command]))
        if count:
            data = self.spi_controller.read(count)

        self.chip_sel_pin.value(1)

        return data

    ##
    ## Properties
    ##

    @property
    def font(self) -> None:
        return self._font

    @font.setter
    def font(self, font) -> None:
        if font is not None:
            self._font = font

    ##
    ## Methods
    ##

    def read_pixel(self, x: int, y: int) -> int:
        """
        Read the colour value of the pixel at position (`x`, `y`) and return to the caller.

        Returns
        -------

        int:
            The packaged byte representation of the colour at the pixel location
            (x, y).
        """
        self._write(_SETCOLUMN, bytearray([x, x]))
        self._write(_SETROW, bytearray([y, y]))

        return self._read(None, 2)

    def write_pixel(self, x: int, y: int, colour: int = 0) -> None:
        """
        Set the pixel at position (`x`, `y`) to the specified colour value.

        Parameters
        ----------

        x: int
            The X co-ordinate of the pixel to set.
        y: int
            The Y co-ordinate of the pixel to set.
        colour: int
            The packaged byte representation of the colour to be used
            when setting the pixel. Defaults to black.
        """
        self._write(_SETCOLUMN, bytearray([x, x]))
        self._write(_SETROW, bytearray([y, y]))

        #          self._write(None,bytearray([colour >> 8, colour &0xff]))
        self.draw_line(x, y, x, y, colour)

    def colour565(self, r: int, g: int, b: int) -> int:
        """
        Construct a packed byte representation of a colour value, from the
        three bytes `r` (red), `g` (green) and `b` (blue). The bottom five
        bytes of the three input variables are used, and on the ARM platform
        the packed byte representation looks like

        ````
        G2 G1 G0 B4 B3 B2 B1 B0 R4 R3 R2 R1 R0 G5 G4 G3
        ````

        Parameters
        ----------

        r:
            The red component of the packed byte value, of which the lower five bytes are selected.
        g:
            The green component of the packed byte value, of which the lower five bytes are selected.
        b:
            The red component of the packed byte value, of which the lower five bytes are selected.

        Returns
        -------

        int:
            A packed byte value of the colour representation.

        """
        #  5  4  3  2  1  0  9  8  7  6  5  4  3  2  1  0
        #  R4 R3 R2 R1 R0 G5 G4 G3 G2 G1 G0 B4 B3 B2 B1 B0
        # return  (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

        #  for ARM need  to swap byte
        #  G2 G1 G0 B4 B3 B2 B1 B0 R4 R3 R2 R1 R0 G5 G4 G3
        return (g & 0x1C) << 1 | (b >> 3) | (r & 0xF8) | g >> 5

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, colour: int) -> None:
        """
        Draw a line from co-ordinates (`x2`, `y2`) to (`x2`, `y2`) using the
        specified RGB colour. Use the [`color565`] method to construct a suitable RGB
        colour representation.

        Parameters
        ----------

        x1: int
            The X co-ordinate of the pixel for the start point of the line.
        y1: int
            The Y co-ordinate of the pixel for the start point of the line.
        x2: int
            The X co-ordinate of the pixel for the end point of the line.
        y2: int
            The Y co-ordinate of the pixel for the end point of the line.
        colour: int
            The packaged byte representation of the colour to be used
            when drawing the line.
        """
        r = (colour >> 10) & 0x3E
        g = (colour >> 5) & 0x3E
        b = (colour & 0x1F) << 1

        data = ustruct.pack(self._ENCODE_LINE, x1, y1, x2, y2, r, g, b)
        self._write(_DRAWLINE, data)

    def draw_rectangle(
        self, x: int, y: int, width: int, height: int, linecolour: int, fillcolour: int
    ) -> None:
        """
        Draw a rectangle at the co-ordinate (`x`, `y`) of `height` and `width`,
        using the `linecolour` for the frame of the rectangle and `fillcolour` as the
        interior colour.

        Parameters
        ----------

        x: int
            The X co-ordinate of the pixel for the start point of the rectangle.
        y: int
            The Y co-ordinate of the pixel for the start point of the rectangle.
        width: int
            The width of the rectangle in pixels.
        height: int
            The hight of the rectangle in pixels.
        linecolour: int
            The packaged byte representation of the colour to be used
            when drawing the frame of the rectangle.
        fillcolour: int
            The packaged byte representation of the colour to be used
            when the interior of the rectangle. May be `None` if no fill is
            to be used.
        """
        if fillcolour is None:
            self._write(_FILL, b"\x00")
            br = 0
            bg = 0
            bb = 0
        else:
            self._write(_FILL, b"\x01")
            br = (fillcolour >> 10) & 0x3E
            bg = (fillcolour >> 5) & 0x3E
            bb = (fillcolour & 0x1F) << 1

        r = (linecolour >> 10) & 0x3E
        g = (linecolour >> 5) & 0x3E
        b = (linecolour & 0x1F) << 1

        data = ustruct.pack(
            self._ENCODE_RECT, x, y, x + width - 1, y + height - 1, r, g, b, br, bg, bb
        )

        self._write(_DRAWRECT, data)

    def fill(self, colour: int = 0) -> None:
        """
        Fill the entire display with the specified colour. By default this
        will set the display to black, if no `colour` is specified.

        Parameters
        ----------

        colour: int
            The packaged byte representation of the colour to be used
            when the interior of the rectangle. Defaults to black.
        """
        self.draw_rectangle(0, 0, self.width, self.height, colour, colour)

    def block(self, x, y, width, height, data):
        self._write(_SETCOLUMN, bytearray([x, x + width - 1]))
        self._write(_SETROW, bytearray([y, y + height - 1]))
        self._write(None, data)

    def reset(self) -> None:
        """
        Resets the display, clearing the current contents.
        """
        if self.reset_pin is not None:
            self.reset_pin.value(0)
            utime.sleep(0.1)
            self.reset_pin.value(1)

    def write_char(self, x: int, y: int, utf8Char: str, colour: int) -> int:
        """
        Write a `utf8Char` character (using the current `font`) starting
        at the pixel position (`x`, `y`) in the specified `colour`.

        !!! note
            Whilst the `utf8Char` character _must_ be a valid UTF-8
            character, most fonts only support the equivalent of the (7-bit) ASCII character
            set. This method _will not_ display character values that cannot be supported by
            the underlying font. See the font description for the exact values that are
            valid for the specific font being used.

        Parameters
        ----------

        x: int
            The X co-ordinate of the pixel for the character start position.
        y: int
            The Y co-ordinate of the pixel for the character start position.
        utf8Char:
            The character to write to the display.
        colour: int
            The packaged byte representation of the colour to be used
            when drawing the character.

        Returns
        -------

        int:
            The X pixel co-ordinate immediately following the character written
            in the specified font. This can be used to easily locate multiple characters at
            a given Y position: see also `write_text()`.
        """

        # print("write_char(x={},y={},c={},colour={})".format(x,y,utf8Char,colour))
        if self.font is None:
            return x
        # {offset, width, height, advance cursor, x offset, y offset} */
        self.font.setPosition(utf8Char)
        _offset, _width, _height, _cursor, x_off, y_off = self.font.current_glyph
        # print("_offset",_offset)
        # print("Width",_width)
        # print("height",_height)
        # print("cursor",_cursor)
        # print("xoff",x_off)
        # print("yoff",y_off)
        for y1 in range(_height):
            for x1 in range(_width):
                if self.font.getNext():
                    self.write_pixel(x + x1 + x_off, y + y1 + y_off, colour)
        return x + _cursor

    def write_text(self, x: int, y: int, txt_str: str, colour: int) -> None:
        """
        Write the string `txt_str` (using the current `font`) starting
        at the pixel position (`x`, `y`) in the specified `colour` to
        the display.

        !!! note
            Whilst the `txt_str` character _must_ be a valid UTF-8
            string, most fonts only support the equivalent of the (7-bit) ASCII character
            set. This method _will not_ display character values that cannot be supported by
            the underlying font. See the font description for the exact values that are
            valid for the specific font being used.

        Parameters
        ----------

        x: int
            The X co-ordinate of the pixel for the text start position.
        y: int
            The Y co-ordinate of the pixel for the text start position.
        txt_str:
            The string of characters to write to the display.
        colour: int
            The packaged byte representation of the colour to be used
            when drawing the character.
        """
        if self.font is not None:
            for c in txt_str:
                x = self.write_char(x, y, c, colour)
