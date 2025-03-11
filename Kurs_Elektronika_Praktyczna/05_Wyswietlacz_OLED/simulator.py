import framebuf
import mem_used

WIDTH   = const(128)
HEIGHT  = const(64)

class SIM(framebuf.FrameBuffer):
    
    def __init__(self):
        self.array = bytearray(WIDTH * HEIGHT // 8)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.MONO_VLSB)
            
    def display_on(self, value):
        print(f"Display on: {value}")
    
    def contrast(self, value):
        print(f"Display contrast: {value}")
        
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
            for i in range(3, len(bitmap)): negative_bitmap[i] = ~negative_bitmap[i]
            buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
            self.rect(x-space, y, space, height, 1, True)
            self.rect(x+width, y, space, height, 1, True)
        
        self.blit(buffer, x, y)
        return width + space     

    def print_text(self, font, text, x, y, align="L", color=1):
        width = self.get_text_width(font, text)
        
        if   align == "R": x = WIDTH - width
        elif align == "C": x = WIDTH//2 - width//2
        elif align == "r": x = x - width + 1
        elif align == "c": x = x - width//2
        
        for char in text:
            x += self.print_char(font, char, x, y, color)
    
    def get_text_width(self, font, text):
        total = 0
        last_char_space = 0
        for char in text:
            try:
                bitmap = font[ord(char)]
            except:
                bitmap = font[0]
                print(f"Char {char} doesn't exist in font")
            
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space

if __name__ == "__main__":
    display = SIM()
    display.rect(0, 0, 128, 64, 1)
    display.text('abcdefghijklm', 1, 2, 1)
    display.text('nopqrstuvwxyz', 1, 10, 1)
    display.refresh()
    display.simulate()
    mem_used.print_ram_used()
