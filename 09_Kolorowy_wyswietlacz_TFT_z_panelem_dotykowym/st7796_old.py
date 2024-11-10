from micropython import const
import mem_used
import time
import framebuf
import ft6336
from machine import Pin, SPI, PWM, I2C

WIDTH  = const(320)
HEIGHT = const(480)

RED    = const(0b000_00000_11111_000)
YELLOW = const(0b111_00000_11111_111)
GREEN  = const(0b111_00000_00000_111)
CYAN   = const(0b111_11111_00000_111)
BLUE   = const(0b000_11111_00000_000)
VIOLET = const(0b000_11111_11111_000)
WHITE  = const(0b111_11111_11111_111)
BLACK  = const(0b000_00000_00000_000)

#cs  = Pin(17, Pin.OUT, value=1)
cs  = Pin(17, Pin.OUT, value=1)
dc  = Pin(15, Pin.OUT, value=1)
rst = Pin(16, Pin.OUT, value=1)
#led = PWM(Pin(5), freq=10000, duty=1023)
#spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(6), miso=Pin(4))

buffer = bytearray(WIDTH*HEIGHT*2)
frame  = framebuf.FrameBuffer(buffer, WIDTH, HEIGHT, framebuf.RGB565)

def refresh():
    cs(0)
    dc(0)
    spi.write(bytes([0x2C]))
    dc(1)
    spi.write(buffer)
    cs(1)

def write_data(data):
    dc(1)
    cs(0)
    spi.write(bytes([data]))
    cs(1)
    
def write_cmd(data):
    dc(0)
    cs(0)
    spi.write(bytes([data]))
    cs(1)
        
def init():
    rst(0)
    time.sleep_ms(15)
    rst(1)
    time.sleep_ms(15)
    
    write_cmd(0x3A)             # COLMOD: Pixel Format Set
    write_data(0x05)            # 16-bit pixel format
     
    # orientacja pionowa
    write_cmd(0x36)             # Memory Access Control
    write_data(0b01001000);     # MY=0 MX=1 MV=0 ML=0 BGR=1 MH=0 Dummy Dummy orientacja pionowa 

    """
    # orientacja pozioma
    write_cmd(0x36)             # Memory Access Control
    write_data(0b11101100);     # MY=1 MX=1 MV=1 ML=0 BGR=1 MH=1 Dummy Dummy orientacja pozioma
    
    write_cmd(0x2B)             # Row range 0..319
    write_data(0x00)
    write_data(0x00)
    write_data(0x01)
    write_data(0x3F)
    
    write_cmd(0x2A)             # Col range 0..479
    write_data(0x00)
    write_data(0x00)
    write_data(0x01)
    write_data(0xDF)
    """
    
    write_cmd(0x11)             # Sleep Out
    write_cmd(0x29)             # Display ON

def color(red, green, blue):
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
    blue   = (blue & 0xF8) << 5
    color  = red | green1 | green2 | blue
    return color

def rainbow_demo():
    start_time = time.ticks_us()
    
    row = 0
    step = 256 / (HEIGHT // 5)
    
    # Red -> Yellow
    temp = 0
    for i in range(HEIGHT // 5):
        frame.hline(0, row, WIDTH, color(255, temp, 0))
        temp += step
        row += 1
    
    # Yellow -> Green
    temp = 256
    for i in range(HEIGHT // 5):
        frame.hline(0, row, WIDTH, color(temp, 255, 0))
        temp -= step
        row += 1
    
    # Green -> Cyan
    temp = 0
    for i in range(HEIGHT // 5):
        frame.hline(0, row, WIDTH, color(0, 255, temp))
        temp += step
        row += 1
    
    # Cyan -> Blue
    temp = 256
    for i in range(HEIGHT // 5):
        frame.hline(0, row, WIDTH, color(0, temp, 255))
        temp -= step
        row += 1
    
    # Blue -> Magenta
    temp = 0
    for i in range(HEIGHT // 5):
        frame.hline(0, row, WIDTH, color(temp, 0, 255))
        temp += step
        row += 1
    
    work_time = (time.ticks_us() - start_time) / 1000    
    frame.text(f"Czas: {work_time}ms", 10, 10, BLACK) 
    refresh()

def draw_point(result_tuple):
    x, y, pressed = result_tuple
    print(f"{x:3d} {y:3d} {pressed}")
    if(pressed):
        frame.pixel(x, y, YELLOW)
    else:
        frame.pixel(x, y, RED)
    refresh()
        
def touch_demo():
    print("touch_demo")
    frame.fill(BLACK)
    refresh()
    
    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    touch = ft6336.FT6336(i2c, 20, draw_point)


if __name__ == "__main__":
    init()
    #rainbow_demo()
    touch_demo()

    #del buffer
    mem_used.print_ram_used()

