from machine import Pin, SPI

# Conversion coefficients for ST7796
AX = 273
BX = -469
AY = 172
BY = -149

# Conversion coefficients for ILI9341
# AX = -175
# BX = 334500
# AY = -129
# BY = 254560

touch_cs  = Pin(41, Pin.OUT, value=1)
touch_irq = Pin(1,  Pin.IN)
spi = SPI(1, baudrate=5_000_000, polarity=0, phase=0, sck=Pin(40), mosi=Pin(42), miso=Pin(2))

def init(ax, bx, ay, by):
    global AX
    global BX
    global AY
    global BY
    AX = ax
    BX = bx
    AY = ay
    BY = by

def is_pressed():
    if touch_irq() == 1:
        return False
    else:
        return True

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
