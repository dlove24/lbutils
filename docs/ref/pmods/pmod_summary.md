# Pmod Drivers

## Package Structure

The `lbutils.pmods` package provides drivers and support for the Digilent Peripheral Modules. This library is designed to provide drivers and support for the [Digilent peripheral modules](https://digilent.com/reference/pmod/start). Not all boards are supported: and in some cases only certain busses are supported (e.g. using only the I2C bus, even though the `pmod` supports both I2C and SPI).

These packages are organised into the following structure, with [`i2c`][lbutils.pmods.i2c] and [`spi`][SPI Drivers] documented separately in more detail.

```puml
@startuml lbutils
namespace lbutils {
    namespace graphics {
        namespace fonts {
            namespace base_font <<Rectangle>> {
                abstract class BaseFont {
                    - bitmap
                    - index
                    - glyph
                    {abstract} +int get_bit()
                    {abstract} +int get_next()
                    {abstract} +int set_position()
                }
            }
            namespace font06 <<Rectangle>> {
                class Font06 {
                    - bitmap
                    - index
                    - glyph
                    +int get_bit()
                    +int get_next()
                    +int set_position()
                }
            }
            namespace font08 <<Rectangle>> {
                class Font08{
                    - bitmap
                    - index
                    - glyph
                    +int get_bit()
                    +int get_next()
                    +int set_position()
                }
            }
            namespace org_01 <<Rectangle>> {
                class Org01{
                    - bitmap
                    - index
                    - glyph
                    +int get_bit()
                    +int get_next()
                    +int set_position()
                }
            }
        }
    namespace helpers <<Rectangle>> {
        class Pen {
            + bg_colour : Colour
            + fg_colour : Colour
            + thickness : int
            }
        class Pixel {
            + x : int
            + y : int
            + x_y : tuple
            +move_to()
            +offset()
            +offset_polar()
            }
        class BoundPixel {
            + min_x : int
            + min_y : int
            + max_x : int
            + max_y : int
            }
    }
    namespace colours <<Rectangle>> {
        class Colour {
            + red : int
            + green : int
            + blue : int
            + as_rgb565 : int
            + as_rgb888 : int
            +DEVICE_WORD_ORDER word_order
            {static} +from_rgb565()
        }
    }
    namespace canvas <<Rectangle>> {
        abstract class Canvas {
            + bg_colour : Colour
            + cursor : BoundPixel
            + fg_colour : Colour
            + origin : BoundPixel
            + pen : Pen
            + height : int
            + width : int
            + x : int
            + y : int
            + x_y : int
            + font : BaseFont
            {abstract} +draw_line()
            {abstract} +draw_rectangle()
            +draw_to()
            +fill_screen()
            +moveto()
            +move_origin_to()
            {abstract} +read_pixel()
            +select_bg_colour()
            +select_fg_colour()
            +write_char()
            {abstract} +write_pixel()
            +write_text()
            }
        }
    }
    namespace pmods {
        namespace i2c {
        }
        namespace spi {
            class OLEDrgb {
                - read()
                - write()
                + draw_line()
                + draw_rectangle()
                + read_pixel()
                + reset()
                + write_pixel()
                }
        }
    }
}

lbutils.graphics.fonts.font06.Font06 <|-- lbutils.graphics.fonts.base_font.BaseFont
lbutils.graphics.fonts.font08.Font08 <|-- lbutils.graphics.fonts.base_font.BaseFont
lbutils.graphics.fonts.org_01.Org01 <|-- lbutils.graphics.fonts.base_font.BaseFont

lbutils.graphics.helpers.Pen::bg_colour <-- lbutils.graphics.colours.Colour
lbutils.graphics.helpers.Pen::fg_colour <-- lbutils.graphics.colours.Colour

lbutils.graphics.helpers.BoundPixel <|-- lbutils.graphics.helpers.Pixel

lbutils.graphics.canvas.Canvas::bg_colour <-- lbutils.graphics.colours.Colour
lbutils.graphics.canvas.Canvas::fg_colour <-- lbutils.graphics.colours.Colour
lbutils.graphics.canvas.Canvas::cursor <-- lbutils.graphics.helpers.BoundPixel
lbutils.graphics.canvas.Canvas::origin <-- lbutils.graphics.helpers.BoundPixel
lbutils.graphics.canvas.Canvas::pen <-- lbutils.graphics.helpers.Pen
lbutils.graphics.canvas.Canvas::font <-- lbutils.graphics.fonts.base_font.BaseFont

lbutils.pmods.spi.OLEDrgb <|-- lbutils.graphics.canvas.Canvas

@enduml
```

## SPI Conventions

!!! note "Modern SPI Name in Use"
     For this module, and all SPI references in the library, the [modern SPI
     names](https://www.oshwa.org/a-resolution-to-redefine-spi-signal-names/) are in
     use. However, most  of the PMod reference documentation (and the underlying
     hardware devices) still use the older terms.

![Modern Naming Conventions for the SPI Interfaces](../../media/spi_interfaces.png)

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
| Pin 1  | CS            | 14           | SPI Chip Select                     |
| Pin 2  | SDO           | 19           | SPI Serial Data Out                 |
| Pin 3  | SDI           | 16           | SPI Serial Data In                  |
| Pin 4  | SCK           | 17           | SPI Serial Clock                    |
| Pin 5  | GND           | 3            | Ground                              |
| Pin 6  | VCC           | 5            | VCC (+3.3V)                         |
| Pin 7  |               |              |                                     |
| Pin 8  |               |              |                                     |
| Pin 9  |               |              |                                     |
| Pin 10 |               |              |                                     |
| Pin 11 | GND           | 3            | Ground                              |
| Pin 12 | VCC           | 5            | VCC (+3.3V)                         |

Examples for specific pin interfaces for individual modules can be found in the '`examples`' folder: or [in the documentation](https://lbutils.readthedocs.io/en/latest/) for each class below.

## Tested Implementations

This version is written for MicroPython 3.4, and has been tested on:

  * Raspberry Pi Pico H/W




