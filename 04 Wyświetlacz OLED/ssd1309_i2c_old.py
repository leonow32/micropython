from micropython import const
import framebuf

WIDTH  = 128
HEIGHT = 64
ADDRESS = 0x3C

_i2c = None

# register definitions
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
    
def write_data(buffer):
    write_list = [b"\x40", None]  # Co=0, D/C#=1
    write_list[1] = buffer
    _i2c.writevto(ADDRESS, write_list)

def refresh(array):
#     write_cmd(SET_COL_ADDR)
#     write_cmd(0)
#     write_cmd(127)
#     write_cmd(SET_PAGE_ADDR)
#     write_cmd(0)
#     write_cmd(7)
    
    set_cursor = bytearray([0x80, 0x21, 0x80, 0, 0x80, 127, 0x80, 0x22, 0x80, 0, 0x80, 7])
    _i2c.writeto(ADDRESS, set_cursor)
    
    write_list = [b"\x40", None]  # Co=0, D/C#=1
    write_list[1] = array
    _i2c.writevto(ADDRESS, write_list)

def init(i2c):
    
    print("init")
    global _i2c
    _i2c = i2c
    
    init_sequence = (
        SET_DISP | 0x00,  # off
        # address setting
        SET_MEM_ADDR,
        0x00,  # horizontal
        # resolution and layout
        SET_DISP_START_LINE | 0x00,
        SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
        SET_MUX_RATIO,
        HEIGHT - 1,
        SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
        SET_DISP_OFFSET,
        0x00,
        SET_COM_PIN_CFG,
        #0x02 if self.width > 2 * self.height else 0x12,
        0x12,
        
        # timing and driving scheme
        SET_DISP_CLK_DIV,
        0x80,
        SET_PRECHARGE,
        0xF1,
        SET_VCOM_DESEL,
        0x30,  # 0.83*Vcc
        # display
        SET_CONTRAST,
        0xFF,  # maximum
        SET_ENTIRE_ON,  # output follows RAM contents
        SET_NORM_INV,  # not inverted
        # charge pump
        SET_CHARGE_PUMP,
        0x14,
        SET_DISP | 0x01,
    )
    
    for cmd in init_sequence:
        write_cmd(cmd)

