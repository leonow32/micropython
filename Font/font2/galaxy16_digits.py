import framebuf
galaxy16_digits = {
    32: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00'), 2, 16, framebuf.MONO_VLSB), 2, 16, 1),
    39: (framebuf.FrameBuffer(bytearray(b'\x0c\x12\x12\x0c\x00\x00\x00\x00'), 4, 16, framebuf.MONO_VLSB), 4, 16, 1),
    46: (framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x000HH0'), 4, 16, framebuf.MONO_VLSB), 4, 16, 1),
    48: (framebuf.FrameBuffer(bytearray(b'\xf8\x04\x02\xe2\x12\x12\x12\xe2\x02\x04\xf8\x1f @GHHHG@ \x1f'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    49: (framebuf.FrameBuffer(bytearray(b'0(\xe4\x02\x02\xfe\x00\x00\x7f@@\x7f'), 6, 16, framebuf.MONO_VLSB), 6, 16, 1),
    50: (framebuf.FrameBuffer(bytearray(b'\x00\x9eRRRRR"\x02\x04\xf8\x7f@@LJJJJJIx'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    51: (framebuf.FrameBuffer(bytearray(b'\x1e\x12\x12\xd2RRR"\x02\x84xxHHKJJJD@!\x1e'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    52: (framebuf.FrameBuffer(bytearray(b'\xfc\x04\x04|@~\x02\x02~\xc0\x03\x02\x02\x02\x02~@@~\x03'), 10, 16, framebuf.MONO_VLSB), 10, 16, 1),
    53: (framebuf.FrameBuffer(bytearray(b'\xfe\x02\x02rRRRRR\x9e\x00{JJJJJJD@ \x1f'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    54: (framebuf.FrameBuffer(bytearray(b'\xf8\x04\x02bRRRRR\x9e\x00\x1f @DJJJD@ \x1f'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    55: (framebuf.FrameBuffer(bytearray(b'\x1e\x12\x12\xd22\x02\x82b\x1a\x06pLC`\x18\x06\x01\x00\x00\x00'), 10, 16, framebuf.MONO_VLSB), 10, 16, 1),
    56: (framebuf.FrameBuffer(bytearray(b'x\x84\x02"RRR"\x02\x84x\x1e!@DJJJD@!\x1e'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    57: (framebuf.FrameBuffer(bytearray(b'\xf8\x04\x02"RRR"\x02\x04\xf8\x00yJJJJJF@ \x1f'), 11, 16, framebuf.MONO_VLSB), 11, 16, 1),
    58: (framebuf.FrameBuffer(bytearray(b'\x80@@\x801JJ1'), 4, 16, framebuf.MONO_VLSB), 4, 16, 1),
    0: (framebuf.FrameBuffer(bytearray(b'\xff\x01\xff\xff\x80\xff'), 3, 16, framebuf.MONO_VLSB), 3, 16, 1),
}
