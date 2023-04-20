# LBUtils

## Background

This library is designed to install all of the common drivers, library code, and helper code used within modules at Leeds Beckett University. It is principally targeted at MicroPython on the Pico H/W micro-controllers: but compatibility is also maintained with CPython 3.10 where possible (or relevant).

Examples for how to use the library can be found in the '`examples`' folder: or [in the documentation](https://dlove24.github.io/lbutils/lbutils/examples/index.html). Otherwise the library is organised as follows

* **[`drivers`][lbutils.drivers]**: Classes aimed at low-level support of I2C, SPI
and other devices requiring board-level support.
* **[`graphics`][lbutils.graphics]**: Classes providing basic drawing and font support for display drivers.
* **[`helpers`][lbutils.helpers]**: Functions and classes which help replace boiler-plate code for tasks such as setting up network access.
* **[`pmods`][lbutils.pmods]**: Drivers and support for the
[Digilent peripheral modules](https://digilent.com/reference/pmod/start).

## Library Module and Package Layout

Many of the classes and functions provided by this library are split across multiple files, which are organised into [_modules_](https://docs.python.org/3/tutorial/modules.html) and [_packages_](https://docs.python.org/3/tutorial/modules.html#packages). In most cases the distinction between a module and a package in Python isn't that relevant: unless you are searching for the location of a specific class or method.

In most cases the packages will automatically export the classes of the contained modules: so the [`Colour`][lbutils.graphics.Colour] class, for instance, is available as both `lbutils.graphics.colours.Colour` and `lbutils.graphics.Colour`. The recommend `import` statement for this library is therefore

````python
from lbutils import graphics
from lbutils.graphics import colours, fonts
````

The module name is will be part of the `class` documentation, but in most cases the short form (using only the package name) is preferred.

To make the distinction between modules and packages easier to follow when navigating the documentation, the package documentation will distinguish between them as follows. Diagrams noting the core packages will denote those packages with a module name as a 'tag', as in the following package structure for the library

```puml
@startuml lbutils
namespace lbutils{
    namespace drivers {
    }
    namespace graphics {
        namespace fonts {
        }
    }
    namespace helpers {
    }
    namespace pmods {
        namespace i2c {
        }
        namespace spi {
        }
    }

}
@enduml
```

Modules within the packages will, by contrast, simply be drawn as a rounded rectangle; as in the following structure for the [`graphics`][lbutils.graphics] library

```puml
@startuml lbutils
namespace lbutils{
    namespace graphics {
        namespace fonts {
            namespace base_font <<Rectangle>> {
            }
            namespace font06 <<Rectangle>> {
            }
            namespace font08 <<Rectangle>> {
            }
            namespace org_01 <<Rectangle>> {
            }
        }
        namespace canvas <<Rectangle>> {
        }
        namespace colours <<Rectangle>> {
        }
        namespace helpers <<Rectangle>> {
        }
    }
}
@enduml
```

At a high-level, the overall structure of the classes into packages and modules in the library is therefore organised as follows

```puml
@startuml lbutils
namespace lbutils {
    namespace drivers {
        namespace seven_segment <<Rectangle>> {
            class SegDisplay {
                - list _char_list
                + display()
                }
        }
        namespace seven_segment_hex <<Rectangle>> {
            class SegHexDisplay {
                - list _char_list
                + display()
                }
        }
        namespace common <<Rectangle>> {
            enum PIN_ON_SENSE {
                + HIGH
                + LOW
            }
        }
    }
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
            +DEVICE_BIT_ORDER bitorder
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
    namespace helpers {
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

lbutils.drivers.seven_segment.SegDisplay <-- lbutils.drivers.common.PIN_ON_SENSE
lbutils.drivers.seven_segment_hex.SegHexDisplay <-- lbutils.drivers.common.PIN_ON_SENSE

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

## Installation

A package of this library is provided on PyPi as [`lbutils-mp`](https://pypi.org/project/lbutils-mp/). This can be installed with the normal Python tools, and should also install to boards running MicroPython under [Thonny](https://thonny.org/).

For manual installation, everything under the `lbutils` directory should be copied to the appropriate directory on the MicroPython board, usually `/lib`. The library, or individual drivers, can then be imported as normal: see the documentation for the [examples](https://lbutils.readthedocs.io/en/latest/examples) for more detailed guidance on the use of the library. This code is also available in the `examples` folder on [GitHub](https://github.com/dlove24/lbutils).

## Notes

- This library is principally a teaching library, so the [Documentation](https://lbutils.readthedocs.io) is be at least as important as the 'code'. Where possible all algorithms and implementation techniques are explained as fully as possible, or at least linked to reference standards/implementations

- All documentation is be organised according to the [Diátaxis](https://diataxis.fr/) framework: ideally with examples that do not require specific board set-ups. Where possible other sites such as [WokWi](https://wokwi.com) are used to give expanded examples that do not require installation.

- For consistency, all code is in the format standardised by the [Black](https://github.com/psf/black) library. The library is also fully typed, with accommodations made for the lack of a full type implementation on MicroPython.

- Documentation is generated by [MkDocs](https://www.mkdocs.org), using the embedded comments in the code. All documentation strings are in the [Markdown format accepted by MkDocs](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions), and are automatically rebuilt on commit. This also extends to class and other diagrams where possible.

## Known Implementations

- Raspberry Pi Pico W (MicroPython 3.4)
- CPython (3.10)
