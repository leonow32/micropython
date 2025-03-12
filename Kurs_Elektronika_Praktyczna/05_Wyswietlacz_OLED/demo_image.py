# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import ssd1309
import mem_used
import time

from image.back_32x32 import *
from image.book_32x32 import *
from image.cancel_32x32 import *
from image.clock_32x32 import *
from image.down_32x32 import *
from image.ep_logo_128x40 import *
from image.hand_32x32 import *
from image.light_32x32 import *
from image.ok_32x32 import *
from image.settings_32x32 import *
from image.square_8x16 import *
from image.test_16x16 import *
from image.up_32x32 import *
from image.world_128x64 import *

i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency
display = ssd1309.SSD1309(i2c)

start_time = time.ticks_us()
display.blit(ok_32x32,        0,  0)
display.blit(back_32x32,      0, 32)
display.blit(clock_32x32,    32,  0)
display.blit(settings_32x32, 32, 32)
display.blit(book_32x32,     64,  0)
display.blit(light_32x32,    64, 32)
display.blit(up_32x32,       96,  0)
display.blit(down_32x32,     96, 32)

# display.blit(world_128x64, 0, 0)
# display.blit(world_128x64, 0, 0, 0)  # tło przezroczyste

# display.blit(ep_logo_128x40, 0, 0)

end_time = time.ticks_us()
display.refresh()

mem_used.print_ram_used()


