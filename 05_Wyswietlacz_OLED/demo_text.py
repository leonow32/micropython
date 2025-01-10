from machine import Pin, I2C
import ssd1309
import mem_used

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)

display.rect(0, 0, 128, 64, 1)
display.text('abcdefghijklm', 1, 2, 1)
display.text('nopqrstuvwxyz', 1, 10, 1)
display.text('ABCDEFGHIJKLM', 1, 18, 1)
display.text('NOPQRSTUVWXYZ', 1, 26, 1)
display.text('0123456789+-*/', 1, 34, 1)
display.text('!@#$%^&*(),.<>?', 1, 42, 1)
display.refresh()
display.simulate()

mem_used.print_ram_used()