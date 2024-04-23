from machine import Pin, SPI
import ssd1306

# spi1 = SPI(1, baudrate=1_000_000, polarity=1, phase=1, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# display = ssd1306.SSD1306_SPI(width=128, height=64, spi=spi1, dc=Pin(25), res=Pin(26), cs=Pin(5))

spi2 = SPI(1, baudrate=27_000_000, polarity=0, phase=0, sck=Pin(0), mosi=Pin(4), miso=Pin(25))
display = ssd1306.SSD1306_SPI(width=128, height=64, spi=spi2, dc=Pin(15), res=Pin(2), cs=Pin(13))

display.rect(0,0,127,63,1)
display.text('abcdefghijklm', 1, 2, 1)
display.text('nopqrstuvwxyz', 1, 10, 1)
display.text('ABCDEFGHIJKLM', 1, 18, 1)
display.text('NOPQRSTUVWXYZ', 1, 26, 1)
display.text('0123456789+-*/', 1, 34, 1)
display.text('!@#$%^&*(),.<>?', 1, 42, 1)
#display.text('DUPA', 0, 3, 1)
#display.contrast(255)
display.show()