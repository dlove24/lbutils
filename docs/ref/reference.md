# Guide to the API

::: lbutils
    options:
        heading_level: 2

::: lbutils.drivers
    options:
        heading_level: 2

Drivers for the display of a single digit

* [`SegDisplay`][lbutils.drivers.SegDisplay]. Display a single decimal digit, using seven GPIO pins.
* [`SegHexDisplay`][lbutils.drivers.SegHexDisplay]. Display a single hexadecimal digit, using seven GPIO pins.

::: lbutils.graphics.fonts
    options:
        heading_level: 2

### Classes

* [`PFx_Font`][lbutils.graphics.fonts.PFx_Font]. Base class, used  by the font display routines.
* [`Font06`][lbutils.graphics.fonts.font06]. Six Pixel bitmap font.
* [`Font08`][lbutils.graphics.fonts.font08]. Eight Pixel bitmap font.
* [`Org_01`][lbutils.graphics.fonts.org_01]. Alternative bitmap font.

::: lbutils.helpers
    options:
        heading_level: 2

### Functions

* [`scan_i2c_bus`][lbutils.helpers.i2c.scan_i2c_bus]. Scan for I2C devices on the listed bus, printing out the found device addresses to the console.
