from machine import Pin, SPI
import mem_used

READ_X  = const(0b10010000)
READ_Y  = const(0b11010000)
READ_Z1 = const(0b10110000)
READ_Z2 = const(0b11000000)
THRESHOLD = const(600)
AVGERAGES = const(4)

# These are the values at lowest coordinates and maximum coordinates
# These values are used to map the touch screen over display
# These values can also be considered as calibration, a run-time calibration
# is more meaningful but as of now it is hard-coded
MIN_X = const(200)
MIN_Y = const(200)
MAX_X = const(1950)
MAX_Y = const(1860)
RES_X = const(480)
RES_Y = const(320)

cs  = Pin(41, Pin.OUT, value=1)
spi = SPI(1, baudrate=5_000_000, polarity=0, phase=0, sck=Pin(40), mosi=Pin(42), miso=Pin(2))

average_buf_x = []
average_buf_y = []

def command(cmd):
    tx = bytearray([cmd, 0, 0])
    rx = bytearray(3)
    cs(0)
    spi.write_readinto(tx, rx)
    cs(1)
    return rx[1] << 8 | rx[2]

def is_touched():
    z1 = command(READ_Z1) >> 3
    z2 = command(READ_Z2) >> 3
    z  = z1 + 4096 - z2
    #print(z)
    return z > THRESHOLD

def init():
    print(f"init()")

def calculate_coords_x(x):
    if(x > MIN_X):
        x -= MIN_X
    else:
        x = 0
    
    x = x * RES_X // (MAX_X - MIN_X)
    return x

def calculate_coords_y(y):
    if(y > MIN_Y):
        y -= MIN_Y
    else:
        y = 0
    
    y = y * RES_Y // (MAX_Y - MIN_Y)
    return y

def calculate_avg_x(x):
    
    if len(average_buf_x) == AVGERAGES:
        average_buf_x.pop(0)
        
    average_buf_x.append(x)
        
    sum = 0
    for item in average_buf_x:
        sum += item
        
    result = sum / len(average_buf_x)
    
    print(f"len: {len(average_buf_x)}, sum: {sum}, resukr: {result}")
    return int(result)

def calculate_avg_y(y):
    
    if len(average_buf_y) == AVGERAGES:
        average_buf_y.pop(0)
        
    average_buf_y.append(y)
        
    sum = 0
    for item in average_buf_y:
        sum += item
        
    result = sum / len(average_buf_y)
    #print(result)
    return int(result)

def read():
    
    if is_touched():
        command(READ_X)        # po co to?
        x = command(READ_X) >> 4
        y = command(READ_Y) >> 4
        
        x = calculate_coords_x(x)
        y = calculate_coords_y(y)
        
        x = calculate_avg_x(x)
        y = calculate_avg_y(y)
        
        if(len(average_buf_x) < AVGERAGES):
            return False
        else:
            return (x, y)
        
    else:
        average_buf_x.clear()
        average_buf_y.clear()
        return False

if __name__ == "__main__":
    res = read()
    print(res)
    mem_used.print_ram_used()