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


class Font_06(BaseFont):
    """6x6 pixel sans-serif font, created by
    [`fontconvert`](https://github.com/danjperron/ssd1331_micropython.git)."""

    def __init__(self):
        super().__init__(self.bitmap, self.index, self.glyph)

    bitmap = bytes(
        [
            0x00,
            0xD0,
            0xB4,
            0x6F,
            0xFA,
            0x5F,
            0x3E,
            0x80,
            0xCE,
            0x73,
            0x64,
            0xBF,
            0xC0,
            0x70,
            0x70,
            0xFC,
            0x5D,
            0x00,
            0xC0,
            0xC0,
            0x80,
            0x29,
            0x28,
            0x6D,
            0x96,
            0xC9,
            0x70,
            0xF0,
            0xD9,
            0xE0,
            0xF6,
            0x1F,
            0x26,
            0xF2,
            0xFF,
            0x1F,
            0x78,
            0xFF,
            0xF2,
            0x24,
            0xF6,
            0x9F,
            0xFF,
            0x1E,
            0xA0,
            0xB0,
            0x39,
            0x80,
            0xE3,
            0x80,
            0x8F,
            0x00,
            0xE1,
            0x69,
            0xB8,
            0x60,
            0x66,
            0x69,
            0xFE,
            0x9F,
            0x78,
            0x87,
            0xE9,
            0x9E,
            0xFF,
            0x8F,
            0xFF,
            0x88,
            0x7B,
            0x97,
            0x9F,
            0x99,
            0xE9,
            0x70,
            0xD7,
            0xAC,
            0xCA,
            0x88,
            0x8F,
            0x9F,
            0x99,
            0xDD,
            0xBB,
            0xF9,
            0x9F,
            0xF9,
            0xF8,
            0xF9,
            0x9E,
            0x10,
            0xF9,
            0xE9,
            0xFE,
            0x1F,
            0xE9,
            0x20,
            0x99,
            0x9F,
            0x96,
            0x66,
            0x9F,
            0xFA,
            0xF6,
            0x6F,
            0xA9,
            0x20,
            0xF2,
            0x6F,
            0xEA,
            0xC0,
            0x89,
            0x22,
            0xD5,
            0xC0,
            0x54,
            0xF0,
            0x80,
            0x79,
            0x70,
            0x88,
            0xE9,
            0xE0,
            0xF3,
            0x80,
            0x11,
            0xFD,
            0xF0,
            0xFF,
            0xF0,
            0x6B,
            0xA4,
            0xF9,
            0xFF,
            0x88,
            0xF9,
            0x90,
            0x43,
            0x2E,
            0x4D,
            0x70,
            0x84,
            0x2D,
            0x8A,
            0x00,
            0xC9,
            0x26,
            0xFD,
            0x6A,
            0x00,
            0xF9,
            0x90,
            0xF9,
            0xF0,
            0xF9,
            0xF8,
            0xF9,
            0xF1,
            0xE8,
            0xF7,
            0xF0,
            0x5D,
            0x30,
            0x99,
            0xF0,
            0x96,
            0x60,
            0xAD,
            0x54,
            0x00,
            0xE4,
            0xE0,
            0xB6,
            0x4C,
            0xFC,
            0xF0,
            0x6A,
            0x24,
            0xC0,
            0xFC,
            0xC8,
            0xA5,
            0x80,
            0x3E,
            0x00,
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
        [0, 1, 1, 5, 0, -1],  # 0x20 ' '
        [1, 1, 4, 5, 2, -4],  # 0x21 '!'
        [2, 3, 2, 5, 1, -4],  # 0x22 '"'
        [3, 4, 4, 5, 0, -4],  # 0x23 '#'
        [5, 3, 6, 5, 1, -5],  # 0x24 '$'
        [8, 4, 4, 5, 0, -4],  # 0x25 '%'
        [10, 4, 4, 5, 1, -4],  # 0x26 '&'
        [12, 1, 2, 5, 2, -4],  # 0x27 '''
        [13, 1, 5, 5, 1, -5],  # 0x28 '('
        [14, 1, 5, 5, 2, -5],  # 0x29 ')'
        [15, 3, 2, 5, 1, -4],  # 0x2A '*'
        [16, 3, 3, 5, 1, -4],  # 0x2B '+'
        [18, 1, 2, 5, 1, -1],  # 0x2C ','
        [19, 2, 1, 5, 1, -2],  # 0x2D '-'
        [20, 1, 1, 5, 1, -1],  # 0x2E '.'
        [21, 3, 5, 5, 0, -4],  # 0x2F '/'
        [23, 4, 4, 5, 1, -4],  # 0x30 '0'
        [25, 3, 4, 5, 1, -4],  # 0x31 '1'
        [27, 5, 4, 5, 1, -4],  # 0x32 '2'
        [30, 4, 4, 5, 1, -4],  # 0x33 '3'
        [32, 4, 4, 5, 1, -4],  # 0x34 '4'
        [34, 4, 4, 5, 1, -4],  # 0x35 '5'
        [36, 4, 4, 5, 1, -4],  # 0x36 '6'
        [38, 4, 4, 5, 1, -4],  # 0x37 '7'
        [40, 4, 4, 5, 1, -4],  # 0x38 '8'
        [42, 4, 4, 5, 1, -4],  # 0x39 '9'
        [44, 1, 3, 5, 1, -3],  # 0x3A ':'
        [45, 1, 4, 5, 1, -3],  # 0x3B ';'
        [46, 3, 3, 5, 1, -3],  # 0x3C '<'
        [48, 3, 3, 5, 0, -4],  # 0x3D '='
        [50, 3, 3, 5, 1, -3],  # 0x3E '>'
        [52, 2, 4, 5, 0, -4],  # 0x3F '?'
        [53, 4, 5, 5, 1, -4],  # 0x40 '@'
        [56, 4, 4, 5, 1, -4],  # 0x41 'A'
        [58, 4, 4, 5, 1, -4],  # 0x42 'B'
        [60, 4, 4, 5, 1, -4],  # 0x43 'C'
        [62, 4, 4, 5, 1, -4],  # 0x44 'D'
        [64, 4, 4, 5, 1, -4],  # 0x45 'E'
        [66, 4, 4, 5, 1, -4],  # 0x46 'F'
        [68, 4, 4, 5, 1, -4],  # 0x47 'G'
        [70, 4, 4, 5, 1, -4],  # 0x48 'H'
        [72, 3, 4, 5, 1, -4],  # 0x49 'I'
        [74, 2, 4, 5, 1, -4],  # 0x4A 'J'
        [75, 4, 4, 5, 1, -4],  # 0x4B 'K'
        [77, 4, 4, 5, 1, -4],  # 0x4C 'L'
        [79, 4, 4, 5, 1, -4],  # 0x4D 'M'
        [81, 4, 4, 5, 1, -4],  # 0x4E 'N'
        [83, 4, 4, 5, 1, -4],  # 0x4F 'O'
        [85, 4, 4, 5, 1, -4],  # 0x50 'P'
        [87, 4, 5, 5, 1, -4],  # 0x51 'Q'
        [90, 4, 4, 5, 1, -4],  # 0x52 'R'
        [92, 4, 4, 5, 1, -4],  # 0x53 'S'
        [94, 3, 4, 5, 1, -4],  # 0x54 'T'
        [96, 4, 4, 5, 1, -4],  # 0x55 'U'
        [98, 4, 4, 5, 1, -4],  # 0x56 'V'
        [100, 4, 4, 5, 0, -4],  # 0x57 'W'
        [102, 4, 4, 5, 1, -4],  # 0x58 'X'
        [104, 3, 4, 5, 1, -4],  # 0x59 'Y'
        [106, 4, 4, 5, 1, -4],  # 0x5A 'Z'
        [108, 2, 5, 5, 1, -5],  # 0x5B '['
        [110, 3, 5, 5, 0, -4],  # 0x5C '\'
        [112, 2, 5, 5, 1, -5],  # 0x5D ']'
        [114, 3, 2, 5, 0, -4],  # 0x5E '^'
        [115, 4, 1, 5, 0, 0],  # 0x5F '_'
        [116, 1, 1, 5, 1, -5],  # 0x60 '`'
        [117, 4, 3, 5, 0, -3],  # 0x61 'a'
        [119, 4, 5, 5, 0, -5],  # 0x62 'b'
        [122, 3, 3, 5, 0, -3],  # 0x63 'c'
        [124, 4, 5, 5, 0, -5],  # 0x64 'd'
        [127, 4, 3, 5, 0, -3],  # 0x65 'e'
        [129, 3, 5, 5, 0, -5],  # 0x66 'f'
        [131, 4, 4, 5, 0, -3],  # 0x67 'g'
        [133, 4, 5, 5, 0, -5],  # 0x68 'h'
        [136, 3, 5, 5, 1, -5],  # 0x69 'i'
        [138, 2, 6, 5, 1, -5],  # 0x6A 'j'
        [140, 5, 5, 5, 0, -5],  # 0x6B 'k'
        [144, 3, 5, 5, 0, -5],  # 0x6C 'l'
        [146, 5, 3, 5, 0, -3],  # 0x6D 'm'
        [149, 4, 3, 5, 0, -3],  # 0x6E 'n'
        [151, 4, 3, 5, 0, -3],  # 0x6F 'o'
        [153, 4, 4, 5, 0, -3],  # 0x70 'p'
        [155, 4, 4, 5, 0, -3],  # 0x71 'q'
        [157, 2, 3, 5, 1, -3],  # 0x72 'r'
        [158, 4, 3, 5, 0, -3],  # 0x73 's'
        [160, 3, 4, 5, 0, -4],  # 0x74 't'
        [162, 4, 3, 5, 0, -3],  # 0x75 'u'
        [164, 4, 3, 5, 0, -3],  # 0x76 'v'
        [166, 5, 3, 5, 0, -3],  # 0x77 'w'
        [169, 4, 3, 5, 0, -3],  # 0x78 'x'
        [171, 4, 4, 5, 0, -3],  # 0x79 'y'
        [173, 4, 3, 5, 0, -3],  # 0x7A 'z'
        [175, 3, 6, 5, 1, -5],  # 0x7B '{'
        [178, 1, 6, 5, 2, -5],  # 0x7C '|'
        [179, 3, 6, 5, 1, -5],  # 0x7D '}'
        [182, 3, 3, 4, 0, -4],
    ]  # 0x7E '~'


# Approx. 4959 bytes
