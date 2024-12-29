from machine import Pin, I2C
import images
import ssd1309
import mem_used
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_us()

# display.blit(images.ep_logo, 0, 0)
# display.blit(images.test, 10, 10)
display.blit(images.clock, 50, 20)
display.blit(images.dos16_F, 0, 0)
display.blit(images.dos16_j, 8, 0)

end_time = time.ticks_us()
display.refresh()


print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
