from machine import Pin, I2C
import framebuf

WIDTH   = const(128)
HEIGHT  = const(64)
ADDRESS = const(0x3C)

class SSD1309(framebuf.FrameBuffer):
    
    def __init__(self, i2c):
        self.i2c = i2c
        self.array = bytearray(WIDTH * HEIGHT // 8)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.MONO_VLSB)
        
        config = (0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, 0x7F, 0xC8,
                  0xD3, 0x00, 0xDA, 0x12, 0xD5, 0x80, 0xD9, 0xF1,
                  0xDB, 0x30, 0x81, 0xFF, 0xA4, 0xA6, 0x8D, 0x14, 0xAF)
        
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

if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    display = SSD1309(i2c)
    
    display.rect(0, 0, 128, 64, 1)
    display.text('artyrtybcdefghijklm', 1, 2, 1)
    display.text('nopqrstuvwxyz', 1, 10, 1)
    display.refresh()
    display.simulate()
    