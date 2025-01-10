import framebuf
dos8 = {
    0: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    1: (framebuf.FrameBuffer(bytearray(b'~\x81\x95\xb1\xb1\x95\x81~'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    2: (framebuf.FrameBuffer(bytearray(b'~\xff\xeb\xcf\xcf\xeb\xff~'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    3: (framebuf.FrameBuffer(bytearray(b'\x0e\x1f?~?\x1f\x0e\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    4: (framebuf.FrameBuffer(bytearray(b'\x08\x1c>\x7f>\x1c\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    5: (framebuf.FrameBuffer(bytearray(b'8:\x9f\xff\x9f:8\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    6: (framebuf.FrameBuffer(bytearray(b'\x18<\xbe\xff\xbe<\x18\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    7: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x18<<\x18\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    8: (framebuf.FrameBuffer(bytearray(b'\xff\xff\xe7\xc3\xc3\xe7\xff\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    9: (framebuf.FrameBuffer(bytearray(b'\x00<fBBf<\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    10: (framebuf.FrameBuffer(bytearray(b'\xff\xc3\x99\xbd\xbd\x99\xc3\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    11: (framebuf.FrameBuffer(bytearray(b'p\xf8\x88\x88\xfd\x7f\x07\x0f'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    12: (framebuf.FrameBuffer(bytearray(b'\x00N_\xf1\xf1_N\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    13: (framebuf.FrameBuffer(bytearray(b'\xc0\xe0\xff\x7f\x05\x05\x07\x07'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    14: (framebuf.FrameBuffer(bytearray(b'\xc0\xff\x7f\x05\x05e\x7f?'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    15: (framebuf.FrameBuffer(bytearray(b'ZZ<\xe7\xe7<ZZ'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    16: (framebuf.FrameBuffer(bytearray(b'\x7f>>\x1c\x1c\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    17: (framebuf.FrameBuffer(bytearray(b'\x08\x08\x1c\x1c>>\x7f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    18: (framebuf.FrameBuffer(bytearray(b'\x00$f\xff\xfff$\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    19: (framebuf.FrameBuffer(bytearray(b'\x00__\x00\x00__\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    20: (framebuf.FrameBuffer(bytearray(b'\x06\x0f\t\x7f\x7f\x01\x7f\x7f'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    21: (framebuf.FrameBuffer(bytearray(b'@\x9a\xbf\xa5\xa5\xfdY\x02'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    22: (framebuf.FrameBuffer(bytearray(b'\x00pppppp\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    23: (framebuf.FrameBuffer(bytearray(b'\x80\x94\xb6\xff\xff\xb6\x94\x80'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    24: (framebuf.FrameBuffer(bytearray(b'\x00\x04\x06\x7f\x7f\x06\x04\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    25: (framebuf.FrameBuffer(bytearray(b'\x00\x100\x7f\x7f0\x10\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    26: (framebuf.FrameBuffer(bytearray(b'\x08\x08\x08*>\x1c\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    27: (framebuf.FrameBuffer(bytearray(b'\x08\x1c>*\x08\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    28: (framebuf.FrameBuffer(bytearray(b'<<     \x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    29: (framebuf.FrameBuffer(bytearray(b'\x08\x1c>\x08\x08>\x1c\x08'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    30: (framebuf.FrameBuffer(bytearray(b'08<>><80'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    31: (framebuf.FrameBuffer(bytearray(b'\x06\x0e\x1e>>\x1e\x0e\x06'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    32: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    33: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x06__\x06\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    34: (framebuf.FrameBuffer(bytearray(b'\x00\x03\x07\x00\x00\x07\x03\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    35: (framebuf.FrameBuffer(bytearray(b'\x14\x7f\x7f\x14\x7f\x7f\x14\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    36: (framebuf.FrameBuffer(bytearray(b'\x00$.kk:\x12\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    37: (framebuf.FrameBuffer(bytearray(b'Ff0\x18\x0cfb\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    38: (framebuf.FrameBuffer(bytearray(b'0zO]7zH\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    39: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x04\x07\x03\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    40: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x1c>cA\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    41: (framebuf.FrameBuffer(bytearray(b'\x00\x00Ac>\x1c\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    42: (framebuf.FrameBuffer(bytearray(b'\x08*>\x1c\x1c>*\x08'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    43: (framebuf.FrameBuffer(bytearray(b'\x00\x08\x08>>\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    44: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x80\xe0`\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    45: (framebuf.FrameBuffer(bytearray(b'\x00\x08\x08\x08\x08\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    46: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00``\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    47: (framebuf.FrameBuffer(bytearray(b'`0\x18\x0c\x06\x03\x01\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    48: (framebuf.FrameBuffer(bytearray(b'\x1c>cIc>\x1c\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    49: (framebuf.FrameBuffer(bytearray(b'\x00@B\x7f\x7f@@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    50: (framebuf.FrameBuffer(bytearray(b'BcqYIof\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    51: (framebuf.FrameBuffer(bytearray(b'"cIII\x7f6\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    52: (framebuf.FrameBuffer(bytearray(b'\x18\x1c\x16S\x7f\x7fP\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    53: (framebuf.FrameBuffer(bytearray(b'/oIIIy1\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    54: (framebuf.FrameBuffer(bytearray(b'<~KIIx0\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    55: (framebuf.FrameBuffer(bytearray(b'\x03\x03qy\r\x07\x03\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    56: (framebuf.FrameBuffer(bytearray(b'6\x7fIII\x7f6\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    57: (framebuf.FrameBuffer(bytearray(b'\x06OIIi?\x1e\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    58: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00ff\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    59: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x80\xe6f\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    60: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x08\x1c6cA\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    61: (framebuf.FrameBuffer(bytearray(b'\x00$$$$$$\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    62: (framebuf.FrameBuffer(bytearray(b'\x00Ac6\x1c\x08\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    63: (framebuf.FrameBuffer(bytearray(b'\x02\x03\x01Y]\x07\x02\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    64: (framebuf.FrameBuffer(bytearray(b'>\x7fA]]\x1f\x1e\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    65: (framebuf.FrameBuffer(bytearray(b'|~\x0b\t\x0b~|\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    66: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fII\x7f6\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    67: (framebuf.FrameBuffer(bytearray(b'\x1c>cAAc"\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    68: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fAc>\x1c\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    69: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fI]Ac\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    70: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fI\x1d\x01\x03\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    71: (framebuf.FrameBuffer(bytearray(b'\x1c>cAQ3r\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    72: (framebuf.FrameBuffer(bytearray(b'\x7f\x7f\x08\x08\x08\x7f\x7f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    73: (framebuf.FrameBuffer(bytearray(b'\x00\x00A\x7f\x7fA\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    74: (framebuf.FrameBuffer(bytearray(b'0p@A\x7f?\x01\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    75: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7f\x08\x1cwc\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    76: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fA@`p\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    77: (framebuf.FrameBuffer(bytearray(b'\x7f\x7f\x0e\x1c\x0e\x7f\x7f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    78: (framebuf.FrameBuffer(bytearray(b'\x7f\x7f\x06\x0c\x18\x7f\x7f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    79: (framebuf.FrameBuffer(bytearray(b'>\x7fAAA\x7f>\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    80: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7fI\t\x0f\x06\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    81: (framebuf.FrameBuffer(bytearray(b'>\x7fAA\xe1\xff\xbe\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    82: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7f\t\x19\x7ff\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    83: (framebuf.FrameBuffer(bytearray(b'\x00"gMYs"\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    84: (framebuf.FrameBuffer(bytearray(b'\x00\x07C\x7f\x7fC\x07\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    85: (framebuf.FrameBuffer(bytearray(b'?\x7f@@@\x7f?\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    86: (framebuf.FrameBuffer(bytearray(b'\x1f?`@`?\x1f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    87: (framebuf.FrameBuffer(bytearray(b'?\x7f`8`\x7f?\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    88: (framebuf.FrameBuffer(bytearray(b'cw\x1c\x08\x1cwc\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    89: (framebuf.FrameBuffer(bytearray(b'\x00\x07OxxO\x07\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    90: (framebuf.FrameBuffer(bytearray(b'GcqYMgs\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    91: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x7f\x7fAA\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    92: (framebuf.FrameBuffer(bytearray(b'\x01\x03\x06\x0c\x180`\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    93: (framebuf.FrameBuffer(bytearray(b'\x00\x00AA\x7f\x7f\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    94: (framebuf.FrameBuffer(bytearray(b'\x08\x0c\x06\x03\x06\x0c\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    95: (framebuf.FrameBuffer(bytearray(b'\x80\x80\x80\x80\x80\x80\x80\x80'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    96: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x01\x03\x06\x04\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    97: (framebuf.FrameBuffer(bytearray(b' tTT<x@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    98: (framebuf.FrameBuffer(bytearray(b'A\x7f?DD|8\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    99: (framebuf.FrameBuffer(bytearray(b'8|DDDl(\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    100: (framebuf.FrameBuffer(bytearray(b'8|DE?\x7f@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    101: (framebuf.FrameBuffer(bytearray(b'8|TTT\\\x18\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    102: (framebuf.FrameBuffer(bytearray(b'H~\x7fI\t\x03\x02\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    103: (framebuf.FrameBuffer(bytearray(b'\x98\xbc\xa4\xa4\xf8|\x04\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    104: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7f\x08\x04|x\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    105: (framebuf.FrameBuffer(bytearray(b'\x00\x00D}}@\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    106: (framebuf.FrameBuffer(bytearray(b'\x00`\xe0\x80\x80\xfd}\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    107: (framebuf.FrameBuffer(bytearray(b'A\x7f\x7f\x108lD\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    108: (framebuf.FrameBuffer(bytearray(b'\x00\x00A\x7f\x7f@\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    109: (framebuf.FrameBuffer(bytearray(b'||\x0cx\x0c|x\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    110: (framebuf.FrameBuffer(bytearray(b'\x04|x\x04\x04|x\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    111: (framebuf.FrameBuffer(bytearray(b'8|DDD|8\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    112: (framebuf.FrameBuffer(bytearray(b'\x84\xfc\xf8\xa4$<\x18\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    113: (framebuf.FrameBuffer(bytearray(b'\x18<$\xa4\xf8\xfc\x84\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    114: (framebuf.FrameBuffer(bytearray(b'D|xL\x04\x0c\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    115: (framebuf.FrameBuffer(bytearray(b'H\\TTTt$\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    116: (framebuf.FrameBuffer(bytearray(b'\x04\x04?\x7fDd \x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    117: (framebuf.FrameBuffer(bytearray(b'<|@@<|@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    118: (framebuf.FrameBuffer(bytearray(b'\x1c<`@`<\x1c\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    119: (framebuf.FrameBuffer(bytearray(b'<|`8`|<\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    120: (framebuf.FrameBuffer(bytearray(b'Dl8\x108lD\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    121: (framebuf.FrameBuffer(bytearray(b'\x9c\xbc\xa0\xa0\xa0\xfc|\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    122: (framebuf.FrameBuffer(bytearray(b'\x00Ldt\\Ld\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    123: (framebuf.FrameBuffer(bytearray(b'\x00\x08\x08>wAA\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    124: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x7f\x7f\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    125: (framebuf.FrameBuffer(bytearray(b'\x00AAw>\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    126: (framebuf.FrameBuffer(bytearray(b'\x02\x03\x01\x03\x02\x03\x01\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    127: (framebuf.FrameBuffer(bytearray(b'pxLFLxp\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    128: (framebuf.FrameBuffer(bytearray(b'\x1e\xbf\xa1\xa1\xe1s\x12\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    129: (framebuf.FrameBuffer(bytearray(b'=}@@=}@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    130: (framebuf.FrameBuffer(bytearray(b'8|TVW]\x18\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    131: (framebuf.FrameBuffer(bytearray(b'"uUU=yB\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    132: (framebuf.FrameBuffer(bytearray(b'!uTT<yA\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    133: (framebuf.FrameBuffer(bytearray(b' tUW>x@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    134: (framebuf.FrameBuffer(bytearray(b' tWW<x@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    135: (framebuf.FrameBuffer(bytearray(b'\x18<\xa4\xa4\xe4d$\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    136: (framebuf.FrameBuffer(bytearray(b':}UUU]\x1a\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    137: (framebuf.FrameBuffer(bytearray(b'9}TTT]\x19\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    138: (framebuf.FrameBuffer(bytearray(b'8|UWV\\\x18\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    139: (framebuf.FrameBuffer(bytearray(b'\x00\x01E||A\x01\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    140: (framebuf.FrameBuffer(bytearray(b'\x02\x01E}}A\x02\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    141: (framebuf.FrameBuffer(bytearray(b'\x00\x00I{z@\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    142: (framebuf.FrameBuffer(bytearray(b'y}\x16\x12\x16}y\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    143: (framebuf.FrameBuffer(bytearray(b'x~\x17\x15\x17~x\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    144: (framebuf.FrameBuffer(bytearray(b'||VWUDD\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    145: (framebuf.FrameBuffer(bytearray(b' tT||TT\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    146: (framebuf.FrameBuffer(bytearray(b'|~\x0b\t\x7f\x7fI\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    147: (framebuf.FrameBuffer(bytearray(b':}EEE}:\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    148: (framebuf.FrameBuffer(bytearray(b'9}DDD}9\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    149: (framebuf.FrameBuffer(bytearray(b'8|EGF|8\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    150: (framebuf.FrameBuffer(bytearray(b':yAA9z@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    151: (framebuf.FrameBuffer(bytearray(b'<}CB<|@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    152: (framebuf.FrameBuffer(bytearray(b'\x9d\xbd\xa0\xa0\xa0\xfd}\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    153: (framebuf.FrameBuffer(bytearray(b'\x19=fBf=\x19\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    154: (framebuf.FrameBuffer(bytearray(b'=}@@@}=\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    155: (framebuf.FrameBuffer(bytearray(b'\x18<$\xe7\xe7$$\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    156: (framebuf.FrameBuffer(bytearray(b'H~\x7fICf \x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    157: (framebuf.FrameBuffer(bytearray(b'\x00+/\xfc\xfc/+\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    158: (framebuf.FrameBuffer(bytearray(b'\xff\xff\t\t/\xf6\xf8\xa0'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    159: (framebuf.FrameBuffer(bytearray(b' `H~?\t\x03\x02'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    160: (framebuf.FrameBuffer(bytearray(b' tVW=x@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    161: (framebuf.FrameBuffer(bytearray(b'\x00\x00Hz{A\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    162: (framebuf.FrameBuffer(bytearray(b'8|DFG}8\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    163: (framebuf.FrameBuffer(bytearray(b'<|BC=|@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    164: (framebuf.FrameBuffer(bytearray(b'\n{q\x0b\n{q\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    165: (framebuf.FrameBuffer(bytearray(b'z{\x193b{y\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    166: (framebuf.FrameBuffer(bytearray(b'\x00&/)//(\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    167: (framebuf.FrameBuffer(bytearray(b'\x00&/)/&\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    168: (framebuf.FrameBuffer(bytearray(b'\x00 p]M@` '), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    169: (framebuf.FrameBuffer(bytearray(b'88\x08\x08\x08\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    170: (framebuf.FrameBuffer(bytearray(b'\x08\x08\x08\x08\x0888\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    171: (framebuf.FrameBuffer(bytearray(b'Bo?\x18\xcc\xee\xbb\x91'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    172: (framebuf.FrameBuffer(bytearray(b'Bo?Xl\xd6\xfbA'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    173: (framebuf.FrameBuffer(bytearray(b'\x00\x000}}0\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    174: (framebuf.FrameBuffer(bytearray(b'\x08\x1c6"\x08\x1c6"'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    175: (framebuf.FrameBuffer(bytearray(b'"6\x1c\x08"6\x1c\x08'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    176: (framebuf.FrameBuffer(bytearray(b'\xaa\x00U\x00\xaa\x00U\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    177: (framebuf.FrameBuffer(bytearray(b'\xaaU\xaaU\xaaU\xaaU'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    178: (framebuf.FrameBuffer(bytearray(b'\xaa\xffU\xff\xaa\xffU\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    179: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xff\xff\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    180: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\xff\xff\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    181: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\xff\xff\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    182: (framebuf.FrameBuffer(bytearray(b'\x10\x10\xff\xff\x00\xff\xff\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    183: (framebuf.FrameBuffer(bytearray(b'\x10\x10\xf0\xf0\x10\xf0\xf0\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    184: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\xfc\xfc\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    185: (framebuf.FrameBuffer(bytearray(b'\x14\x14\xf7\xf7\x00\xff\xff\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    186: (framebuf.FrameBuffer(bytearray(b'\x00\x00\xff\xff\x00\xff\xff\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    187: (framebuf.FrameBuffer(bytearray(b'\x14\x14\xf4\xf4\x04\xfc\xfc\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    188: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x17\x17\x10\x1f\x1f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    189: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x1f\x1f\x10\x1f\x1f\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    190: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\x1f\x1f\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    191: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\xf0\xf0\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    192: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x1f\x1f\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    193: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\x1f\x1f\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    194: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\xf0\xf0\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    195: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xff\xff\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    196: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\x10\x10\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    197: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\xff\xff\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    198: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xff\xff\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    199: (framebuf.FrameBuffer(bytearray(b'\x00\x00\xff\xff\x00\xff\xff\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    200: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x1f\x1f\x10\x17\x17\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    201: (framebuf.FrameBuffer(bytearray(b'\x00\x00\xfc\xfc\x04\xf4\xf4\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    202: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x17\x17\x10\x17\x17\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    203: (framebuf.FrameBuffer(bytearray(b'\x14\x14\xf4\xf4\x04\xf4\xf4\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    204: (framebuf.FrameBuffer(bytearray(b'\x00\x00\xff\xff\x00\xf7\xf7\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    205: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\x14\x14\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    206: (framebuf.FrameBuffer(bytearray(b'\x14\x14\xf7\xf7\x00\xf7\xf7\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    207: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\x17\x17\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    208: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x1f\x1f\x10\x1f\x1f\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    209: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\xf4\xf4\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    210: (framebuf.FrameBuffer(bytearray(b'\x10\x10\xf0\xf0\x10\xf0\xf0\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    211: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x1f\x1f\x10\x1f\x1f\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    212: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x1f\x1f\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    213: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xfc\xfc\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    214: (framebuf.FrameBuffer(bytearray(b'\x00\x00\xf0\xf0\x10\xf0\xf0\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    215: (framebuf.FrameBuffer(bytearray(b'\x10\x10\xff\xff\x10\xff\xff\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    216: (framebuf.FrameBuffer(bytearray(b'\x14\x14\x14\xff\xff\x14\x14\x14'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    217: (framebuf.FrameBuffer(bytearray(b'\x10\x10\x10\x1f\x1f\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    218: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xf0\xf0\x10\x10\x10'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    219: (framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    220: (framebuf.FrameBuffer(bytearray(b'\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    221: (framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x00\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    222: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\xff\xff\xff\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    223: (framebuf.FrameBuffer(bytearray(b'\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    224: (framebuf.FrameBuffer(bytearray(b'8|Dl8lD\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    225: (framebuf.FrameBuffer(bytearray(b'~\x7f\x01\t_v \x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    226: (framebuf.FrameBuffer(bytearray(b'\x7f\x7f\x01\x01\x01\x03\x03\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    227: (framebuf.FrameBuffer(bytearray(b'\x04||\x04||\x04\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    228: (framebuf.FrameBuffer(bytearray(b'cw]IAcc\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    229: (framebuf.FrameBuffer(bytearray(b'8|D|<\x04\x04\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    230: (framebuf.FrameBuffer(bytearray(b'\x80\xfc|@@|<\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    231: (framebuf.FrameBuffer(bytearray(b'\x04\x06\x02~|\x06\x02\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    232: (framebuf.FrameBuffer(bytearray(b'\x00\x99\xbd\xe7\xe7\xbd\x99\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    233: (framebuf.FrameBuffer(bytearray(b'\x1c>kIk>\x1c\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    234: (framebuf.FrameBuffer(bytearray(b'L~s\x01s~L\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    235: (framebuf.FrameBuffer(bytearray(b'\x000xJO}9\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    236: (framebuf.FrameBuffer(bytearray(b'\x18<$<<$<\x18'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    237: (framebuf.FrameBuffer(bytearray(b"\x98\xfcd<>\'=\x18"), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    238: (framebuf.FrameBuffer(bytearray(b'\x00\x1c>kIII\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    239: (framebuf.FrameBuffer(bytearray(b'|~\x02\x02\x02~|\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    240: (framebuf.FrameBuffer(bytearray(b'*******\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    241: (framebuf.FrameBuffer(bytearray(b'\x00DD__DD\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    242: (framebuf.FrameBuffer(bytearray(b'\x00@Q[ND@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    243: (framebuf.FrameBuffer(bytearray(b'\x00@DN[Q@\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    244: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\xfe\xff\x01\x07\x06'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    245: (framebuf.FrameBuffer(bytearray(b'`\xe0\x80\xff\x7f\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    246: (framebuf.FrameBuffer(bytearray(b'\x00\x08\x08**\x08\x08\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    247: (framebuf.FrameBuffer(bytearray(b'$6\x126$6\x12\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    248: (framebuf.FrameBuffer(bytearray(b'\x00\x06\x0f\t\x0f\x06\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    249: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x18\x18\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    250: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x08\x08\x00\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    251: (framebuf.FrameBuffer(bytearray(b'\x100p\xc0\xff\xff\x01\x01'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    252: (framebuf.FrameBuffer(bytearray(b'\x00\x01\x1f\x1e\x01\x1f\x1e\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    253: (framebuf.FrameBuffer(bytearray(b'\x00\x11\x19\x1d\x17\x12\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    254: (framebuf.FrameBuffer(bytearray(b'\x00\x00<<<<\x00\x00'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
    255: (framebuf.FrameBuffer(bytearray(b'\xff\x81\x81\x81\x81\x81\x81\xff'), 8, 8, framebuf.MONO_VLSB), 8, 8, 0),
}
