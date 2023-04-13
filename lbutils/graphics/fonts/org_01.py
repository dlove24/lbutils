# MIT License
#
# Copyright (c) 2023 Roz Wyatt-Millington
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

from .base_font import BaseFont


class Org_01(BaseFont):
    """A tiny, stylized font with all characters within a 6 pixel height.

    Created by [`fontconvert`](https://github.com/danjperron/
    ssd1331_micropython.git), from the `Org_v01` by [Orgdot](
    https://www.orgdot.com/aliasfonts).
    """

    def __init__(self):
        super().__init__(self.bitmap, self.index, self.glyph)

    bitmap = bytes(
        [
            0xE8,
            0xA0,
            0x57,
            0xD5,
            0xF5,
            0x00,
            0xFD,
            0x3E,
            0x5F,
            0x80,
            0x88,
            0x88,
            0x88,
            0x80,
            0xF4,
            0xBF,
            0x2E,
            0x80,
            0x80,
            0x6A,
            0x40,
            0x95,
            0x80,
            0xAA,
            0x80,
            0x5D,
            0x00,
            0xC0,
            0xF0,
            0x80,
            0x08,
            0x88,
            0x88,
            0x00,
            0xFC,
            0x63,
            0x1F,
            0x80,
            0xF8,
            0xF8,
            0x7F,
            0x0F,
            0x80,
            0xF8,
            0x7E,
            0x1F,
            0x80,
            0x8C,
            0x7E,
            0x10,
            0x80,
            0xFC,
            0x3E,
            0x1F,
            0x80,
            0xFC,
            0x3F,
            0x1F,
            0x80,
            0xF8,
            0x42,
            0x10,
            0x80,
            0xFC,
            0x7F,
            0x1F,
            0x80,
            0xFC,
            0x7E,
            0x1F,
            0x80,
            0x90,
            0xB0,
            0x2A,
            0x22,
            0xF0,
            0xF0,
            0x88,
            0xA8,
            0xF8,
            0x4E,
            0x02,
            0x00,
            0xFD,
            0x6F,
            0x0F,
            0x80,
            0xFC,
            0x7F,
            0x18,
            0x80,
            0xF4,
            0x7D,
            0x1F,
            0x00,
            0xFC,
            0x21,
            0x0F,
            0x80,
            0xF4,
            0x63,
            0x1F,
            0x00,
            0xFC,
            0x3F,
            0x0F,
            0x80,
            0xFC,
            0x3F,
            0x08,
            0x00,
            0xFC,
            0x2F,
            0x1F,
            0x80,
            0x8C,
            0x7F,
            0x18,
            0x80,
            0xF9,
            0x08,
            0x4F,
            0x80,
            0x78,
            0x85,
            0x2F,
            0x80,
            0x8D,
            0xB1,
            0x68,
            0x80,
            0x84,
            0x21,
            0x0F,
            0x80,
            0xFD,
            0x6B,
            0x5A,
            0x80,
            0xFC,
            0x63,
            0x18,
            0x80,
            0xFC,
            0x63,
            0x1F,
            0x80,
            0xFC,
            0x7F,
            0x08,
            0x00,
            0xFC,
            0x63,
            0x3F,
            0x80,
            0xFC,
            0x7F,
            0x29,
            0x00,
            0xFC,
            0x3E,
            0x1F,
            0x80,
            0xF9,
            0x08,
            0x42,
            0x00,
            0x8C,
            0x63,
            0x1F,
            0x80,
            0x8C,
            0x62,
            0xA2,
            0x00,
            0xAD,
            0x6B,
            0x5F,
            0x80,
            0x8A,
            0x88,
            0xA8,
            0x80,
            0x8C,
            0x54,
            0x42,
            0x00,
            0xF8,
            0x7F,
            0x0F,
            0x80,
            0xEA,
            0xC0,
            0x82,
            0x08,
            0x20,
            0x80,
            0xD5,
            0xC0,
            0x54,
            0xF8,
            0x80,
            0xF1,
            0xFF,
            0x8F,
            0x99,
            0xF0,
            0xF8,
            0x8F,
            0x1F,
            0x99,
            0xF0,
            0xFF,
            0x8F,
            0x6B,
            0xA4,
            0xF9,
            0x9F,
            0x10,
            0x8F,
            0x99,
            0x90,
            0xF0,
            0x55,
            0xC0,
            0x8A,
            0xF9,
            0x90,
            0xF8,
            0xFD,
            0x63,
            0x10,
            0xF9,
            0x99,
            0xF9,
            0x9F,
            0xF9,
            0x9F,
            0x80,
            0xF9,
            0x9F,
            0x20,
            0xF8,
            0x88,
            0x47,
            0x1F,
            0x27,
            0xC8,
            0x42,
            0x00,
            0x99,
            0x9F,
            0x99,
            0x97,
            0x8C,
            0x6B,
            0xF0,
            0x96,
            0x69,
            0x99,
            0x9F,
            0x10,
            0x2E,
            0x8F,
            0x2B,
            0x22,
            0xF8,
            0x89,
            0xA8,
            0x0F,
            0xE0,
        ]
    )

    index = {
        " ": 0,
        "!": 1,
        '"': 2,
        "#": 3,
        "$": 4,
        "%": 5,
        "&": 6,
        "'": 7,
        "(": 8,
        ")": 9,
        "*": 10,
        "+": 11,
        ",": 12,
        "-": 13,
        ".": 14,
        "/": 15,
        "0": 16,
        "1": 17,
        "2": 18,
        "3": 19,
        "4": 20,
        "5": 21,
        "6": 22,
        "7": 23,
        "8": 24,
        "9": 25,
        ":": 26,
        ";": 27,
        "<": 28,
        "=": 29,
        ">": 30,
        "?": 31,
        "@": 32,
        "A": 33,
        "B": 34,
        "C": 35,
        "D": 36,
        "E": 37,
        "F": 38,
        "G": 39,
        "H": 40,
        "I": 41,
        "J": 42,
        "K": 43,
        "L": 44,
        "M": 45,
        "N": 46,
        "O": 47,
        "P": 48,
        "Q": 49,
        "R": 50,
        "S": 51,
        "T": 52,
        "U": 53,
        "V": 54,
        "W": 55,
        "X": 56,
        "Y": 57,
        "Z": 58,
        "[": 59,
        "\\": 60,
        "]": 61,
        "^": 62,
        "_": 63,
        "`": 64,
        "a": 65,
        "b": 66,
        "c": 67,
        "d": 68,
        "e": 69,
        "f": 70,
        "g": 71,
        "h": 72,
        "i": 73,
        "j": 74,
        "k": 75,
        "l": 76,
        "m": 77,
        "n": 78,
        "o": 79,
        "p": 80,
        "q": 81,
        "r": 82,
        "s": 83,
        "t": 84,
        "u": 85,
        "v": 86,
        "w": 87,
        "x": 88,
        "y": 89,
        "z": 90,
        "{": 91,
        "|": 92,
        "}": 93,
        "~": 94,
    }

    glyph = [
        [0, 0, 0, 6, 0, 1],  # 0x20 ' '
        [0, 1, 5, 2, 0, -4],  # 0x21 '!'
        [1, 3, 1, 4, 0, -4],  # 0x22 '"'
        [2, 5, 5, 6, 0, -4],  # 0x23 '#'
        [6, 5, 5, 6, 0, -4],  # 0x24 '$'
        [10, 5, 5, 6, 0, -4],  # 0x25 '%'
        [14, 5, 5, 6, 0, -4],  # 0x26 '&'
        [18, 1, 1, 2, 0, -4],  # 0x27 '''
        [19, 2, 5, 3, 0, -4],  # 0x28 '('
        [21, 2, 5, 3, 0, -4],  # 0x29 ')'
        [23, 3, 3, 4, 0, -3],  # 0x2A '*'
        [25, 3, 3, 4, 0, -3],  # 0x2B '+'
        [27, 1, 2, 2, 0, 0],  # 0x2C ','
        [28, 4, 1, 5, 0, -2],  # 0x2D '-'
        [29, 1, 1, 2, 0, 0],  # 0x2E '.'
        [30, 5, 5, 6, 0, -4],  # 0x2F '/'
        [34, 5, 5, 6, 0, -4],  # 0x30 '0'
        [38, 1, 5, 2, 0, -4],  # 0x31 '1'
        [39, 5, 5, 6, 0, -4],  # 0x32 '2'
        [43, 5, 5, 6, 0, -4],  # 0x33 '3'
        [47, 5, 5, 6, 0, -4],  # 0x34 '4'
        [51, 5, 5, 6, 0, -4],  # 0x35 '5'
        [55, 5, 5, 6, 0, -4],  # 0x36 '6'
        [59, 5, 5, 6, 0, -4],  # 0x37 '7'
        [63, 5, 5, 6, 0, -4],  # 0x38 '8'
        [67, 5, 5, 6, 0, -4],  # 0x39 '9'
        [71, 1, 4, 2, 0, -3],  # 0x3A ':'
        [72, 1, 4, 2, 0, -3],  # 0x3B ';'
        [73, 3, 5, 4, 0, -4],  # 0x3C '<'
        [75, 4, 3, 5, 0, -3],  # 0x3D '='
        [77, 3, 5, 4, 0, -4],  # 0x3E '>'
        [79, 5, 5, 6, 0, -4],  # 0x3F '?'
        [83, 5, 5, 6, 0, -4],  # 0x40 '@'
        [87, 5, 5, 6, 0, -4],  # 0x41 'A'
        [91, 5, 5, 6, 0, -4],  # 0x42 'B'
        [95, 5, 5, 6, 0, -4],  # 0x43 'C'
        [99, 5, 5, 6, 0, -4],  # 0x44 'D'
        [103, 5, 5, 6, 0, -4],  # 0x45 'E'
        [107, 5, 5, 6, 0, -4],  # 0x46 'F'
        [111, 5, 5, 6, 0, -4],  # 0x47 'G'
        [115, 5, 5, 6, 0, -4],  # 0x48 'H'
        [119, 5, 5, 6, 0, -4],  # 0x49 'I'
        [123, 5, 5, 6, 0, -4],  # 0x4A 'J'
        [127, 5, 5, 6, 0, -4],  # 0x4B 'K'
        [131, 5, 5, 6, 0, -4],  # 0x4C 'L'
        [135, 5, 5, 6, 0, -4],  # 0x4D 'M'
        [139, 5, 5, 6, 0, -4],  # 0x4E 'N'
        [143, 5, 5, 6, 0, -4],  # 0x4F 'O'
        [147, 5, 5, 6, 0, -4],  # 0x50 'P'
        [151, 5, 5, 6, 0, -4],  # 0x51 'Q'
        [155, 5, 5, 6, 0, -4],  # 0x52 'R'
        [159, 5, 5, 6, 0, -4],  # 0x53 'S'
        [163, 5, 5, 6, 0, -4],  # 0x54 'T'
        [167, 5, 5, 6, 0, -4],  # 0x55 'U'
        [171, 5, 5, 6, 0, -4],  # 0x56 'V'
        [175, 5, 5, 6, 0, -4],  # 0x57 'W'
        [179, 5, 5, 6, 0, -4],  # 0x58 'X'
        [183, 5, 5, 6, 0, -4],  # 0x59 'Y'
        [187, 5, 5, 6, 0, -4],  # 0x5A 'Z'
        [191, 2, 5, 3, 0, -4],  # 0x5B '['
        [193, 5, 5, 6, 0, -4],  # 0x5C '\'
        [197, 2, 5, 3, 0, -4],  # 0x5D ']'
        [199, 3, 2, 4, 0, -4],  # 0x5E '^'
        [200, 5, 1, 6, 0, 1],  # 0x5F '_'
        [201, 1, 1, 2, 0, -4],  # 0x60 '`'
        [202, 4, 4, 5, 0, -3],  # 0x61 'a'
        [204, 4, 5, 5, 0, -4],  # 0x62 'b'
        [207, 4, 4, 5, 0, -3],  # 0x63 'c'
        [209, 4, 5, 5, 0, -4],  # 0x64 'd'
        [212, 4, 4, 5, 0, -3],  # 0x65 'e'
        [214, 3, 5, 4, 0, -4],  # 0x66 'f'
        [216, 4, 5, 5, 0, -3],  # 0x67 'g'
        [219, 4, 5, 5, 0, -4],  # 0x68 'h'
        [222, 1, 4, 2, 0, -3],  # 0x69 'i'
        [223, 2, 5, 3, 0, -3],  # 0x6A 'j'
        [225, 4, 5, 5, 0, -4],  # 0x6B 'k'
        [228, 1, 5, 2, 0, -4],  # 0x6C 'l'
        [229, 5, 4, 6, 0, -3],  # 0x6D 'm'
        [232, 4, 4, 5, 0, -3],  # 0x6E 'n'
        [234, 4, 4, 5, 0, -3],  # 0x6F 'o'
        [236, 4, 5, 5, 0, -3],  # 0x70 'p'
        [239, 4, 5, 5, 0, -3],  # 0x71 'q'
        [242, 4, 4, 5, 0, -3],  # 0x72 'r'
        [244, 4, 4, 5, 0, -3],  # 0x73 's'
        [246, 5, 5, 6, 0, -4],  # 0x74 't'
        [250, 4, 4, 5, 0, -3],  # 0x75 'u'
        [252, 4, 4, 5, 0, -3],  # 0x76 'v'
        [254, 5, 4, 6, 0, -3],  # 0x77 'w'
        [257, 4, 4, 5, 0, -3],  # 0x78 'x'
        [259, 4, 5, 5, 0, -3],  # 0x79 'y'
        [262, 4, 4, 5, 0, -3],  # 0x7A 'z'
        [264, 3, 5, 4, 0, -4],  # 0x7B '{'
        [266, 1, 5, 2, 0, -4],  # 0x7C '|'
        [267, 3, 5, 4, 0, -4],  # 0x7D '}'
        [269, 5, 3, 6, 0, -3],
    ]  # 0x7E '~'


# Approx. 4959 bytes
