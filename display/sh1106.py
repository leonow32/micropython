# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import framebuf
import mem_used

WIDTH   = const(128) # Visible width 
WIDTHR  = const(132) # Memory buffer inside the driver
HEIGHT  = const(64)

class SH1106(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, i2c, address=0x3C, flip_x=False, flip_y=False, offset_x=2):
        """
        - offset_x - max 15px
        """
        self.i2c = i2c
        self.address = address
        self.offset_x = offset_x
        self.array = bytearray(WIDTHR * HEIGHT // 8)
        super().__init__(self.array, WIDTHR, HEIGHT, framebuf.MONO_VLSB)
        
        config = (
            0xAE,                     # Display off
            0x00 | offset_x,          # Column Low Nibble + offset x
            0x10,                     # Column High Nibble = 0
            0xB0,                     # Set Page = 0
            0x40,                     # Set Start Line = 0
            0xA1 if flip_x else 0xA0, # Set Remap (flip x)
            0xDA, 0x12,               # Com pins
            0xD3, 0x00,               # Display offset
            0xC8 if flip_y else 0xC0, # Scan direction (flip y)
            0xA6,                     # Positive image
            0xA4,                     # Entrie display on
            0x81, 0xFF,               # Contrast = full
            0xA8, 0x3F,               # Multiplex ratio = 1/64 duty
            0xD5, 0x80,               # Display clock divider
            0xD9, 0xF1,               # Charge period
            0xDB, 0x40,               # VCOM select
            0x8D, 0x14,               # Charge pump
            0xAF,                     # Display on
            
#             0x20, 0x00,               # Set memory addressing mode to horizontal addressing mode
#             0x40,                     # Set display start line to 0
#             0xA0 if rotate else 0xA1, # Set segment remap
#             0xA8, 0x3F,               # Set multiplex ratio to 63
#             0xC0 if rotate else 0xC8, # Set COM scan direction
#             0xD3, 0x00,               # Set display offset to 0
#             0xDA, 0x12,               # Set COM pins hardware config to enable COM left/right remap, sequential COM pin config
#             0xD5, 0x80,               # Set clock and oscillator frequency to freq=8, clock=0
#             0xD9, 0xF1,               # Set pre-charge period to phase_2=F, phase_1=1
#             0xDB, 0x3C,               # Set VCOMH to max
#             0x81, 0xFF,               # Set contrast to 255 (max)
#             0xA4,                     # Use image in GDDRAM memory
#             0xA6,                     # Display not inverted
#             0x8D, 0x14,               # SSD1306 only - charge pump enable
#             0xAF,                     # Display on
        )
        
        for cmd in config:
            self.write_cmd(cmd)
            
    @micropython.viper
    def write_cmd(self, cmd: int):
        self.i2c.writeto(self.address, bytes([0x80, cmd]))
    
    @micropython.viper
    def enable(self):
        self.write_cmd(0xAF)
        
    @micropython.viper
    def disable(self):
        self.write_cmd(0xAE)
    
    @micropython.viper
    def contrast(self, value):
        self.write_cmd(0x81)
        self.write_cmd(value)
    
    @micropython.native
    def refresh(self):
        for page in range(8):
            header = bytes([
                0x80, 0xB0 | page,          # Set page number
                0x80, 0x00 | self.offset_x, # Set x cursor, low nibble
                0x80, 0x10,                 # Set x cursor, high nibble
                0x40                        # The following bytes are graphic data
            ])
            
            self.i2c.writevto(self.address, (header, self.array[page*WIDTHR:(page+1)*WIDTHR-1]))
        
    @micropython.viper
    def simulate(self):
        for y in range(HEIGHT):
            print(f"{y}\t", end="")
            for x in range(WIDTH):
                bit  = 1 << (y % 8)
                byte = int(self.array[(y // 8) * WIDTHR + x])
                pixel = "#" if byte & bit else "."
                print(pixel, end="")
            print("")
    
    @micropython.native
    def print_char(self, font, char, x, y, color=1):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        width  = bitmap[0]
        height = bitmap[1]
        space  = bitmap[2]
        
        if color:
            buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
        else:
            negative_bitmap = bitmap[:]
            for i in range(3, len(bitmap)):
                negative_bitmap[i] = ~negative_bitmap[i]
            buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
            self.rect(x-space, y, space, height, 1, True)
            self.rect(x+width, y, space, height, 1, True)
        
        self.blit(buffer, x, y)
        return width + space     

    @micropython.native
    def print_text(self, font, text, x, y, align="L", color=1):
        width = self.get_text_width(font, text)
        
        if   align == "R":
            x = WIDTH - width
        elif align == "C":
            x = WIDTH//2 - width//2
        elif align == "r":
            x = x - width + 1
        elif align == "c":
            x = x - width//2
        
        for char in text:
            x += self.print_char(font, char, x, y, color)
    
    @micropython.native
    def get_text_width(self, font, text):
        total = 0
        last_char_space = 0
        for char in text:
            bitmap = font.get(ord(char), font[0])
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space

if __name__ == "__main__":
    from machine import Pin, I2C
    import mem_used
#     import sh1106

    i2c = I2C(0) # use default pinout and clock frequency
    print(i2c)   # print pinout and clock frequency

    display = SH1106(i2c, address=0x3D, offset_x=2, flip_x=True, flip_y=True)
    display.rect(0, 0, 128, 64, 1)
    display.line(2, 2, 125, 61, 1)
    display.text('abcdefghijklm', 1, 2, 1)
    display.text('nopqrstuvwxyz', 1, 10, 1)
    display.refresh()
#     display.simulate()

    mem_used.print_ram_used()
