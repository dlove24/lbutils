# Seven Segment Display Drivers

Simple (decimal) numeric driver for a seven-segment display, requiring seven GPIO pins.

## Overview

During initialisation the user must supply a list of exactly seven GPIO pins,
using the numeric pin identifier (e.g. 16 for GPIO Pin 16). Each entry in the
list corresponds to the segment 'a' (for the first entry) to 'g' (for the last
entry). Physically, each LED segment is also assumed to be laid out in the
standard pattern, shown below. Once the constructor has been called, no further
changes are possible: and the driver will also assume exclusive use of the
relevant GPIO pins.

````
     - A -
   |       |
   F       B
   | - G - |
   E       C
   |       |
     - D -
````

**Figure 1: Assumed Layout of the Seven Segment Display**

To display a character, the `display` method of the class is used: passing in an
integer in the range 0..9 representing the number to show on the seven segment.
Not that by default the `display` method assumes that GPIO pins must be held
*low* for the segment to display: i.e. the behaviour normally used by common
anode seven-segment displays. If you need the requested GPIO pin to be held
*high* to display a segment, pass in `True` to the `inverted` parameter of the
`display` method.

!!! Note
    The drivers will only display characters in the specified range, and
    will raise a `ValueError` exception if the requested character is not in an
    appropriate range.

## Examples

### Examples Folder

* `seven_segment_example.py`
* `seven_segment_hex_example.py`

### WokWi

* [Seven Segment WokWi](https://wokwi.com/projects/360451068863047681)
* [Seven Hex Segment WokWi](https://wokwi.com/projects/360462223276690433)

## Tested Implementations

This version is written for MicroPython 3.4, and has been tested on:

* Raspberry Pi Pico H/W

## Classes

### `SegDisplay`

::: lbutils.drivers.SegDisplay

### `SegHexDisplay`

::: lbutils.drivers.SegHexDisplay
