from machine import Pin, SPI
from time import sleep_ms
from gc import mem_free, mem_alloc, collect
from time import ticks_ms
import framebuf

RED    = 0b000_00000_11111_000
YELLOW = 0b111_00000_11111_111
GREEN  = 0b111_00000_00000_111
CYAN   = 0b111_11111_00000_111
BLUE   = 0b000_11111_00000_000
VIOLET = 0b000_11111_11111_000
WHITE  = 0b111_11111_11111_111
BLACK  = 0b000_00000_00000_000

cs  = Pin(17, Pin.OUT, value=1)
dc  = Pin(15, Pin.OUT, value=1)
rst = Pin(16, Pin.OUT, value=1)
led = Pin(5,  Pin.OUT, value=1)
spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))

buffer = bytearray(480*320*2)
frame  = framebuf.FrameBuffer(buffer, 480, 320, framebuf.RGB565)

def refresh():
    cs(0)
    
    dc(0)
    spi.write(bytearray([0x2B]))
    dc(1)
    spi.write(bytearray([0x00, 0x00, 0x01, 0x3F]))
    
    dc(0)
    spi.write(bytearray([0x2A]))
    dc(1)
    spi.write(bytearray([0x00, 0x00, 0x01, 0xDF]))
    
    dc(0)
    spi.write(bytearray([0x2C]))
    dc(1)
    spi.write(buffer)
    
    cs(1)

def write_data(data):
    dc(1)
    cs(0)
    spi.write(bytearray([data]))
    cs(1)
    
def write_cmd(data):
    dc(0)
    cs(0)
    spi.write(bytearray([data]))
    cs(1)
        
def init():
    rst(0)
    sleep_ms(15)
    rst(1)
    sleep_ms(15)
    
    write_cmd(0xF0)             # Command Set Control
    write_data(0xC3)            # Enable command 2 part I
    
    write_cmd(0xF0)             # Command Set Control
    write_data(0x96)            # Enable command 2 part II
        
    write_cmd(0x3A)             # COLMOD: Pixel Format Set
    write_data(0x05)            # 16-bit pixel format
    
    write_cmd(0xB0)             # Interface Mode Control
    write_data(0x80)            # SPI Enable
    
    write_cmd(0xB6)             # Display Function Control
    write_data(0x00)
#   write_data(0b00000010)      # ISC[3:0]=2 GS=0 SS=0
#   write_data(0b01000010)      # ISC[3:0]=2 GS=1 SS=0 (mirror Y)
    write_data(0b11100010);         # ISC[3:0]=2 GS=1 SS=0
    
    
    write_cmd(0xB5)             # Blanking Porch Control
    write_data(0x02)
    write_data(0x03)
    write_data(0x00)
    write_data(0x04)
    
    write_cmd(0xB1)             # Frame Rate Control (In Normal Mode/Full Colors)
    write_data(0x80)
    write_data(0x10)
    
    write_cmd(0xB4)             # Display Inversion Control
    write_data(0x00)
    
    write_cmd(0xB7)
    write_data(0xC6)
    
    write_cmd(0xC5)
    write_data(0x24)
    
    write_cmd(0xE4)             # UNDOCUMMENTED
    write_data(0x31)
    
    write_cmd(0xE8)             # Display Output
    write_data(0x40)
    write_data(0x8A)
    write_data(0x00)
    write_data(0x00)
    write_data(0x29)
    write_data(0x19)
    write_data(0xA5)
    write_data(0x33)
    
    write_cmd(0xC2)             # Power control 3
    
    write_cmd(0xA7)             # UNDOCUMMENTED
     
    write_cmd(0xE0)             # Positive Gamma Control
    write_data(0xF0)
    write_data(0x09)
    write_data(0x13)
    write_data(0x12)
    write_data(0x12)
    write_data(0x2B)
    write_data(0x3C)
    write_data(0x44)
    write_data(0x4B)
    write_data(0x1B)
    write_data(0x18)
    write_data(0x17)
    write_data(0x1D)
    write_data(0x21)
     
    write_cmd(0XE1)             # Negative Gamma Control
    write_data(0xF0)
    write_data(0x09)
    write_data(0x13)
    write_data(0x0C)
    write_data(0x0D)
    write_data(0x27)
    write_data(0x3B)
    write_data(0x44)
    write_data(0x4D)
    write_data(0x0B)
    write_data(0x17)
    write_data(0x17)
    write_data(0x1D)
    write_data(0x21)
     
    write_cmd(0x36)             # Memory Access Control
#   write_data(0x48)
    write_data(0b00101100);     # MY=0 MX=0 MV=1 ML=0 MH=1 BGR=1
    
    write_cmd(0xF0)             # Command Set Control
    write_data(0xC3)
    
    write_cmd(0xF0)             # Command Set Control
    write_data(0x69)
    
    write_cmd(0x13)             # Normal Display Mode ON
    write_cmd(0x11)             # Sleep Out
    write_cmd(0x29)             # Display ON

def ram():
    print(f"Free: {gc.mem_free()}")
    print(f"Used: {gc.mem_alloc()}")

def color(red, green, blue):
    red    = red & 0xF8
    green1 = (green & 0xE0) >> 5
    green2 = (green & 0x1C) << 11
    blue   = (blue & 0xF8) << 5
    color  = red | green1 | green2 | blue
    return color

def rgb_demo():
    #           x1,  y1,    w,   h, color
    frame.rect(  0,   0,  100,   8, 0b1000000000000000, True)
    frame.rect(  0,  10,  100,   8, 0b0100000000000000, True)
    frame.rect(  0,  20,  100,   8, 0b0010000000000000, True)
    frame.rect(  0,  30,  100,   8, 0b0001000000000000, True)
    frame.rect(  0,  40,  100,   8, 0b0000100000000000, True)
    frame.rect(  0,  50,  100,   8, 0b0000010000000000, True)
    frame.rect(  0,  60,  100,   8, 0b0000001000000000, True)
    frame.rect(  0,  70,  100,   8, 0b0000000100000000, True)
    frame.rect(  0,  80,  100,   8, 0b0000000010000000, True)
    frame.rect(  0,  90,  100,   8, 0b0000000001000000, True)
    frame.rect(  0, 100,  100,   8, 0b0000000000100000, True)
    frame.rect(  0, 110,  100,   8, 0b0000000000010000, True)
    frame.rect(  0, 120,  100,   8, 0b0000000000001000, True)
    frame.rect(  0, 130,  100,   8, 0b0000000000000100, True)
    frame.rect(  0, 140,  100,   8, 0b0000000000000010, True)
    frame.rect(  0, 150,  100,   8, 0b0000000000000001, True)
    refresh()

def rainbow_demo():
    frame.rect(  0,   0, 480,  40, RED,    True)
    frame.rect(  0,  40, 480,  40, YELLOW, True)
    frame.rect(  0,  80, 480,  40, GREEN,  True)
    frame.rect(  0, 120, 480,  40, CYAN,   True)
    frame.rect(  0, 160, 480,  40, BLUE,   True)
    frame.rect(  0, 200, 480,  40, VIOLET, True)
    frame.rect(  0, 240, 480,  40, BLACK,  True)
    frame.rect(  0, 280, 480,  40, WHITE,  True)
    refresh()
    
def lines_demo(loops):
    from random import randrange
    
    x1 = 0
    y1 = 0
    colors = [RED, YELLOW, GREEN, CYAN, BLUE, VIOLET]
    
    start_time = ticks_ms()
    for i in range(loops):
        x2 = randrange(480)
        y2 = randrange(320)
        frame.line(x1, y1, x2, y2, colors[randrange(6)])
        refresh()
        x1 = x2
        y1 = y2
    
    end_time = ticks_ms()
    work_time = end_time - start_time
    frame_time = work_time / loops
    
    print(f"Frame time: {frame_time} ms")
    print(f"Frame rate: {1000/frame_time} fps")

def pixels_demo(loops):
    from random import randrange
    colors = [RED, YELLOW, GREEN, CYAN, BLUE, VIOLET]
    
    start_time = ticks_ms()
    for i in range(loops):
        x = randrange(480)
        y = randrange(320)
        frame.pixel(x, y, colors[randrange(6)])
        refresh()
    
    end_time = ticks_ms()
    work_time = end_time - start_time
    frame_time = work_time / loops
    
    print(f"Frame time: {frame_time} ms")
    print(f"Frame rate: {1000/frame_time} fps")

def touch_demo():
    from xpt2046_demo import init, read_x, read_y, is_pressed
    from random import randrange
    colors = [RED, YELLOW, GREEN, CYAN, BLUE, VIOLET]
    
    init(273, -442, 172, -159)
    
    while True:
        if is_pressed():
            x = read_x()
            y = read_y()
            frame.pixel(x, y, colors[randrange(6)])
            refresh()

init()
frame.fill(BLACK)

frame.pixel(20, 20, WHITE)
frame.pixel(460, 20, YELLOW)
frame.pixel(20, 300, RED)
frame.pixel(460, 300, GREEN)

# frame.text("1234567890", 50, 100, WHITE)

time_start = ticks_ms()
refresh()
time_end = ticks_ms()
print(f"Refresh time: {time_end-time_start} ms")

#rgb_demo()
rainbow_demo()
#lines_demo(100000)
#pixels_demo(10000)
#touch_demo()

del buffer



