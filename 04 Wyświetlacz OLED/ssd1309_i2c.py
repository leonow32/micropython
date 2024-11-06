import framebuf

WIDTH   = 128
HEIGHT  = 64
ADDRESS = 0x3C

_i2c = None

def write_cmd(cmd):
    temp = bytearray([0x80, cmd])
    _i2c.writeto(ADDRESS, temp)

def refresh(array):    
#     set_cursor = bytearray([0x21, 0x00, 0x7F, 0x22, 0x00, 0x07])
#     set_cursor = b"\x21\x00\x7F\x22\x00\x07"
    set_cursor = (0x21, 0x00, 0x7F, 0x22, 0x00, 0x07)
    
    for byte in set_cursor:
        write_cmd(byte)
    
#     write_list = [bytearray([0x40]), array]
    write_list = [b"\x40", array]
    _i2c.writevto(ADDRESS, write_list)
    
#     test = bytearray([0x40]) + array
#     
#     
#     _i2c.writeto(ADDRESS, test)

def init(i2c):
    global _i2c
    _i2c = i2c
    
    init_sequence = (0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, 0x7F, 0xC8,
                     0xD3, 0x00, 0xDA, 0x12, 0xD5, 0x80, 0xD9, 0xF1,
                     0xDB, 0x30, 0x81, 0xFF, 0xA4, 0xA6, 0x8D, 0x14, 0xAF)
        
    for cmd in init_sequence:
        write_cmd(cmd)

