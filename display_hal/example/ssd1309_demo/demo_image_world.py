# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import ssd1309
import mem_used
import time

from image.world_128x64 import *

i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency
display = ssd1309.SSD1309(i2c)

display.blit(world_128x64, 0, 0)

end_time = time.ticks_us()

display.refresh()

print(f"Time: {(end_time-start_time)/1000}")
mem_used.print_ram_used()



