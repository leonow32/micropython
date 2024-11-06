import framebuf

WIDTH  = 128
HEIGHT = 64
ADDRESS = 0x3C

_i2c = None

from micropython import const
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

def write_cmd(cmd):
    temp = bytearray([0x80, cmd])
    _i2c.writeto(ADDRESS, temp)

def refresh(array):    
    set_cursor = bytearray([0x21, 0, 127, 0x22, 0, 7])
    for byte in set_cursor:
        write_cmd(byte)
    
    write_list = [b"\x40", None]  # Co=0, D/C#=1
    write_list[1] = array
    _i2c.writevto(ADDRESS, write_list)

def init(i2c):
    global _i2c
    _i2c = i2c
    
    init_sequence = (0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, 0x7F, 0xC8,
                     0xD3, 0x00, 0xDA, 0x12, 0xD5, 0x80, 0xD9, 0xF1,
                     0xDB, 0x30, 0x81, 0xFF, 0xA4, 0xA6, 0x8D, 0x14, 0xAF)
    
    for cmd in init_sequence:
        write_cmd(cmd)

