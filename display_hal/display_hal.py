# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.26.1 ESP32 Pico
# MicroPython 1.27.0 ESP32 Pico
# MicroPython 1.27.0 Raspberry Pico 2

import framebuf

class DisplayHAL:
    
    @micropython.native
    def __init__(self, display):
        self.display  = display
        self.width    = display.width
        self.height   = display.height
        self._transp  = -1
        self._color_f = 1 if display.mono else 0xFFFF
        self._color_b = 0
        self._palette = framebuf.FrameBuffer(bytearray(4), 2, 1, framebuf.MONO_VLSB if display.mono else framebuf.RGB565)
        self._palette.pixel(1, 0, self._color_f)
        self._palette.pixel(0, 0, 0)
    
    def color_set(self, foreground, background=None):
        self._color_f = foreground
        
        if background is not None:
            self._color_b = background
            
        if self._color_f >= 0 and self._color_b >= 0:
            self._transp = -1
            self._palette.pixel(1, 0, self._color_f)
            self._palette.pixel(0, 0, self._color_b)
        elif self._color_f < 0 and self._color_b >= 0:
            self._transp = 0 if self._color_b else 1
            self._palette.pixel(1, 0, self._transp)
            self._palette.pixel(0, 0, self._color_b)
        elif self._color_f >= 0 and self._color_b < 0:
            self._transp = 0 if self._color_f else 1
            self._palette.pixel(1, 0, self._color_f)
            self._palette.pixel(0, 0, self._transp)
        else:
            self._transp = 0
            self._palette.pixel(1, 0, 0)
            self._palette.pixel(0, 0, 0)
    
    @micropython.viper
    def __str__(self):
        return f"DisplayHAL(display={self.display})"
    
    @micropython.viper
    def enable(self):
        self.display.enable()
        
    @micropython.viper
    def disable(self):
        self.display.disable()
    
    @micropython.viper
    def contrast_set(self, value):
        self.display.contrast_set(value)
        
    @micropython.viper
    def color(self, r, g, b):
        return self.display.color(r, g, b)
    
    @micropython.viper
    def refresh(self):
        self.display.refresh()
        
    @micropython.viper
    def simulate(self):
        self.display.simulate()
        
    @micropython.viper
    def pixel(self, x, y):
        self.display.pixel(x, y, self._color_f)
        
    @micropython.viper
    def line(self, x1, y1, x2, y2):
        self.display.line(x1, y1, x2, y2, self._color_f)
        
    @micropython.viper
    def hline(self, x, y, width):
        self.display.hline(x, y, width, self._color_f)
        
    @micropython.viper
    def vline(self, x, y, height):
        self.display.vline(x, y, h, self._color_f)
        
    @micropython.viper
    def rect(self, x, y, width, height):
        self.display.rect(x, y, width, height, self._color_f)
        
    @micropython.viper
    def fill_rect(self, x, y, width, height):
        self.display.fill_rect(x, y, width, height, self._color_f)
        
    @micropython.viper
    def fill(self):
        self.display.fill(self._color_f)
        
    @micropython.native
    def circle(self, x, y, radius, fill=False):
        self.display.ellipse(x, y, radius, radius, self._color_f, fill)
        
    @micropython.native
    def char(self, font, char, x, y, color=1):
        try:
            bitmap = font[ord(char)]
        except:
            bitmap = font[0]
            print(f"Char {char} doesn't exist in font")
        
        width  = bitmap[0]
        height = bitmap[1]
        space  = bitmap[2]
        
        if self.display.mono:
            if color:
                buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
            else:
                negative_bitmap = bitmap[:]
                for i in range(3, len(bitmap)):
                    negative_bitmap[i] = ~negative_bitmap[i]
                buffer = framebuf.FrameBuffer(negative_bitmap[3:], width, height, 0)
                self.display.rect(x-space, y, space, height, 1, True)
                self.display.rect(x+width, y, space, height, 1, True)
            self.display.blit(buffer, x, y)
        else:
            buffer = framebuf.FrameBuffer(bitmap[3:], width, height, 0)
            palette_array = bytearray(4)
            palette_framebuffer = framebuf.FrameBuffer(palette_array, 2, 1, framebuf.RGB565)
            palette_framebuffer.pixel(0, 0, self.display.color(0x12, 0x34, 0x56)) # background
            palette_framebuffer.pixel(1, 0, color) # foreground
            self.display.blit(buffer, x, y, self.display.color(0x12, 0x34, 0x56), palette_framebuffer)
            
        return width + space  
        
    @micropython.native
    def text(self, text, x, y, color, font=None, align="left"):
        if font:
            if align == "RIGHT":
                width = self.text_width(text, font)
                x = self.display.width - width
            elif align == "CENTER":
                width = self.text_width(text, font)
                x = self.display.width//2 - width//2
            elif align == "right":
                width = self.text_width(text, font)
                x = x - width + 1
            elif align == "center":
                width = self.text_width(text, font)
                x = x - width//2
            
            for char in text:
                x += self.char(font, char, x, y, color)
        else:
            self.display.text(text, x, y, color)
    
    @micropython.native
    def text_width(self, text, font):
        total = 0
        last_char_space = 0
        for char in text:
            bitmap = font.get(ord(char), font[0])
            total += bitmap[0]
            total += bitmap[2]
            last_char_space = bitmap[2]
        
        return total - last_char_space
            
    @micropython.native
    def image(self, bitmap, x: int, y: int) -> None:
        self.display.blit(bitmap, x, y, self._transp, self._palette)
        
    def image_old(self, bitmap, x, y, color=-1):
        if self.display.mono:
            self.display.blit(bitmap, x, y, color)
        else:
            palette_array = bytearray(4)
            palette_framebuffer = framebuf.FrameBuffer(palette_array, 2, 1, framebuf.RGB565)
            palette_framebuffer.pixel(0, 0, self.display.color(0x12, 0x34, 0x56)) # background
            palette_framebuffer.pixel(1, 0, color) # foreground
            self.display.blit(bitmap, x, y, self.display.color(0x12, 0x34, 0x56), palette_framebuffer)

if __name__ == "__main__":
    import mem_used
    import measure_time
    from machine import Pin, I2C, SPI
    
#     from dem128064e1 import *
    
#     from sh1106 import *
#     from sh1108 import *
    from display_hal.driver.ssd1309 import *
#     from ssd1351 import *
#     from ssd1363_spi import *
#     from ssd1363_spi_bw import *

    from display_hal.image_mono.down_32x32 import *
    from display_hal.image_mono.up_32x32 import *
    from display_hal.image_mono.ball_16x16 import *
    from display_hal.image_mono.chess_8x8 import *

    from display_hal.font.extronic16_unicode import *
    from display_hal.font.extronic16B_unicode import *

    i2c = I2C(0) # use default pinout and clock frequency
#     display = SH1106(i2c, address=0x3D, rotate=0, offset_x=2)
    display = SSD1309(i2c, address=0x3C, rotate=0)

#     spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0)
    
#     display = SH1108(spi, cs=Pin(4), dc=Pin(2), rotate=0, offset_x=16)
#     Pin(4, mode=Pin.OUT, value=1)
#     Pin(2, mode=Pin.OUT, value=1)
    
#     display = SSD1351(spi, cs=Pin(27), dc=Pin(15), rotate=0)
#     Pin(27, mode=Pin.OUT, value=1)
#     Pin(15, mode=Pin.OUT, value=1)

#     spi = SPI(1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(5), miso=None)
#     display = SSD1363_SPI(spi, cs=Pin(7), dc=Pin(6), rotate=0)
#     display = SSD1363_SPI_BW(spi, cs=Pin(7), dc=Pin(6), rotate=0)
#     display = SSD1363_SPI(spi, cs=Pin(9), dc=Pin(10), rotate=0)

#     spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
#     display = DEM128064E1(spi, cs=Pin(5), dc=Pin(6), rst=Pin(7))
    
#     from display_hal.driver.dem240064b import *
#     spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
#     display = DEM240064B(spi, cs0=Pin(5), cs1=Pin(8), dc=Pin(6), rst=Pin(7))
    
    dihal = DisplayHAL(display)
    print(dihal)
    
#     dihal.contrast_set(0xFF)
    
    measure_time.begin()
#     dihal.rect(0, 0, display.width, display.height, dihal.color(0xFF, 0xFF, 0xFF))
#     dihal.line(2, 2, display.width-3, display.height-3, dihal.color(0xFF, 0x00, 0x00))
#     dihal.circle(display.width//2, display.height//2, display.width//4-3, dihal.color(0x00, 0xFF, 0x00))
#     dihal.text('abcdefghijklm',  1,  2, dihal.color(0x00, 0xFF, 0xFF))
#     dihal.text('nopqrstuvwxyz',  1, 10, dihal.color(0x00, 0x00, 0xFF))
#     dihal.text("abcdefghijkl",  50, 20, dihal.color(0xFF, 0xFF, 0xFF), extronic16_unicode,  "center")
#     dihal.text("abcdefghijkl",  50, 40, dihal.color(0xFF, 0xFF, 0x00), extronic16B_unicode, "center")
#     dihal.image(up_32x32,       96,  0, dihal.color(0xFF, 0x00, 0x00))
#     dihal.image(down_32x32,     96, 32, dihal.color(0x00, 0xFF, 0x00))
    
    # Chessboard as a background
    dihal.color_set(1, 0)
    for x in range(0, dihal.width, 8):
        for y in range(0, dihal.height, 8):
            dihal.image(chess_8x8, x, y)
    
    # Row 0, Col 0 - foreground off, background off
    dihal.color_set(0, 0)
    dihal.image(ball_16x16, 20, 4)
    
    # Row 0, Col 1 - foreground off, background on (negative)
    dihal.color_set(0, 1)
    dihal.image(ball_16x16, 56, 4)
    
    # Row 0, Col 2 - foreground off, background transparent
    dihal.color_set(0, -1)
    dihal.image(ball_16x16, 92, 4)

    # Row 1, Col 0 - foreground on, background off
    dihal.color_set(1, 0)
    dihal.image(ball_16x16, 20, 24)
    
    # Row 1, Col 1 - foreground on, background on
    dihal.color_set(1, 1)
    dihal.image(ball_16x16, 56, 24)
    
    # Row 1, Col 2 - foreground on, background transparent
    dihal.color_set(1, -1)
    dihal.image(ball_16x16, 92, 24)

    # Row 2, Col 0 - foreground transparent, background off
    dihal.color_set(-1, 0)
    dihal.image(ball_16x16, 20, 44)
    
    # Row 2, Col 1 - foreground transparent, background on
    dihal.color_set(-1, 1)
    dihal.image(ball_16x16, 56, 44)
    
    # Row 2, Col 2 - foreground transparent, background transparent
    dihal.color_set(-1, -1)
    dihal.image(ball_16x16, 92, 44)

    measure_time.end("Rendering time:")
    
    measure_time.begin()
    dihal.refresh()
    measure_time.end("Refresh time:  ")
    
#     dihal.simulate()

    mem_used.print_ram_used()