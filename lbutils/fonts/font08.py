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



from display.fonts.pfx_font import PFx_Font


class Font_08(PFx_Font):
    """
    Created by [`fontconvert`](https://github.com/danjperron/ssd1331_micropython.git)
    """

    def __init__(self):
        super().__init__(self.bitmap, self.index, self.glyph)

    bitmap = bytes(
        [
            0xF4,
            0xF4,
            0x00,
            0xB4,
            0x00,
            0x4B,
            0xF4,
            0x92,
            0x49,
            0x2F,
            0xD2,
            0x09,
            0xE9,
            0x64,
            0x78,
            0x9A,
            0x5E,
            0x40,
            0x00,
            0x46,
            0x94,
            0x84,
            0x21,
            0x29,
            0x62,
            0x6B,
            0xA7,
            0xC0,
            0xC0,
            0x6A,
            0xA4,
            0x00,
            0x95,
            0x58,
            0x00,
            0xAB,
            0x88,
            0xEA,
            0x80,
            0x21,
            0x3E,
            0x42,
            0x00,
            0xD8,
            0x00,
            0xE0,
            0x80,
            0x00,
            0x10,
            0x84,
            0x21,
            0x08,
            0x00,
            0x69,
            0x99,
            0x99,
            0x60,
            0x59,
            0x24,
            0xB8,
            0x00,
            0x69,
            0x12,
            0x48,
            0xF0,
            0x69,
            0x16,
            0x19,
            0x60,
            0x11,
            0x94,
            0xA9,
            0x7C,
            0x40,
            0xF8,
            0x86,
            0x19,
            0x60,
            0x69,
            0x8E,
            0x99,
            0x60,
            0xF1,
            0x22,
            0x44,
            0x80,
            0x69,
            0x96,
            0x99,
            0x60,
            0x69,
            0x97,
            0x19,
            0x60,
            0x98,
            0x13,
            0x60,
            0x24,
            0x84,
            0x20,
            0x0F,
            0x0F,
            0x00,
            0x84,
            0x24,
            0x80,
            0x69,
            0x12,
            0x44,
            0x04,
            0x39,
            0x19,
            0x6B,
            0x9D,
            0x03,
            0x80,
            0x69,
            0x99,
            0xF9,
            0x90,
            0xE9,
            0x9E,
            0x99,
            0xE0,
            0x69,
            0x88,
            0x89,
            0x60,
            0xE9,
            0x99,
            0x99,
            0xE0,
            0xF8,
            0x8E,
            0x88,
            0xF0,
            0xF8,
            0x8E,
            0x88,
            0x80,
            0x69,
            0x8B,
            0x99,
            0x70,
            0x99,
            0x9F,
            0x99,
            0x90,
            0x49,
            0x24,
            0x90,
            0x00,
            0x24,
            0x93,
            0x50,
            0x00,
            0x99,
            0xAC,
            0xA9,
            0x90,
            0x88,
            0x88,
            0x88,
            0xF0,
            0xDD,
            0x6B,
            0x58,
            0xC6,
            0x20,
            0x8E,
            0x6B,
            0x5A,
            0xCE,
            0x20,
            0x74,
            0x63,
            0x18,
            0xC5,
            0xC0,
            0xE9,
            0x9E,
            0x88,
            0x80,
            0x69,
            0x99,
            0x9B,
            0x60,
            0xE9,
            0x9E,
            0xA9,
            0x90,
            0x69,
            0x86,
            0x19,
            0x60,
            0xF9,
            0x08,
            0x42,
            0x10,
            0x80,
            0x99,
            0x99,
            0x99,
            0x60,
            0x8C,
            0x63,
            0x18,
            0xA8,
            0x80,
            0x8C,
            0x6B,
            0x5A,
            0xD5,
            0x40,
            0x8C,
            0x54,
            0x45,
            0x46,
            0x20,
            0x8C,
            0x54,
            0x42,
            0x10,
            0x80,
            0xF8,
            0x44,
            0x44,
            0x43,
            0xE0,
            0xEA,
            0xAC,
            0x00,
            0x02,
            0x04,
            0x08,
            0x10,
            0x20,
            0x40,
            0xD5,
            0x5C,
            0x00,
            0x22,
            0xA2,
            0x00,
            0xFC,
            0x00,
            0x90,
            0x79,
            0x97,
            0x88,
            0x8E,
            0x99,
            0xE0,
            0xF2,
            0x70,
            0x11,
            0x17,
            0x99,
            0x70,
            0x06,
            0xF8,
            0x70,
            0x65,
            0x4E,
            0x44,
            0x40,
            0x79,
            0x97,
            0x1F,
            0x88,
            0x8E,
            0x99,
            0x90,
            0x08,
            0x24,
            0x90,
            0x00,
            0x08,
            0x24,
            0x92,
            0xC0,
            0x88,
            0x9A,
            0xCA,
            0x90,
            0x44,
            0x44,
            0x44,
            0x60,
            0xD5,
            0x6B,
            0x10,
            0xE9,
            0x99,
            0x79,
            0x96,
            0xE9,
            0x9E,
            0x88,
            0x79,
            0x97,
            0x11,
            0xF2,
            0x40,
            0x0F,
            0xE1,
            0xF0,
            0x44,
            0xE4,
            0x46,
            0x99,
            0x97,
            0xAA,
            0xA4,
            0x8D,
            0x6A,
            0xA0,
            0x96,
            0x69,
            0x99,
            0x97,
            0x1F,
            0xF2,
            0x4F,
            0x29,
            0x64,
            0x88,
            0x00,
            0xFF,
            0x89,
            0x34,
            0xA0,
            0x00,
            0x1F,
            0x80,
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
        [0, 1, 1, 6, 0, -1],  # 0x20 ' '
        [1, 1, 6, 6, 2, -6],  # 0x21 '!'
        [3, 3, 2, 6, 1, -6],  # 0x22 '"'
        [5, 6, 8, 6, 0, -7],  # 0x23 '#'
        [11, 6, 9, 6, 0, -7],  # 0x24 '$'
        [19, 6, 8, 6, 0, -7],  # 0x25 '%'
        [25, 4, 6, 6, 1, -6],  # 0x26 '&'
        [28, 1, 2, 6, 2, -6],  # 0x27 '''
        [29, 2, 7, 6, 2, -7],  # 0x28 '('
        [32, 2, 7, 6, 1, -7],  # 0x29 ')'
        [35, 5, 5, 6, 0, -4],  # 0x2A '*'
        [39, 5, 5, 6, 0, -4],  # 0x2B '+'
        [43, 2, 3, 6, 2, -1],  # 0x2C ', '
        [45, 3, 1, 6, 1, -2],  # 0x2D '-'
        [46, 1, 1, 6, 2, -1],  # 0x2E '.'
        [47, 6, 7, 6, 0, -7],  # 0x2F '/'
        [53, 4, 7, 6, 1, -6],  # 0x30 '0'
        [57, 3, 7, 6, 1, -6],  # 0x31 '1'
        [61, 4, 7, 6, 1, -6],  # 0x32 '2'
        [65, 4, 7, 6, 1, -6],  # 0x33 '3'
        [69, 5, 7, 6, 1, -6],  # 0x34 '4'
        [74, 4, 7, 6, 1, -6],  # 0x35 '5'
        [78, 4, 7, 6, 1, -6],  # 0x36 '6'
        [82, 4, 7, 6, 1, -6],  # 0x37 '7'
        [86, 4, 7, 6, 1, -6],  # 0x38 '8'
        [90, 4, 7, 6, 1, -6],  # 0x39 '9'
        [94, 1, 4, 6, 2, -4],  # 0x3A ':'
        [95, 2, 6, 6, 2, -4],  # 0x3B ';'
        [97, 4, 5, 6, 1, -5],  # 0x3C '<'
        [100, 4, 5, 6, 1, -4],  # 0x3D '='
        [103, 4, 5, 6, 1, -5],  # 0x3E '>'
        [106, 4, 8, 6, 1, -7],  # 0x3F '?'
        [110, 6, 7, 6, 0, -7],  # 0x40 '@'
        [116, 4, 7, 6, 1, -7],  # 0x41 'A'
        [120, 4, 7, 6, 1, -7],  # 0x42 'B'
        [124, 4, 7, 6, 1, -7],  # 0x43 'C'
        [128, 4, 7, 6, 1, -7],  # 0x44 'D'
        [132, 4, 7, 6, 1, -7],  # 0x45 'E'
        [136, 4, 7, 6, 1, -7],  # 0x46 'F'
        [140, 4, 7, 6, 1, -7],  # 0x47 'G'
        [144, 4, 7, 6, 1, -7],  # 0x48 'H'
        [148, 3, 7, 6, 1, -7],  # 0x49 'I'
        [152, 3, 7, 6, 1, -7],  # 0x4A 'J'
        [156, 4, 7, 6, 1, -7],  # 0x4B 'K'
        [160, 4, 7, 6, 1, -7],  # 0x4C 'L'
        [164, 5, 7, 6, 0, -7],  # 0x4D 'M'
        [169, 5, 7, 6, 0, -7],  # 0x4E 'N'
        [174, 5, 7, 6, 0, -7],  # 0x4F 'O'
        [179, 4, 7, 6, 1, -7],  # 0x50 'P'
        [183, 4, 7, 6, 1, -7],  # 0x51 'Q'
        [187, 4, 7, 6, 1, -7],  # 0x52 'R'
        [191, 4, 7, 6, 1, -7],  # 0x53 'S'
        [195, 5, 7, 6, 0, -7],  # 0x54 'T'
        [200, 4, 7, 6, 1, -7],  # 0x55 'U'
        [204, 5, 7, 6, 0, -7],  # 0x56 'V'
        [209, 5, 7, 6, 0, -7],  # 0x57 'W'
        [214, 5, 7, 6, 0, -7],  # 0x58 'X'
        [219, 5, 7, 6, 0, -7],  # 0x59 'Y'
        [224, 5, 7, 6, 0, -7],  # 0x5A 'Z'
        [229, 2, 7, 6, 2, -7],  # 0x5B ' ['
        [232, 6, 7, 6, 0, -7],  # 0x5C '\'
        [238, 2, 7, 6, 1, -7],  # 0x5D ']'
        [241, 5, 3, 6, 0, -7],  # 0x5E '^'
        [244, 6, 1, 6, 0, 1],  # 0x5F '_'
        [246, 2, 2, 6, 1, -6],  # 0x60 '`'
        [247, 4, 4, 6, 1, -4],  # 0x61 'a'
        [249, 4, 7, 6, 1, -7],  # 0x62 'b'
        [253, 3, 4, 6, 1, -4],  # 0x63 'c'
        [255, 4, 7, 6, 1, -7],  # 0x64 'd'
        [259, 4, 5, 6, 1, -5],  # 0x65 'e'
        [262, 4, 7, 6, 1, -7],  # 0x66 'f'
        [266, 4, 6, 6, 1, -4],  # 0x67 'g'
        [269, 4, 7, 6, 1, -7],  # 0x68 'h'
        [273, 3, 7, 6, 1, -7],  # 0x69 'i'
        [277, 3, 9, 6, 0, -7],  # 0x6A 'j'
        [281, 4, 7, 6, 1, -7],  # 0x6B 'k'
        [285, 4, 7, 6, 1, -7],  # 0x6C 'l'
        [289, 5, 4, 6, 0, -4],  # 0x6D 'm'
        [292, 4, 4, 6, 1, -4],  # 0x6E 'n'
        [294, 4, 4, 6, 1, -4],  # 0x6F 'o'
        [296, 4, 6, 6, 1, -4],  # 0x70 'p'
        [299, 4, 6, 6, 1, -4],  # 0x71 'q'
        [302, 3, 4, 6, 1, -4],  # 0x72 'r'
        [304, 4, 5, 6, 1, -5],  # 0x73 's'
        [307, 4, 6, 6, 1, -6],  # 0x74 't'
        [310, 4, 4, 6, 1, -4],  # 0x75 'u'
        [312, 4, 4, 6, 1, -4],  # 0x76 'v'
        [314, 5, 4, 6, 0, -4],  # 0x77 'w'
        [317, 4, 4, 6, 1, -4],  # 0x78 'x'
        [319, 4, 6, 6, 1, -4],  # 0x79 'y'
        [322, 4, 4, 6, 1, -4],  # 0x7A 'z'
        [324, 3, 7, 6, 1, -7],  # 0x7B '{'
        [328, 1, 8, 6, 2, -7],  # 0x7C '|'
        [329, 3, 7, 6, 1, -7],  # 0x7D '}'
        [333, 4, 3, 4, 0, -5],
    ]  # 0x7E '~'
