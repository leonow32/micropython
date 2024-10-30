from machine import Pin, SPI

READ_X  = 0b10010000
READ_Y  = 0b11010000
READ_Z1 = 0b10110000
READ_Z2 = 0b11000000
THRESHOLD  = 400
AVGERAGEST = 4

# These are the values at lowest coordinates and maximum coordinates
# These values are used to map the touch screen over display
# These values can also be considered as calibration, a run-time calibration
# is more meaningful but as of now it is hard-coded
MIN_X = 200
MIN_Y = 200
MAX_X = 1950
MAX_Y = 1860
RES_X = 480
RES_Y = 320

cs  = Pin(41, Pin.OUT, value=1)
irq = Pin(1, Pin.IN)
spi = SPI(1, baudrate=5_000_000, polarity=0, phase=0, sck=Pin(40), mosi=Pin(42), miso=Pin(2))

def command(cmd):
    tx = bytearray([cmd, 0, 0])
    rx = bytearray(3)
    cs(0)
    spi.write_readinto(tx, rx)
    cs(1)
    return (rx[1] << 8 | rx[2]) >> 4

def is_touched():
    return irq() == False
    #res = (irq() == False)
    #print(f"is_touched() = {res}")
    #pass

def init():
    print(f"init()")

def calculate_x(x):
    if(x > MIN_X):
        x -= MIN_X
    else:
        x = 0
    
    x = x * RES_X // (MAX_X - MIN_X)
    return x

def calculate_y(y):
    if(y > MIN_Y):
        y -= MIN_Y
    else:
        y = 0
    
    y = y * RES_Y // (MAX_Y - MIN_Y)
    return y

def read():
    x = 0
    y = 0
    count = 0
    
    for i in range(5):
        if is_touched():
            x += calculate_x(command(READ_X))
            y += calculate_y(command(READ_Y))
            count += 1
        else:
            break
    
    if count:
        x = x // count
        y = y // count
        return (x, y)
    else:
        return False

"""
def read_x_raw():
    buffer = bytearray(b'\x90\x00\x00')
    touch_cs(0)
    spi.write_readinto(buffer, buffer)
    touch_cs(1)
    result = (buffer[1] << 8 | buffer[2]) >> 4
    return result

def read_y_raw():
    buffer = bytearray(b'\xD0\x00\x00')
    touch_cs(0)
    spi.write_readinto(buffer, buffer)
    touch_cs(1)
    result = (buffer[1] << 8 | buffer[2]) >> 4
    return result

def read_x():
    x = read_x_raw()
    x = (x * AX + BX) // 1000
    return x

def read_y():
    y = read_y_raw()
    y = (y * AY + BY) // 1000
    return y

def touch_demo():
    if is_pressed():
        x = read_x()
        y = read_y()
        print(f"x = {x} \t y = {y}")
"""
