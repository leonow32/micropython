from machine import Pin, I2C
import ssd1309
import mem_used
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_ms()



display.refresh()

end_time = time.ticks_ms()
print(f"Work time: {end_time-start_time} ms")
mem_used.print_ram_used()
