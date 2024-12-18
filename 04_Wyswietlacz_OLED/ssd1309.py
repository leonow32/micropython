from machine import Pin, I2C
import framebuf
import images
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
        
        #for cmd in config:
        #    self.i2c.writeto(ADDRESS, bytes((0x80, cmd)))
            
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
    
#     array = bytearray(8 * 16 // 8)
#     image = framebuf.FrameBuffer(array, 16, 8, framebuf.MONO_VLSB)
#     array[0] = 0b10000000
#     display.blit(image, 0, 0)
#     
#     clock = bytearray(b'\x00\x00\x00\x00\x80\xc0`0\x18\x18\x8c\x0c\x06\x06\x06&&\x06\x06\x06\x0c\x8c\x18\x180`\xc0\x80\x00\x00\x00\x00\x00\xf0\xfc\x0f\x03\x80\x00\x04\x00\x00\x00\x00\x00\x00\x00\xff\xff\x80\x80\x80\x80\x00\x00\x00\x04\x00\x80\x03\x0f\xfc\xf0\x00\x00\x0f?\xf0\xc0\x01\x00 \x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x00\x00\x00 \x00\x01\xc0\xf0?\x0f\x00\x00\x00\x00\x00\x01\x03\x06\x0c\x18\x1810```dd```01\x18\x18\x0c\x06\x03\x01\x00\x00\x00\x00')
#     clock_buf = framebuf.FrameBuffer(clock, 32, 32, framebuf.MONO_VLSB)
#     display.blit(clock_buf, 0, 0)
    
    display.blit(images.clock, -10, 5)
    display.blit(images.test, 20, 30)
    
    display.fill_rect(64, 0, 64, 64, 1)
    
    #for i in len(images.test):
    #    images.test[i] = ~images.test[i]
        
    display.blit(images.test, 70, 30, 0, )
    
    
    #display.rect(0, 0, 128, 64, 1)
    #display.text('abcdefghijklm', 1, 2, 1)
    display.text('nopqrstuvwxyz', 50, 10, 0)
    #display.refresh()
    
    
    
    display.simulate()
    mem_used.print_ram_used()
    