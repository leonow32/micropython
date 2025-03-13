import framebuf
square_8x16 = framebuf.FrameBuffer(bytearray(b'\xff\x01\x01\x01\x01\x01\x01\xff\xff\x80\x80\x80\x80\x80\x80\xff'), 8, 16, framebuf.MONO_VLSB)
