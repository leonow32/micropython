# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import framebuf

WIDTH   = const(128)
HEIGHT  = const(64)

class SSD1309(framebuf.FrameBuffer):
    
    @micropython.native
    def __init__(self, i2c, rotate=False, address=0x3C):
        self.i2c = i2c
        self.address = address
        self.array = bytearray(WIDTH * HEIGHT // 8)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.MONO_VLSB)
        
        config = (
            0xAE,                     # Display off
            0x20, 0x00,               # Set memory addressing mode to horizontal addressing mode
            0x40,                     # Set display start line to 0
            0xA0 if rotate else 0xA1, # Set segment remap
            0xA8, 0x3F,               # Set multiplex ratio to 63
            0xC0 if rotate else 0xC8, # Set COM scan direction
            0xD3, 0x00,               # Set display offset to 0
            0xDA, 0x12,               # Set COM pins hardware config to enable COM left/right remap, sequential COM pin config
            0xD5, 0x80,               # Set clock and oscillator frequency to freq=8, clock=0
            0xD9, 0xF1,               # Set pre-charge period to phase_2=F, phase_1=1
            0xDB, 0x3C,               # Set VCOMH to max
            0x81, 0xFF,               # Set contrast to 255 (max)
            0xA4,                     # Use image in GDDRAM memory
            0xA6,                     # Display not inverted
            0x8D, 0x14,               # SSD1306 only - charge pump enable
            0xAF,                     # Display on
        )
        
        for cmd in config:
            self.write_cmd(cmd)
            
    @micropython.viper
    def write_cmd(self, cmd: int):
        self.i2c.writeto(self.address, bytes([0x80, cmd]))
    
    @micropython.viper
    def display_on(self):
        self.write_cmd(0xAF)
        
    @micropython.viper
    def display_off(self):
        self.write_cmd(0xAE)
    
    @micropython.viper
    def contrast(self, value):
        self.write_cmd(0x81)
        self.write_cmd(value)
    
    @micropython.viper
    def refresh(self):
        # Set column address range from 0x00 to 0x7F, set page address range from 0x00 to 0x07
        for cmd in (0x21, 0x00, 0x7F, 0x22, 0x00, 0x07):
            self.write_cmd(cmd)
        
        self.i2c.writevto(self.address, (b"\x40", self.array))
        
    @micropython.viper
    def simulate(self):
        for y in range(HEIGHT):
            print(f"{y}\t", end="")
            for x in range(WIDTH):
                bit  = 1 << (y % 8)
                byte = int(self.array[(y // 8) * WIDTH + x])
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
