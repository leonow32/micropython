from machine import Pin, SPI
from time import sleep_ms
from gc import mem_free, mem_alloc, collect
from time import ticks_ms, ticks_us
import framebuf

WIDTH  = 320
HEIGHT = 240

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
led = Pin(39,  Pin.OUT, value=1)
spi = SPI(2, baudrate=40_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))

buffer = bytearray(WIDTH * HEIGHT * 2)
frame  = framebuf.FrameBuffer(buffer, WIDTH, HEIGHT, framebuf.RGB565)

def refresh():
    cs(0)
    

    
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
    
    write_cmd(0xC0);                # Power control 1
    write_data(0x23);               # VRH[5:0]
# 
    write_cmd(0xC1);                # Power control 2
    write_data(0x10);               # SAP[2:0]; BT[3:0]
# 
    write_cmd(0xC5);                # VCM control
    write_data(0x3e);               # Contrast
    write_data(0x28);
# 
    write_cmd(0xC7);                # VCM control2
    write_data(0x86);               # --

    write_cmd(0x36);                # Memory Access Control
#   write_data(0b00101000);         # MY=0 MX=0 MV=1 ML=0 BGR=1 MH=0 DUMMY DUMMY
    write_data(0b11101000);         # MY=1 MX=1 MV=1 ML=0 BGR=1 MH=0 DUMMY DUMMY
#   write_data(0b00101100);         # MY=0 MX=0 MV=1 ML=0 BGR=1 MH=1 DUMMY DUMMY

    write_cmd(0x3A);                # Pixel Format Set
    write_data(0x55);

#     write_cmd(0xB1);                # Frame Rate Control (In Normal Mode/Full Colors)
#     write_data(0x00);
#     write_data(0x18);
# 
#     write_cmd(0xB6);                # Display Function Control
#     write_data(0x08);
#     write_data(0b11100010);         # ISC[3:0]=2 GS=1 SS=0
#     write_data(0x27);
    
    write_cmd(0x2A)             # Col range 0..319
    write_data(0x00)
    write_data(0x00)
    write_data(0x01)
    write_data(0x3F)
    
    write_cmd(0x2B)             # Row range 0..239
    write_data(0x00)
    write_data(0x00)
    write_data(0x00)
    write_data(0xEF)
    

    write_cmd(0x11);                # Exit Sleep
#     sleep_ms(120);

    write_cmd(0x29);                # Display on

#     write_cmd(0x2C);                # Memory Write

def ram():
    print(f"Free: {gc.mem_free()}")
    print(f"Used: {gc.mem_alloc()}")

def color(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)
    
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

def rgb_demo():
    #           x1,  y1,   w,   h, color
    frame.rect(  0,   0,  20,   5, 0b1000000000000000, True)
    frame.rect(  0,  10,  20,   5, 0b0100000000000000, True)
    frame.rect(  0,  20,  20,   5, 0b0010000000000000, True)
    frame.rect(  0,  30,  20,   5, 0b0001000000000000, True)
    frame.rect(  0,  40,  20,   5, 0b0000100000000000, True)
    frame.rect(  0,  50,  20,   5, 0b0000010000000000, True)
    frame.rect(  0,  60,  20,   5, 0b0000001000000000, True)
    frame.rect(  0,  70,  20,   5, 0b0000000100000000, True)
    frame.rect(  0,  80,  20,   5, 0b0000000010000000, True)
    frame.rect(  0,  90,  20,   5, 0b0000000001000000, True)
    frame.rect(  0, 100,  20,   5, 0b0000000000100000, True)
    frame.rect(  0, 110,  20,   5, 0b0000000000010000, True)
    frame.rect(  0, 120,  20,   5, 0b0000000000001000, True)
    frame.rect(  0, 130,  20,   5, 0b0000000000000100, True)
    frame.rect(  0, 140,  20,   5, 0b0000000000000010, True)
    frame.rect(  0, 150,  20,   5, 0b0000000000000001, True)
    refresh()

def rainbow_demo():
    frame.rect(  0,   0, 320,  30, RED,    True)
    frame.rect(  0,  30, 320,  30, YELLOW, True)
    frame.rect(  0,  60, 320,  30, GREEN,  True)
    frame.rect(  0,  90, 320,  30, CYAN,   True)
    frame.rect(  0, 120, 320,  30, BLUE,   True)
    frame.rect(  0, 150, 320,  30, VIOLET, True)
    frame.rect(  0, 180, 320,  30, BLACK,  True)
    frame.rect(  0, 210, 320,  30, WHITE,  True)
    refresh()

def rainbow2_demo():
    start_time = ticks_us()
    
    column = 0
    step = 256 / (WIDTH / 5)
    
    # Red -> Yellow
    temp = 0
    for i in range(WIDTH / 5):
        frame.vline(column, 0, HEIGHT, color(255, temp, 0))
        temp += step
        column += 1
    
    # Yellow -> Green
    temp = 256
    for i in range(WIDTH / 5):
        frame.vline(column, 0, HEIGHT, color(temp, 255, 0))
        temp -= step
        column += 1
    
    # Green -> Cyan
    temp = 0
    for i in range(WIDTH / 5):
        frame.vline(column, 0, HEIGHT, color(0, 255, temp))
        temp += step
        column += 1
    
    # Cyan -> Blue
    temp = 256
    for i in range(WIDTH / 5):
        frame.vline(column, 0, HEIGHT, color(0, temp, 255))
        temp -= step
        column += 1
    
    # Blue -> Magenta
    temp = 0
    for i in range(WIDTH / 5):
        frame.vline(column, 0, HEIGHT, color(temp, 0, 255))
        temp += step
        column += 1
    
    work_time = (ticks_us() - start_time) / 1000
    print(f"Time: {work_time} ms")
    
    refresh()

def lines_demo(loops):
    from random import randrange
    
    x1 = 0
    y1 = 0
    colors = [RED, YELLOW, GREEN, CYAN, BLUE, VIOLET]
    
    start_time = ticks_ms()
    for i in range(loops):
        x2 = randrange(320)
        y2 = randrange(240)
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
    
    init(-175, 334500, -129, 254560)
    
    while True:
        if is_pressed():
            x = read_x()
            y = read_y()
            frame.pixel(x, y, colors[randrange(6)])
            refresh()

init()
frame.fill(BLACK)

frame.text("1234567890",  0,   0, WHITE)
frame.text("ABCDEFGHIJ",  0,  50, WHITE)
frame.text("abcdefghij",  0, 100, WHITE)
frame.pixel(  0,   0, WHITE)
frame.pixel(319,   0, WHITE)
frame.pixel(  0, 239, WHITE)
frame.pixel(319, 239, WHITE)

time_start = ticks_ms()
refresh()
time_end = ticks_ms()
print(f"Refresh time: {time_end-time_start} ms")

#rgb_demo()
#rainbow_demo()
#rainbow2_demo()
# lines_demo(100)
# pixels_demo(10000)
# touch_demo()

del buffer


