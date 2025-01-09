from machine import Pin, I2C
import images
import ssd1309
import mem_used
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)

start_time = time.ticks_us()
# display.blit(images.ep_logo_128x40, 0, 0)
display.blit(images.ok_32x32,        0,  0)
display.blit(images.back_32x32,      0, 32)
display.blit(images.clock_32x32,    32,  0)
display.blit(images.settings_32x32, 32, 32)
display.blit(images.book_32x32,     64,  0)
display.blit(images.light_32x32,    64, 32)
display.blit(images.up_32x32,       96,  0)
display.blit(images.down_32x32,     96, 32)

# display.blit(images.world_128x64, 0, 0)
# display.blit(images.world_128x64, 0, 0, 0)  # tło przezroczyste

end_time = time.ticks_us()
display.refresh()

print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
