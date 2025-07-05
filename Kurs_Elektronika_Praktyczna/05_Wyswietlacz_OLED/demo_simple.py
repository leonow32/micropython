from machine import Pin, I2C
import mem_used
import ssd1309

i2c = I2C(0) # use default pinout and clock frequency
print(i2c)   # print pinout and clock frequency

display = ssd1309.SSD1309(i2c)
display.rect(0, 0, 128, 64, 1)
display.text('abcdefghijklm', 1, 2, 1)
display.text('nopqrstuvwxyz', 1, 10, 1)
display.refresh()
display.simulate()

mem_used.print_ram_used()
