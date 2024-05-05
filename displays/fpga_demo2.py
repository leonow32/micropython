from framebuf import *
from time import sleep_ms, ticks_ms
from machine import Pin, SPI

spi = SPI(2, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
print(spi)

cs = Pin(5, Pin.OUT)
dc = Pin(21, Pin.OUT, value=1)

# WIDTH  = 128
# HEIGHT = 96

WIDTH  = 160
HEIGHT = 120

array  = bytearray(WIDTH * HEIGHT // 8)
buffer = FrameBuffer(array, WIDTH, HEIGHT, MONO_VLSB)

def transmit():
    cs(0)
    spi.write(array)
    cs(1)

def lines_demo(loops):
    from random import randrange
    
    x1 = 0
    y1 = 0
    
    start_time = ticks_ms()
    for i in range(loops):
        x2 = randrange(WIDTH)
        y2 = randrange(HEIGHT)
        buffer.line(x1, y1, x2, y2, 1)
        transmit()
        x1 = x2
        y1 = y2
    
    end_time = ticks_ms()
    work_time = end_time - start_time
    frame_time = work_time / loops
    
    print(f"Frame time: {frame_time} ms")
    print(f"Frame rate: {1000/frame_time} fps")

def pixels_demo(loops):
    from random import randrange
    
    start_time = ticks_ms()
    for i in range(loops):
        x = randrange(WIDTH)
        y = randrange(HEIGHT)
        buffer.pixel(x, y, 0) # black pixel
        x = randrange(WIDTH)
        y = randrange(HEIGHT)
        buffer.pixel(x, y, 1) # white pixel
        transmit()
    
    end_time = ticks_ms()
    work_time = end_time - start_time
    frame_time = work_time / loops
    
    print(f"Frame time: {frame_time} ms")
    print(f"Frame rate: {1000/frame_time} fps")
    
#lines_demo(100)
pixels_demo(100000)
transmit()

