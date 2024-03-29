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
"""Simple display driver for the [Pmod
OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/start), based on the
['ssd1331'](https://github.com/danjperron/pico_mpu6050_ssd1331) driver by Daniel
Perron. The [Pmod
OLEDrgb](https://digilent.com/reference/pmod/pmodoledrgb/start) provides an OLED
screen with a 96x64 pixel display capable of 16-bit RGB colour resolution.

This driver makes extensive use of the graphics facilities provided by the
[`Canvas`][lbutils.graphics.Canvas] class, and most of the functionality
provided here implements the low-level routines required by the
[`Canvas`][lbutils.graphics.Canvas]. For details of the methods and routines
used in the examples, and referred to below, see the documentation for the
[`Canvas`][lbutils.graphics.Canvas] class itself. The methods documented here
either provide low-level access to the underlying hardware for the
[`Canvas`][lbutils.graphics.Canvas] class, or accelerate some of the drawing
primitives using the features provided by the SSD1331 hardware.

!!! note

    Enabling the functionality of this module requires an extensive set-up
    routine detailed in the [official reference
    documentation](https:// digilent.com/reference/pmod/pmodoledrgb/reference-manual).
    In the normal use of this driver, the initialising command sequence is sent
    as part of the class construction. It therefore recommended to keep (or call)
    the constructor of this class in any sub-classes.

## Pin Layout

The table below shows the standard GPIO pin numbers for the Pico H/W on the the
Leeds Beckett micron-controller development board, using the standard PMod
header below.

![PMod J1 Header Layout](https://digilent.com/reference/_media/reference/pmod/pmod-pinout-2x6.png)

|        | Pin Name      | Number       | Description                         |
|--------|---------------|--------------|-------------------------------------|
| Pin 1  | CS            | 17           | SPI Chip Select                     |
| Pin 2  | SDO           | 19           | SPI Serial Data Out                 |
| Pin 3  | Not Connected | No Connection| Not Connected                       |
| Pin 4  | SCK           | 18           | SPI Serial Clock                    |
| Pin 5  | GND           | 3            | Ground                              |
| Pin 6  | VCC           | 5            | VCC (+3.3V)                         |
| Pin 7  | D/C           | 14           | Data/Commands. Display Data.        |
| Pin 8  | RES           | 15           | Reset the display controller        |
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

# Import the typing hints if available. Use our backup version
# if the official library is missing
try:
    from typing import Literal, Optional, Union
except ImportError:
    from lbutils.std.typing import Literal, Optional, Union  # type: ignore

# Import the lbutils graphics library
try:
    from lbutils import graphics
    from lbutils.graphics import colours
except ImportError:
    msg = ("Error: Missing required LBUtils graphics library",)
    raise RuntimeError(msg) from ImportError

# Import the core libraries
import ustruct
import utime

# Reference the MicroPython SPI and Pin library
from machine import SPI, Pin

# Allow the use of MicroPython constants
from micropython import const

##
## Display Commands. Internal list of the command code required by the SSD1331
## display driver. These are only used by the `OLEDrgb` class and are not part
## of the user-facing specification. See the
## [SSD1331 datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1331_1.2.pdf)
## for a detailed description of these commands
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
_PRECHARGEA = const(0x8A)
_PRECHARGEB = const(0x8B)
_PRECHARGEC = const(0x8C)
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
_PHASELENGTH = const(0xB1)
_CLOCKDIV = const(0xB3)
_PRECHARGELEVEL = const(0xBB)
_VCOMH = const(0xBE)
_LOCK = const(0xFD)

###
### Classes
###


class OLEDrgb(graphics.Canvas):
    """An implemention of a [`Canvas`][lbutils.graphics.Canvas] for the
    'OLEDrgb' PMod. This drawing support is provided through the following
    categories of tools.

    * **Drawing Primitives**: Provides basic support for drawing lines,
    rectangles, circles and triangles. This serves as a basic collection of
    primitives that can be relied upon by higher-level libraries.
    * **Font Support**: The `Canvas` maintains a record of the current font to
    use when writing text through the `font` attribute. This can be changed by
    users of the library, and defaults to [`Org01`]
    [lbutils.graphics.fonts.Org01].
    * **Colour Support**: Colours can be selected in different ways, and the
    `Canvas` maintains a foreground (`fg_colour`) and background (`bg_color`)
    attribute: along with a common method to override these default colours
    quickly for individual drawing commands. Colours are selected by order of
    precedence, which is defined as

        1. The `Colour`s directly specified in the method call of the drawing
        primitive.
        2. The colours specified by the `Pen` in the method call of the drawing
        primitive.
        3. The colours specified by the `Pen` of the `Canvas` object.
        4. The colours specified by as the default (forground or background)
        colour of the `Canvas` object.
        5. As a default of white (`COLOUR_WHITE`) for the foreground, and black
        (`COLOUR_BLACK`) if all other selection methods fail.

    Attributes
    ----------

    bg_colour: graphics.Colour
        The background [`Colour`][lbutils.graphics.colours.Colour] to use when
        drawing.
    cursor: graphics.BoundPixel
        The [`x`][lbutils.graphics.BoundPixel] and [`y`]
        [lbutils.graphics.BoundPixel] locations  of the current write
        (or read) operation.
    origin: graphics.BoundPixel
        The _user_ reference point for the next sequence of drawing primitives.
        This `origin` will not be altered by changes to the [`x`]
        [lbutils.graphics.BoundPixel] and [`y`]
        [lbutils.graphics.BoundPixel] locations of any drawing command.
    font: fonts.BaseFont
        The sub-class of [`BaseFont`][lbutils.graphics.fonts.base_font.BaseFont]
        to use when drawing characters.
    fg_colour: graphics.Colour
        The foreground [`Colour`][lbutils.graphics.colours.Colour] to use when
        drawing.
    pen: graphics.Pen
        The [`Pen`][lbutils.graphics.Pen] to use when drawing on the canvas.
    height: int
        A read-only value for the height of the canvas in pixels.
    width: int
        A read-only value for the width of the canvas in pixels.
    x: int
            The X co-ordinate value of the `cursor`
    y: int
            The Y co-ordinate value of the `cursor`
    x_y: int
            A tuple representing the co-ordinate (x ,y) of the `cursor`

    Methods
    -------

    **Cursor and Origin Movements**

    * `move_to()`. Move the internal [`cursor`]
    [lbutils.graphics.Canvas.cursor]  to the co-ordinate values (x, y) for
    the next sequence of drawing commands.

    * `move_origin_to()`. Sets the user drawing [`origin`]
    [lbutils.graphics.Canvas.origin] of the `Canvas` to the specified
    co-ordinates for the next sequence of drawing commands.

    **Colour Management**

    * `select_bg_colour()`. Return the colour to be used for drawing in the
    background, taking into account the (optional) overrides specified in
    `bg_color` and `pen`. The selected colour will obey the standard colour
    selection precedence of the `Canvas` class, and is guaranteed to return a
    valid [`Colour`][lbutils.graphics.colours.Colour] object.

    * `select_fg_colour()`. Return the colour to be used for drawing in the
    foreground, taking into account the (optional) overrides specified in `color`
    and `pen`. The selected colour will obey the standard colour selection
    precedence of the `Canvas` class, and is guaranteed to return a valid
    [`Colour`][lbutils.graphics.colours.Colour] object.

    **Shape and Line Drawing Primitives**

    * `draw_line()`. Draw a line from a specified point (by default the
    [`cursor`][lbutils.graphics.Canvas.cursor]) to a co-ordinate.

    * `draw_to()`. Draw a line from a specified point (by default the
    [`cursor`][lbutils.graphics.Canvas.cursor]) to a co-ordinate. Alias for
    [`draw_line()`][lbutils.graphics.Canvas.draw_line].

    * `draw_rectangle()`. Draw a rectangle at the co-ordinate (x, y) of height
    and width, using the specified colours for the frame of the rectangle and
    the interior fill colour (if any).

    * `fill_screen()`. Fill the entire `Canvas` with the background colour.

    **Font and Text Handling**

    * `write_char()`. Write a character (using the current font) starting at the
    specified co-ordinates (by default the current [`cursor`]
    [lbutils.graphics.Canvas.cursor] co-ordinates.), in the specified colour.

    * `write_text()`. Write the a string (using the current font) starting at the
    specified co-ordinates (by default the current [`cursor`]
    [lbutils.graphics.Canvas.cursor] co-ordinates.), in the specified colour.

    **Pixel Manipulation**

    * `read_pixel()`. Return the [`Colour`][lbutils.graphics.colours.Colour] of
    the specified pixel.

    * `write_pixel()`. Set the pixel at the specified position to the foreground
    colour value.
    """

    ##
    ## Private (Non-Public) Attributes
    ##

    # Command sequence used for the display initialisation

    _INIT = (
        (_LOCK, b"\x12"),  # Enable the driver IC to accept commands
        (_DISPLAYOFF, b""),  # Send the display off command
        (_SETREMAP, b"\x72"),  # Set the Remap to RGB Colour
        (_STARTLINE, b"\x00"),  # Set the Display start Line to the top line
        (_DISPLAYOFFSET, b"\x00"),  # Set the Display Offset to no vertical offset
        (_NORMALDISPLAY, b""),  # Make it a normal display
        (_SETMULTIPLEX, b"\x3f"),  # Set the Multiplex Ratio
        (_SETMASTER, b"\x8e"),  # Use a required external Vcc supply
        (_POWERMODE, b"\x0b"),  # Disable Power Saving Mode
        (_PHASELENGTH, b"\x31"),  # Set the Phase Length of the charge and discharge
        (
            _CLOCKDIV,
            b"\xf0",
        ),  # Set the Display Clock Divide Ratio and Oscillator Frequency
        (_PRECHARGEA, b"\x64"),  # Set the Second Pre-Charge Speed of Color A (Red)
        (_PRECHARGEB, b"\x78"),  # Set the Second Pre-Charge Speed of Color B (Green)
        (_PRECHARGEC, b"\x64"),  # Set the Second Pre-Charge Speed of Color C (Blue)
        (
            _PRECHARGELEVEL,
            b"\x3a",
        ),  # Set the Pre-Charge Voltage to approximately 45% of Vcc
        (_VCOMH, b"\x3e"),  # Set the VCOMH Deselect Level
        (_MASTERCURRENT, b"\x0c"),  # Set Master Current Attenuation Factor
        (_CONTRASTA, b"\x91"),  # Set the Contrast for Color A (Red)
        (_CONTRASTB, b"\x50"),  # Set the Contrast for Color B (Green)
        (_CONTRASTC, b"\x7d"),  # Set the Contrast for Color C (Blue)
        (_NO_SCROLL, b""),  # Disable Scrolling
    )

    #
    # Format strings used in byte packing structures
    #

    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">BB"
    _ENCODE_LINE = ">BBBBBBB"
    _ENCODE_RECT = ">BBBBBBBBBB"

    ##
    ## Public Attributes
    ##

    spi_controller: SPI
    data_cmd_pin = Pin
    chip_sel_pin = Pin
    reset_pin = Pin
    vcc_enable = Pin

    ##
    ## Constructors
    ##

    def __init__(
        self,
        spi_controller: SPI = SPI(0, 100000, mosi=Pin(19), sck=Pin(18)),
        data_cmd_pin: Pin = Pin(14, Pin.OUT),
        chip_sel_pin: Pin = Pin(17, Pin.OUT),
        reset_pin: Pin = Pin(15, Pin.OUT),
        vcc_enable: Pin = Pin(22, Pin.OUT),
        width: int = 96,
        height: int = 64,
    ) -> None:
        """Initialise the SPI interface, and sent the sequence of commands
        required for the device startup. The full command sequence is documented
        [here](https://digilent.com/reference/pmod/pmodoledrgb/reference-
        manual), and is recorded in the (private) `_INIT` array.

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

        A detailed example can be found in the `examples/pmods/
        pmod_oled_example.py` folder; which also includes details of the font
        set-up and selection. The example below covers the _set-up_ required by
        the display driver, and for use either consult the example or see the
        drawing methods provided by this class below.

        At a minimum, a client will need to
        instantiate an appropriate object from the
        [`machine.SPI`](https://docs.micropython.org/en/latest/library/machine.SPI.html)
        class

        ````python
        # Instantiate the SPI interface
        spi_controller = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
        ````

        The display driver also requires three control pins outside the
        SPI interface: the `data_cmd_pin`, `chip_sel_pin` and `reset_pin`.
        Select appropriate GPIO pins for the interface, and create
        appropriate objects from the
        [`machine.Pin`](https://docs.micropython.org/en/latest/library/machine.Pin.html)
        class

        ````python
        # Add the pins required by the display controller
        data_cmd_pin = Pin(15, Pin.OUT)
        chip_sel_pin = Pin(14, Pin.OUT)
        reset_pin = Pin(17, Pin.OUT)
        ````

        The display back-light, and the low-power mode of the display
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

        Parameters
        ----------
        spi_controller: SPI
            An instance of the
            [`machine.SPI`](https://docs.micropython.org/en/latest/library/machine.SPI.html)
            class, used to specify the SPI interface that should be used by this
            driver to interface to the display controller.
        data_cmd_pin: int, optional
            The '`D/C`' or 'Data/Command' pin; used to send low-level
            instructions to the display driver. Defaults to GPIO Pin 14.
        chip_sel_pin: int, optional
            SPI `CS` (Chip Select) pin. Defaults to GPIO Pin 15.
        reset_pin: int, optional
            Normally 'low': when held 'high', clears the current display buffer.
            Used to clear the display without having to rewrite each pixel.
            Defaults to GPIO Pin 17.
        vcc_enable:
            Used to control the display and the display back-light. Set to
            'high' to turn the display on, and 'low' to turn the display off.
        width: int, optional
            The width in pixels of the display. Defaults to 96.
        height: int, optional
            The height in pixels of the display. Defaults to 64.
        """

        # Set the ancestor values
        super().__init__(width, height)

        # Set the local attributes
        self.spi_controller = spi_controller
        self.data_cmd_pin = data_cmd_pin
        self.chip_sel_pin = chip_sel_pin
        self.reset_pin = reset_pin
        self.vcc_enable = vcc_enable

        # Initialise the display: see the OLED reference
        # for details of this step
        self.data_cmd_pin.value(0)
        self.reset_pin.value(1)
        self.vcc_enable.value(0)
        utime.sleep_ms(20)

        self.reset_pin.value(0)
        utime.sleep_ms(10)
        self.reset_pin.value(1)
        utime.sleep_ms(5)

        for command, data in self._INIT:
            self._write(command, data)

        self.vcc_enable.value(1)
        utime.sleep_ms(25)
        self._write(_DISPLAYON, b"")
        utime.sleep_ms(100)

    ##
    ## Private (Non-Public) Methods
    ##

    def _read(
        self,
        command: Optional[int] = None,
        count: Optional[int] = 0,
    ) -> int:
        """Decode a command read on the `data_cmd_pin` from the display
        driver."""
        self.data_cmd_pin.value(0)
        self.chip_sel_pin.value(0)

        if command is not None:
            self.spi_controller.write(bytearray([command]))
        if count:
            data = self.spi_controller.read(count)

        self.chip_sel_pin.value(1)

        return data

    def _write(
        self,
        command: Optional[int] = None,
        data: Optional[Union[bytes, bytearray]] = None,
    ) -> None:
        """Write a command over the `data_cmd_pin` to the display driver."""
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

    def _block(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        data: Union[bytes, bytearray],
    ) -> None:
        self._write(_SETCOLUMN, bytearray([x, x + width - 1]))
        self._write(_SETROW, bytearray([y, y + height - 1]))
        self._write(None, data)

    ##
    ## Methods
    ##

    def read_pixel(self, x: int, y: int) -> graphics.Colour:
        """Read the colour value of the pixel at position (`x`, `y`) and return
        to the caller.

        Parameters
        ----------

        x: int
            The x co-ordinate of the pixel to read
        y: int
            The y co-ordinate of the pixel to read

        Returns
        -------

        Colour:
             The [`Colour`][lbutils.graphics.Colour] representation of the pixel
             located at (x, y).
        """
        self._write(_SETCOLUMN, bytearray([x, x]))
        self._write(_SETROW, bytearray([y, y]))

        return graphics.Colour.from_565(self._read(None, 2))

    def write_pixel(self, x: int, y: int, colour: graphics.Colour) -> None:
        """Set the pixel at position (`x`, `y`) to the specified colour value.

        Parameters
        ----------

        x: int
             The X co-ordinate of the pixel to set.
        y: int
             The Y co-ordinate of the pixel to set.
        colour: Colour
             The [`Colour`][lbutils.graphics.Colour] representation of the pixel
             located at (x, y).
        """
        self._write(_SETCOLUMN, bytearray([x, x]))
        self._write(_SETROW, bytearray([y, y]))

        #          self._write(None,bytearray([colour >> 8, colour &0xff]))
        self.draw_line(start=(x, y), end=(x, y), fg_colour=colour)

    def draw_line(
        self,
        end: tuple[int, int],
        start: Optional[tuple[int, int]] = None,
        fg_colour: Optional[graphics.Colour] = None,
        pen: Optional[graphics.Pen] = None,
    ) -> None:
        """Draw a line from the current `cursor` co-ordinates or the co-ordinate
        specified in `start`, to the point given in the `end` co-ordinates and
        using the specified RGB colour. If the drawing colour is not specified
        in the arguments to this method, then it will use the preference order
        for the foreground colour of the `Canvas` Class to find a suitable
        colour. See [`select_fg_colour`]
        [lbutils.graphics.Canvas.select_fg_colour] for more details of the
        foreground colour selection algorithm.

        Example
        -------

        If the method is called with the `start` co-ordinate as `None` then the
        current value of the [`cursor`][lbutils.graphics.Canvas.cursor] will be
        used. However the `end` co-ordinate _must_ be specified. This means that
        in normal use the method can be called as

        ````python
        canvas.draw_line([0, 20])
        ````

        to draw a line from the current [`cursor`]
        [lbutils.graphics.Canvas.cursor] to the co-ordinate '(0, 20)'. This will
        also use the current `fg_colour` of the canvas when drawing the line.

        To change the line colour, either set the [`Pen`][lbutils.graphics.Pen],
        or call the method with the colour set directly as

        ````python
        canvas.draw_line([0, 20], fg_colour = lbutils.graphics.COLOUR_NAVY)
        ````

        The start of the line to be drawn can be changed using the `start`
        parameter: however in this case it is recommended to set _both_ the
        `start` and the `end` as named parameters, e.g.

        ````python
        canvas.draw_line(start = [0, 0], end = [0, 20])
        ````

        Using named parameter makes it much more obvious to readers of the
        library code which co-ordinates are being used to draw the line. Don't
        rely on the readers of the code remembering the positional arguments.

        Parameters
        ----------

        start: tuple
             The (x, y) co-ordinate of the _start_ point of the line, with
             the first value of the `tuple` representing the `x` co-ordinate and
             the second value of the `tuple` representing the `y` co-ordinate. If
             the `start` is `None`, the default, then the current value of the
             [`cursor`][lbutils.graphics.Canvas.cursor] is used as the start
             point of the line. Values beyond the first and second entries of
             the `tuple` are ignored.
        end: tuple
             The (x, y) co-ordinate of the pixel for the _end_ point of the line,
             with the first value of the tuple representing the `x` co-ordinate
             and the second value of the tuple representing the `y` co-ordinate.
             Values beyond the first and second entries of the `tuple` are
             ignored.
        fg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
             line. If not specified, use the preference order for the foreground
             colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
             The [`Pen`][lbutils.graphics.Pen] to be used when drawing the line.
             If not specified, use the preference order for the foreground colour
             of the `Canvas` to find a suitable colour.

        Raises
        ------

        ValueError:
            If the `start` or `end` tuples cannot be correctly interpreted as
            byte values; with the `x` co-ordinate as the first entry of the
            `tuple` and the `y` co-ordinate as the second entry of the tuple.
        """

        use_fg_colour = self.select_fg_colour(fg_colour=fg_colour, pen=pen)

        try:
            if start is None:
                data = ustruct.pack(
                    self._ENCODE_LINE,
                    self.cursor.x,
                    self.cursor.y,
                    end[0],
                    end[1],
                    use_fg_colour.red,
                    use_fg_colour.green,
                    use_fg_colour.blue,
                )
            else:
                data = ustruct.pack(
                    self._ENCODE_LINE,
                    start[0],
                    start[1],
                    end[0],
                    end[1],
                    use_fg_colour.red,
                    use_fg_colour.green,
                    use_fg_colour.blue,
                )
        except ustruct.error:
            msg = (
                "Invalid parameters has been passed to 'draw_line'. I cannot"
                "interpret the co-ordinates passed as arguments: check the"
                "'start' and 'end' tuples are correct",
            )
            raise ValueError(msg) from ustruct.error

        self._write(_DRAWLINE, data)

    def draw_rectangle(
        self,
        width: int,
        height: int,
        start: Optional[tuple[int, int]] = None,
        fg_colour: Optional[graphics.Colour] = None,
        bg_colour: Optional[graphics.Colour] = None,
        pen: Optional[graphics.Pen] = None,
        style: graphics.RECTANGLE_STYLE = graphics.RECTANGLE_STYLE.FILLED,
    ) -> None:
        """Draw a rectangle at the `start` co-ordinate, or the current cursor
        postion if `start` is `None`. In either case the rectangle will be drawn
        to the specified `height` and `width`, using the either the specified or
        `Canvas` `fg_colour` for the frame of the rectangle. If the `style` is
        `"FILLED"` then  either the specified `bg_colour` or `Canvas` `bg_color`
        as the interior colour. If the `style` is `"FRAMED"` then the interior
        of the rectangle is not drawn.

        See either [`select_fg_colour`]
        [lbutils.graphics.Canvas.select_fg_colour] for more details of the
        foreground colour selection algorithm; or [`select_bg_colour`]
        [lbutils.graphics.Canvas.select_bg_colour] for more details of the
        background colour selection algorithm. By default the rectangle is
        `"FILLED"` and so both the background and foreground colours are used.

        Parameters
        ----------

        start: tuple
             The (x, y) co-ordinate of the _start_ point of the rectangle, with
             the first value of the `tuple` representing the `x` co-ordinate and
             the second value of the `tuple` representing the `y` co-ordinate. If
             the `start` is `None`, the default, then the current value of the
             [`cursor`][lbutils.graphics.Canvas.cursor] is used as the start
             point of the rectangle. Values beyond the first and second entries
             of the `tuple` are ignored.
        width: int
             The width of the rectangle in pixels.
        height: int
             The hight of the rectangle in pixels.
        fg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when drawing the
             rectangle. If not specified, use the preference order for the
             foreground colour of the `Canvas` to find a suitable colour.
        bg_colour: Type[graphics.Colour], optional
             The [`Colour`][lbutils.graphics.Colour] to be used when filling the
             rectangle. If not specified, use the preference order for the
             background colour of the `Canvas` to find a suitable colour.
        pen: Type[graphics.Pen], optional
             The [`Pen`][lbutils.graphics.Pen] to be used when drawing the
             rectangle, using the forground colour for the frame and the
             background colour for the fill. If not specified, use the preference
             order for the foreground and background colours of the `Canvas` to
             find suitable colours.
        style: RECTANGLE_STYLE, optional
             Set the style for the rectangle to draw. The default style,
             `RECTANGLE_STYLE.FILLED`, sets the interior of the rectangle to the
             the current background colour.
        """

        use_fg_colour = self.select_fg_colour(fg_colour=fg_colour, pen=pen)
        use_bg_colour = self.select_bg_colour(bg_colour=bg_colour, pen=pen)

        # Send the commands to fill, or not fill, the rectangle
        if style == "FILLED":
            self._write(_FILL, b"\x01")
        else:
            self._write(_FILL, b"\x00")

        if start is None:
            # Send the drawing command (the colour data is ignored if the
            # rectangle is not filled)
            data = ustruct.pack(
                self._ENCODE_RECT,
                self.cursor.x,
                self.cursor.y,
                self.cursor.x + width - 1,
                self.cursor.y + height - 1,
                use_fg_colour.red,
                use_fg_colour.green,
                use_fg_colour.blue,
                use_bg_colour.red,
                use_bg_colour.green,
                use_bg_colour.blue,
            )
        else:
            # Send the drawing command (the colour data is ignored if the
            # rectangle is not filled)
            data = ustruct.pack(
                self._ENCODE_RECT,
                start[0],
                start[1],
                start[0] + width - 1,
                start[1] + height - 1,
                use_fg_colour.red,
                use_fg_colour.green,
                use_fg_colour.blue,
                use_bg_colour.red,
                use_bg_colour.green,
                use_bg_colour.blue,
            )

        self._write(_DRAWRECT, data)

    def reset(self) -> None:
        """Reset the display, clearing the current contents."""
        if self.reset_pin is not None:
            self.reset_pin.value(0)
            utime.sleep(0.1)
            self.reset_pin.value(1)
