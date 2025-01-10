from machine import Pin, I2C
import framebuf
import mem_used

WIDTH   = const(128)
HEIGHT  = const(64)
ADDRESS = const(0x3C)

class SSD1309(framebuf.FrameBuffer):
    
    def __init__(self, i2c):
        self.i2c = i2c
        self.array = bytearray(WIDTH * HEIGHT // 8)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.MONO_VLSB)
        
        config = (0xAE, 0x20, 0x00, 0x40, 0xA1,
                  0xA8, 0x7F, 0xC8, 0xD3, 0x00,
                  0xDA, 0x12, 0xD5, 0x80, 0xD9,
                  0xF1, 0xDB, 0x30, 0x81, 0xFF,
                  0xA4, 0xA6, 0x8D, 0x14, 0xAF)
        
        for cmd in config:
            self.i2c.writeto(ADDRESS, bytes((0x80, cmd)))
            
    def refresh(self):
        set_cursor = (0x21, 0x00, 0x7F, 0x22, 0x00, 0x07)
    
        for cmd in set_cursor:
            self.i2c.writeto(ADDRESS, bytes([0x80, cmd]))
        
        write_list = [b"\x40", self.array]
        self.i2c.writevto(ADDRESS, write_list)
        
    def simulate(self):
        for y in range(HEIGHT):
            print(f"{y}\t", end="")
            for x in range(WIDTH):
                bit  = 1 << (y % 8)
                byte = self.array[(y // 8) * WIDTH + x]
                pixel = "#" if byte & bit else "."
                print(pixel, end="")
            print("")
    
    def print_char(self, font, char, x, y, color=1):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        if color:
            buffer = framebuf.FrameBuffer(bitmap[3:], bitmap[1], bitmap[0], 0)
        else:
            negative_bitmap = bitmap[:]
            for i in range(3, len(bitmap)): negative_bitmap[i] = ~negative_bitmap[i]
            buffer = framebuf.FrameBuffer(negative_bitmap[3:], bitmap[1], bitmap[0], 0)
            self.rect(x-bitmap[2], y, bitmap[2], bitmap[0], 1, True)
            self.rect(x+bitmap[1], y, bitmap[2], bitmap[0], 1, True)
        
        self.blit(buffer, x, y)
        return bitmap[1] + bitmap[2]       

    def print_text(self, font, text, x, y, align="L", color=1):
        width = self.get_text_width(font, text)
        
        if align == "R":
            x = WIDTH - width
        elif align == "C":
            x = WIDTH//2 - width//2
        elif align == "r":
            x = x - width + 1
        elif align == "c":
            x = x - width//2
        
        for char in text:
            x += self.print_char(font, char, x, y, color)
    
    def get_text_width(self, font, text):
        width = 0
        last_char_spacing = 0
        for char in text:
            try:
                bitmap = font[ord(char)]
            except:
                bitmap = font[0]
                print(f"Char {char} doesn't exist in font")
            
            width += bitmap[1]
            width += bitmap[2]
            last_char_spacing = bitmap[2]
        
        return width - last_char_spacing

if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    display = SSD1309(i2c)
    display.rect(0, 0, 128, 64, 1)
    display.text('abcdefghijklm', 1, 2, 1)
    display.text('nopqrstuvwxyz', 1, 10, 1)
    display.refresh()
    display.simulate()
    mem_used.print_ram_used()
    