#
# Original Source: https://github.com/danjperron/ssd1331_micropython.git
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Daniel Perron; 2023, David Love
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Base class for the internal font representations. Based on the [Adafruit GFX
Arduino library](https://github.com/adafruit/Adafruit-GFX-Library.git),
converted by [Daniel
Perron](https://github.com/danjperron/ssd1331_micropython.git).

!!! note
    The character metrics used here (and produced by `fontconvert`) are slightly
    different from original Adafruit GFX & ftGFX tools. In the classic Adafruit
    GFX: the cursor position is the upper-left pixel of each 5x7 character;
    whilst the lower extent of most glyphs (except those w/descenders) is +6
    pixels in Y direction.

## Implementation

With this font representation, the cursor position is on baseline, where
baseline is 'inclusive' (containing the bottom-most row of pixels in most
symbols, except those with descenders; ftGFX is one pixel lower). The Y Cursor
will be moved automatically when switching between classic and new fonts.  If
you switch fonts, any print() calls will continue along the same baseline.

````
                    ...........#####.. -- yOffset
                    ..........######..
                    ..........######..
                    .........#######..
                    ........#########.
   * = Cursor pos.  ........#########.
                    .......##########.
                    ......#####..####.
                    ......#####..####.
       *.#..        .....#####...####.
       .#.#.        ....##############
       #...#        ...###############
       #...#        ...###############
       #####        ..#####......#####
       #...#        .#####.......#####
====== #...# ====== #*###.........#### ======= Baseline
                    || xOffset
````

The `glyph->xOffset` and `yOffset` are pixel offsets, in GFX coordinate space
(`+Y` is down), from the cursor position to the top-left pixel of the glyph
bitmap.  i.e. `yOffset` is typically negative, `xOffset` is typically zero but a
few glyphs will have other values (even negative `xOffsets` are allowed).  The
`glyph->xAdvance` is the distance to move the cursor on the X axis after drawing
the corresponding symbol. There's also some changes with regard to 'background'
color and new GFX fonts (classic fonts unchanged).  See the original
[Adafruit_GFX.cpp](https://github.com/adafruit/Adafruit-GFX-Library/blob/master/
Adafruit_GFX.cpp) for a more detailed explanation of how the glyphs are
reconstructed from the font data.
"""


class BaseFont:
    """A Base Class which implements the access methods required to use the
    individual font representations of the sub-classes. Those sub-classes
    provide only the _bitmap_ representation of the font: the reconstruction of
    that bitmap is handled here by `BaseFont`.

    Methods
    ----------

    * `get_bit()`. Returns the state ('0' or '1') of the bit specified by
    the current cursor `position` within the current glyph bitmap.

    * `get_next()`. Return the state of the current bit within the bitmap
    being displayed, and then advance the internal cursor to
    the next position: ready for the next call.

    * `set_position()`. Set the internal state to draw the glyph of the character
    in the next natural position.
    """

    def __init__(self, bitmap: list[bytes], index: list, glyph: list) -> None:
        """Take the byte array of `bitmap`s with the `index` of font characters
        and use these together with the `glyph` list to reconstruct the required
        font. This method is typically called by a sub-class in the constructor
        of the sub-class as in.

        ````python
        def __init__(self):
            super().__init__(self.bitmap, self.index, self.glyph)
        ````

        Parameters
        ----------

        bitmap: list[bytes]
            Calculated bit representations of glyph fragments. Used in
            reconstructing the specified glyphs.
        index: list
            Cross-references the UTF-8 characters to the list of glyphs specified
            in `glyph`. This provides the main mapping for character values to
            glyphs.
        glyph: list
            Specifies the bitmap sequence used to reconstruct a specific glyph.
            This provides the main definition of the core glphys from the
            original font definition.
        """

        self.bitmap = bitmap
        self.index = index
        self.glyph = glyph
        self.current_char = 0
        self.current_glyph = glyph[0]

    def set_position(self, utf8_char: str) -> None:
        """Set the internal state to draw the glyph of the character given in
        `utf8_char`. This internal state is not exposed to the calling method or
        function: but will be used in subsequent calls to
        [`get_bit`][lbutils.graphics.fonts.base_font.BaseFont.get_bit] or
        [`get_next`][lbutils.graphics.fonts.base_font.BaseFont.get_next].

        Parameters
        ----------

        utf8_char: str
            A single character string holding the character that
            will be drawn next from the internal glyph representation.
        """

        # Calculate the index into the glyph array, based on
        # the specified `utf_8` string. If the string cannot
        # be found, use the space (' ') string instead.
        #
        # Once found, set the `self.current_char` to the
        # required character value
        if utf8_char in self.index:
            self.current_char = self.index[utf8_char]
        else:
            self.current_char = self.index[" "]

        # Get the array of bitmaps corresponding to the
        # required character in `self.current_char`. Assign
        # this array to `self.current_glphy` for future use
        self.current_glyph = self.glyph[self.current_char]

        # Calculated the position of the next glyph, based
        # on the required character and the current glyph
        # bitmap array. Store in `self.position` for later
        # use
        self.position = self.current_glyph[0] * 8

    def get_bit(self, position: int) -> int:
        """Returns the state ('0' or '1') of the bit specified by the current
        cursor `position` within the current glyph bitmap.

        Parameters
        ----------

        position: int
            The position within the glyph bitmap to test for state


        Returns
        -------

        int
            Either '`0`' or '`1`' depending on the bitmap value
            of the current cursor position within the glyph.
        """

        c_offset = position // 8
        c_bit = 128 >> (position % 8)
        c_flag = (self.bitmap[c_offset] & c_bit) != 0

        return c_flag

    def get_next(self) -> int:
        """Return the state of the current bit within the bitmap being
        displayed, and then advance the internal cursor to the next position:
        ready for the next call.

        Returns
        -------

        int
            Either '`0`' or '`1`' depending on the bitmap value
            of the current cursor position within the glyph.
        """

        flag = self.get_bit(self.position)
        self.position = self.position + 1

        return flag
