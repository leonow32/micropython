import framebuf
import mem_used

WIDTH   = const(128)
HEIGHT  = const(64)

class SIM(framebuf.FrameBuffer):
    
    def __init__(self):
        self.array = bytearray(WIDTH * HEIGHT // 8)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.MONO_VLSB)
            
    def refresh(self):
        self.simulate()
        
    def simulate(self):
        for y in range(HEIGHT):
            print(f"{y}\t", end="")
            for x in range(WIDTH):
                bit  = 1 << (y % 8)
                byte = self.array[(y // 8) * WIDTH + x]
                pixel = "#" if byte & bit else "."
                print(pixel, end="")
            print("")
            
    def print_char(self, font, char, x, y):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        buffer = framebuf.FrameBuffer(bitmap[3:], bitmap[1], bitmap[0], 0)
        self.blit(buffer, x, y)
        return bitmap[1] + bitmap[2]
        

    def print_text(self, font, text, x, y, align="L"):
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
            x += self.print_char(font, char, x, y)        
    
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
    display = SIM()
    
    array = bytearray(9 * 15)
    image = framebuf.FrameBuffer(array, 15, 9, framebuf.MONO_VLSB) # x, y
    array[0] = 0b10000000
    array[1] = 0b01000000
    array[2] = 0b00100000
    array[3] = 0b00010000
    array[4] = 0b00001000
    array[5] = 0b00000100
    array[6] = 0b00000010
    array[7] = 0b00000001
    array[8] = 0b10000000
    array[9] = 0b01000000
    array[10] = 0b00100000
    array[11] = 0b00010000
    array[12] = 0b00001000
    array[13] = 0b00000100
    array[14] = 0b00000010
    array[15] = 0b00000001
    display.blit(image, 0, 0)
#     
#     clock = bytearray(b'\x00\x00\x00\x00\x80\xc0`0\x18\x18\x8c\x0c\x06\x06\x06&&\x06\x06\x06\x0c\x8c\x18\x180`\xc0\x80\x00\x00\x00\x00\x00\xf0\xfc\x0f\x03\x80\x00\x04\x00\x00\x00\x00\x00\x00\x00\xff\xff\x80\x80\x80\x80\x00\x00\x00\x04\x00\x80\x03\x0f\xfc\xf0\x00\x00\x0f?\xf0\xc0\x01\x00 \x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x00\x00\x00 \x00\x01\xc0\xf0?\x0f\x00\x00\x00\x00\x00\x01\x03\x06\x0c\x18\x1810```dd```01\x18\x18\x0c\x06\x03\x01\x00\x00\x00\x00')
#     clock_buf = framebuf.FrameBuffer(clock, 32, 32, framebuf.MONO_VLSB)
#     display.blit(clock_buf, 0, 0)
    
#     display.blit(images.clock, -10, 5)
#     display.blit(images.test, 20, 30)
    
#     display.fill_rect(64, 0, 64, 64, 1)
    
    #for i in len(images.test):
    #    images.test[i] = ~images.test[i]
        
#     display.blit(images.test, 70, 30, 0, )
    display.refresh()
    
    
    #display.rect(0, 0, 128, 64, 1)
    #display.text('abcdefghijklm', 1, 2, 1)
#     display.text('nopqrstuvwxyz', 50, 10, 0)
    #display.refresh()
    
    
    
    display.simulate()
    mem_used.print_ram_used()
    
