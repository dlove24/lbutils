# Seven Segment Display Drivers

## Summary

### Driver Classes

Simple numeric (decimal and hexademcimal) drivers for a single seven-segment
display, requiring seven GPIO pins. During initialisation the user must supply a
list of _exactly_ seven GPIO pins, using the numeric pin identifier (e.g. 16 for
GPIO Pin 16). Each entry in the list corresponds to the a single segment as
shown in Figure 1; with the first list entry referring to segment 'a', and the
last list entry to segment 'g'. Physically, each LED segment is also assumed to
be laid out in the standard pattern, shown below in Figure 1.

<figure markdown>
  ![Illustration of a Seven Segment Display](https://upload.wikimedia.org/wikipedia/commons/f/f3/Seven-segment_design_%2B_segments.svg){ width="150" }
  <figcaption><strong>Figure 1: Assumed Layout of the Seven Segment Display</strong></figcaption>
</figure>

!!! Warning

    Once the constructor has been called, no further changes to the pin entries
    are possible. If changes are required, the object must be destroyed, and then
    re-created from the class definition. Also note that the display driver will
    also assume exclusive use of the relevant GPIO pins whilst the driver object is
    in scope.

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

### Tested Implementations

This version is written for MicroPython 3.4, and has been tested on:

* Raspberry Pi Pico H/W

## Examples

### Examples Folder

* `examples/drivers/seven_segment_example.py`
* `examples/drivers/seven_segment_hex_example.py`

### WokWi

* [Seven Segment WokWi](https://wokwi.com/projects/360451068863047681)
* [Seven Hex Segment WokWi](https://wokwi.com/projects/360462223276690433)

::: lbutils.drivers.SegDisplay

::: lbutils.drivers.SegHexDisplay


