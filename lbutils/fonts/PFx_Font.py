#
# Original Source: https://github.com/danjperron/ssd1331_micropython.git
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Daniel Perron
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

"""

Based on the [Adafruit GFX Arduino library](https://github.com/adafruit/Adafruit-GFX-Library.git), converted by [Daniel Perron](https://github.com/danjperron/ssd1331_micropython.git).

"""


class PFx_Font:
    def __init__(self, bitmap, index, glyph):
        self.bitmap = bitmap
        self.index = index
        self.glyph = glyph
        self.current_char = 0
        self.current_glyph = glyph[0]

    def setPosition(self, utf8_char):
        if utf8_char in self.index:
            self.current_char = self.index[utf8_char]
        else:
            self.current_char = self.index[" "]
        self.current_glyph = self.glyph[self.current_char]
        self.position = self.current_glyph[0] * 8

    def getBit(self, position):
        c_offset = position // 8
        c_bit = 128 >> (position % 8)
        c_flag = (self.bitmap[c_offset] & c_bit) != 0
        #       print("pos",position," off ",c_offset," bit ",c_bit," flag ",c_flag)
        return c_flag

    def getNext(self):
        #       print("Position ",self.position)
        flag = self.getBit(self.position)
        self.position = self.position + 1
        return flag
