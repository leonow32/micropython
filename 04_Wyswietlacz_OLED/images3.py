import framebuf
back_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xc0\xc0\xc0\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x03\x03\x07\x1f\xfe\xfc\xf0\x00\x00\x00\x00\x00\x00  pp\xf8\xf8\xfc\xfc\xfe\xfepppppppppx8<\x1f\x0f\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
book_32x32 = (32, 32, bytearray(b'\x00\xe0\xf0\x18\x0c\x0c\x06\x06\x06\x06\x06\x06\x0c\x180\xe0\xe00\x18\x0c\x06\x06\x06\x06\x06\x06\x0c\x0c\x18\xf0\xe0\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x7f\x7f`00\x18\x18\x18\x18\x18\x1800`\x7f\x7f`00\x18\x18\x18\x18\x18\x1800`\x7f\x7f\x00'))
cancel_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00@\xe0\xf0\xe0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\xe0\xf0\xe0@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x07\x0f\x1f>|\xf8\xf0\xe0\xe0\xf0\xf8|>\x1f\x0f\x07\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\xe0\xf0\xf8|>\x1f\x0f\x07\x07\x0f\x1f>|\xf8\xf0\xe0\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x07\x0f\x07\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x07\x0f\x07\x02\x00\x00\x00\x00'))
clock_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x80\xc0`0\x18\x18\x8c\x0c\x06\x06\x06&&\x06\x06\x06\x0c\x8c\x18\x180`\xc0\x80\x00\x00\x00\x00\x00\xf0\xfc\x0f\x03\x80\x00\x04\x00\x00\x00\x00\x00\x00\x00\xff\xff\x80\x80\x80\x80\x00\x00\x00\x04\x00\x80\x03\x0f\xfc\xf0\x00\x00\x0f?\xf0\xc0\x01\x00 \x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x00\x00\x00 \x00\x01\xc0\xf0?\x0f\x00\x00\x00\x00\x00\x01\x03\x06\x0c\x18\x1810```dd```01\x18\x18\x0c\x06\x03\x01\x00\x00\x00\x00'))
down_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x00`\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x07\x1f~\xfc\xf8\xf0\xe0\xc0\x80\x80\xc0\xe0\xf0\xf8\xfc~\x1f\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x07\x1f\x7f\xff\xff\xff\xff\x7f\x1f\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x07\x07\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
ep_logo_128x40 = (128, 40, bytearray(b'\x00\xf8\xf8\xf8888888\x00\xf8\xf8\xf8\x00\x00\x00\x00\x00\x00\xf8\xf8\xf8\xf888888\x00\xf8\xf8\xf8\x00\x80\xe0\xf8x\x18\x00\x00\x008888\xf8\xf8\xf88888\x00\xf8\xf8\xf8\x18\x18\x188\xf8\xf0\xe0\x00\x00\xc0\xe0\xf0x8\x18\x18\x188x\xf0\xe0\xc0\x00\x00\xf8\xf8\xf8\xf8\xe0\x80\x00\x00\x00\x00\xf8\xf8\xf8\x00\x00\xf8\xf8\xf8\xf8\x00\x00\xf8\xf8\xf8\x00\x00\xc0\xe0\xf0x\x18\x08\x00\x00\x00\xc0\xf0\xf88\xf8\xf8\xe0\x00\x00\x00\x00\x00\x00\xff\xff\xff\x8e\x8e\x8e\x8e\x8e\x80\x00\xff\xff\xff\x80\x80\x80\x80\x80\x00\xff\xff\xff\xff\x8e\x8e\x8e\x8e\x80\x00\xff\xff\xff\x0e?\xff\xf3\xc0\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00\xff\xff\xff\x0e\x0e\x1e?\xff\xf3\xe1\x80\x1f\x7f\xff\xf1\xc0\x80\x80\x80\x80\x80\xc0\xf1\xff\x7f\x0f\x00\xff\xff\xff\x00\x03\x07\x1f>\xfc\xf0\xff\xff\xff\x00\x00\xff\xff\xff\xff\x00\x00\xff\xff\xff\x04\x1f?\xfb\xf0\xe0\x80\x00\x80\xf0\xfe\xff?100?\x7f\xff\xf8\xc0\x00\x00\x00\xc3\xc3\xc3\xc3\xc3\xc3\xc3\xc3\xc3\x80\x03\x03\xc3\xc3\xc3\xc3\xc3\xc3\xc0\xc3\x83\x83\x03\x03\x03\x03\x03\x83\xc0\xc3\xc3\xc3\x00\x00\x00\x03\x03\x03\xc0\xc0\xc0\x00\x00\x00\x80\xc3\xc3\xc3@\xc0\xc0\xc0\xc0\xc3\xc3\xc3\xc0\xc0\xc0\xc0\xc0\xc3\xc3\xc3\x02\x00\x00\x01\x01\xc3\xc3\xc3\x03\x03\x81\x81\xc0\xc0\xc0\xc0\xc3\xc3\xc3\x00\xc0\xc0\xc0\xc0\xc0\xc1\xc3\xc3\xc3\xc0\xc0\x03\xc3\xc3\xc3\xc0\x80\x03\x03\x03\x00\x00\xc0\xc0\xc1\x03\x03\x03\x03\x03\x03\xc0\xc0\xc0\xc0\x80\x00\x00\x01\x03\x03\x03\x00\x00\xff\xff\xff\xe0``q\x7f??\x0e\x00\xff\xff\xffpp\xf0\xf9\xff\x9f\x0f\x00\x00\x80\xe0\xfc\xff\x9f\x81\x87\xff\xff\xf8\xe0\x00\x00\x00\xff\xff\xff0\xf8\xfe\xff\x87\x03\x00\x00\x00\x00\x00\x00\xff\xff\xff\x01\x00\x00\x00\x00\x01\x07\x1f\x7f\xfc\xf0\xfc?\x0f\x03\x00\xfc\xff\xff\x87\x03\x01\x00\x00\x00\x00\x01\x00\x00\x00\xc0\xe0\xf0|?\x1f\x07\x03\x00\x00\xff\xff\xff\x07\x0f>|\xf0\xe0\x80\xff\xff\xff\x00\x00\x00\xe0\xf8\xff\x9f\x83\x83\x9f\xff\xfc\xe0\x80\x00\x00\x00\x00\x00\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1f\x00\x00\x00\x03\x07\x1f\x1e\x18\x1c\x1f\x1f\x07\x01\x01\x01\x01\x01\x03\x0f\x1f\x1f\x18\x00\x1f\x1f\x1f\x00\x00\x01\x07\x0f\x1f\x1e\x18\x00\x00\x00\x00\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1f\x00\x00\x00\x00\x01\x07\x0f\x0f\x1e\x1c\x1c\x1c\x1c\x1c\x0c\x1c\x1e\x1f\x1f\x1f\x1d\x1c\x1c\x1c\x1c\x1c\x1c\x00\x1f\x1f\x1f\x00\x00\x00\x00\x01\x03\x0f\x1f\x1f\x1f\x00\x18\x1f\x1f\x0f\x03\x01\x01\x01\x01\x01\x0f\x1f\x1f\x1c\x00\x00\x00'))
hand_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\xf8\xfc\x0e\x06\x0e\xfc\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xe000`\xff\xff\x00\x00\x00\xff\x7f\x06\x03\x07\xfe|\x0e\x06\x0e\xfcx\x1c\x0c\x1c\xf8\xe0\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x0f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x01\x07\x1e8p`````````````````p8\x1c\x0f\x07\x00\x00'))
light_32x32 = (32, 32, bytearray(b'\x00\x18\x1800\x00\x00\x80\xc0`0\x18\x18\x0c\x0c\x0c\x0c\x0c\x0c\x18\x180`\xc0\x80\x00\x0000\x18\x18\x00\x18\x18\x18\x00\x00\x00~\xff\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81\xff~\x00\x00\x00\x18\x18\x18\x00\x18\x18\x0c\x0c\x00\x00\x01\x03\x06\x0c\x18\xf8\xf00000\xf0\xf8\x18\x0c\x06\x03\x01\x00\x00\x0c\x0c\x18\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x7f\xe0\xc0\xc0\xe0\x7f?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
ok_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\xe0\xf0\xf8|>\x1f\x0f\x07\x02\x00\x00\x00\x00\x00\x00\x01\x03\x07\x0f\x1f>|\xf8\xf0\xe0\xf0\xf8|>\x1f\x0f\x07\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
settings_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\xc0\xe0\xf0\xf0\xe0\xc0\x80\xc0\xc0\xf8\xfc\xfc\xfc\xfc\xf8\xc0\xc0\x80\xc0\xe0\xf0\xf0\xe0\xc0\x00\x00\x00\x00\x00\x00\xc0\xe0\xe0\xe1\xfb\xff\x1f\x07\x03\x01\x01\x00\x00\x00\x00\x00\x00\x01\x01\x03\x07\x1f\xff\xfb\xe1\xe0\xe0\xc0\x00\x00\x00\x00\x03\x07\x07\x87\xdf\xff\xf8\xe0\xc0\x80\x80\x00\x00\x00\x00\x00\x00\x80\x80\xc0\xe0\xf8\xff\xdf\x87\x07\x07\x03\x00\x00\x00\x00\x00\x00\x03\x07\x0f\x0f\x07\x03\x01\x03\x03\x1f????\x1f\x03\x03\x01\x03\x07\x0f\x0f\x07\x03\x00\x00\x00\x00'))
square_8x16 = (8, 16, bytearray(b'\xff\x01\x01\x01\x01\x01\x01\xff\xff\x80\x80\x80\x80\x80\x80\xff'))
test_16x16 = (16, 16, bytearray(b'\xff\x01\x05\t\x11!A\x81\x01\x01\x01\x01\x01\x01\x01U\xff\x00\x80\x00\x80\x00\x80\x00\x81\x02\x84\x08\x90 \x80U'))
up_32x32 = (32, 32, bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xe0\xe0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xe0\xf8\xfe\xff\xff\xff\xff\xfe\xf8\xe0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xe0\xf8~?\x1f\x0f\x07\x03\x01\x01\x03\x07\x0f\x1f?~\xf8\xe0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x06\x00\x00\x00\x00\x00'))
world_128x64 = (128, 64, bytearray(b"\xc0\xc0\xe0\xe0\xe0\xe0\xe0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xf0\xf0\xf8\xfc\xfc\xdc\xf0\xec\xfc\xbc\xbe\xec\xfb\x7f\xff\xd3\xffp\xc2\xee\xcf\xcf\x0f\x0f\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f\x7f\x7f\x1f\x82\x02\x00\x00\x00\x00\x00\x00\x00\x00\x06\x8e\xce\xc6\xe6\xe6\xe0\xe0\xc0\xc0\xc0\x80\xc0\xc2\xe2\xf0\xfa\xda\xca\xe8\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf8\xf8\xfa\xfe\xfe\xfe\xfc\xfc\xf8\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xe0\xe8\xf8\xf8\xf8\xf8\xf8\xf8\xf0\xe0\xe0\xc0\xc0\xf0\xd0\xf8\xd8\xe0\xc0\x80\x80\x00\'7\x1f\x1f\x1f\x0f\x07\x07\x07\x0f\x0f\x1f\x1f\x7f\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf3\xf1\xe3\xe3\xfa\xf9\xfd\xfd\xfa\xf9\xf9\xf0\xe0\x01\x03\x07\x07\x07\x01\x01\x01\x00\x00\x00\x01\x03\x03\x01\x00p\xf8\xf8\xc0\xc0\xee\xef\xef\xef\xef\xf7\xf3\xf8\xfb\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xef\xef\x0f\x07\x0f\x7f\x7f?\x1f\x07\x07\x07\x07\x03\x01\x01\x01\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff?\x0f\x0f\x03\x03\x02\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xde\xde\xde\xdf\xcf\x87\x97\x87\x8f\x9b\xb7\xa7\x9f7\xfb\xfb\xff\xff\xff\xff\xff\xe7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x1f\x7f\xff\x07gc=\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0f\x0f\x0f\x7f\x7f\x7f\xe3\xe1\xf1\xe1\x81\x1b\x180``\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf9\xf7\xc7\xbf\x7f\xff\xff\xff\xff\xff?\x1f\x07\x0f\x1f\x1f\x7f\xff\xff\xff?\x1f\x1f?\xff\xff\xff\xff\xdf\xbf\x1f\x0f\x0f\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x07\xcc\xec\xfe\xff\xff\xfe\xfe\xfe\xfc\xf8\xf8\xf0\xc0\xc0\x80\x80\x00\x00\x00\x00\x00\x00\x00\x03\x07\x0f\x1f\x1f\x1f\x0f\x0f\x1f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe|\x19\x01\x00\x00\x00\x00\x00\x00\x00\x00\x07\x0f\x0f\x00\x00\x00\x00\x10}\xf9\xc7\x87c\xf0\xf0p\x00l\x8c\x00\xc0\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x07?\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f\x0f\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf3\xff\xff\xff\xff\xff\xff\xff\xff\x7f\x7f\x00\xe0\xf00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x06\x06\x06\x84\x84\x8c\xf4\xf5\xf8\xf8\xf1\xe5\xf7\xf7\xe6\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xff\xff\xff\xff\xff\x7f\x7f?\x03\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x1f\x7f\x7f\x7f?\x1f\x0f\x00\x00\x01\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x7f\x7f\x7f??\x1f?\x7f\x7f\xff\xff\xff\xff>\x00\x00\x00\x01\x01\x00@\xc0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\xff\xff\xbf\x07\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x07\x06\x00\x00\x00\x00\x00\x00\x0c\x06\x06\x01\x00\x00\x00\x00\x00"))
