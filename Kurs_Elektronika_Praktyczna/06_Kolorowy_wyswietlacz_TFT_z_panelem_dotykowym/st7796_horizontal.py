import machine
import framebuf
import time

WIDTH   = const(480)
HEIGHT  = const(320)

RED     = const(0b000_00000_11111_000)
YELLOW  = const(0b111_00000_11111_111)
GREEN   = const(0b111_00000_00000_111)
CYAN    = const(0b111_11111_00000_111)
BLUE    = const(0b000_11111_00000_000)
MAGENTA = const(0b000_11111_11111_000)
WHITE   = const(0b111_11111_11111_111)
BLACK   = const(0b000_00000_00000_000)

class ST7796(framebuf.FrameBuffer):
    
    def __init__(self, spi, cs, dc, rst):
        self.spi = spi
        self.cs  = cs
        self.dc  = dc
        self.rst = rst
        self.cs.init(mode=machine.Pin.OUT, value=1)
        self.dc.init(mode=machine.Pin.OUT, value=1)
        self.rst.init(mode=machine.Pin.OUT, value=1)
        
        self.array = bytearray(WIDTH * HEIGHT * 2)
        super().__init__(self.array, WIDTH, HEIGHT, framebuf.RGB565)
        
        self.rst(0)
        time.sleep_ms(15)
        self.rst(1)
        time.sleep_ms(15)
        
        self.write_cmd(0x3A)             # COLMOD: Pixel Format Set
        self.write_data(0x05)            # 16-bit pixel format
        
        self.write_cmd(0x36)             # Memory Access Control
        self.write_data(0b11101100);     # MY=1 MX=1 MV=1 ML=0 BGR=1 MH=1 Dummy Dummy orientacja pozioma
        
        self.write_cmd(0x2B)             # Row range 0..319
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)
        
        self.write_cmd(0x2A)             # Col range 0..479
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xDF)
        
        self.write_cmd(0x11)             # Sleep Out
        self.write_cmd(0x29)             # Display ON
            
    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def write_cmd(self, data):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([data]))
        self.cs(1)
        
    def refresh(self):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([0x2C]))
        self.dc(1)
        self.spi.write(self.array)
        self.cs(1)
        
    def color(self, red, green, blue):
        red   = int(red)
        green = int(green)
        blue  = int(blue)
        
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        
        red    = red & 0xF8
        green1 = (green & 0xE0) >> 5
        green2 = (green & 0x1C) << 11
        blue   = (blue  & 0xF8) << 5
        color  = red | green1 | green2 | blue
        return color
    
    def print_char(self, font, char, x, y, color):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        width    = bitmap[0]
        height   = bitmap[1]
        space    = bitmap[2]
        offset_x = 0
        offset_y = 0
        
        for byte in bitmap[3:]:
            for bit in range(8):
                if byte & (1<<bit):
                    self.pixel(offset_x+x, offset_y+y+bit, color)
            
            offset_x += 1
            if offset_x == width:
                offset_x = 0
                offset_y += 8
            
        return width + space     

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
    
    def get_text_width(self, font, text):
        total = 0
        last_char_space = 0
        for char in text:
            bitmap = font.get(ord(char), font[0])
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space
