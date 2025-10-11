from machine import Pin, SPI
import st7796_horizontal as st7796
# import st7796_vertical as st7796

spi = SPI(2, baudrate=80_000_000, polarity=0, phase=0, sck=Pin(15), mosi=Pin(7), miso=None)
display = st7796.ST7796(spi, cs=Pin(4), dc=Pin(6), rst=Pin(5))

display.rect(0, 0, 128, 64, st7796.WHITE)
display.text('abcdefghijklm', 1, 2, st7796.RED)
display.text('nopqrstuvwxyz', 1, 10, st7796.YELLOW)
display.text('ABCDEFGHIJKLM', 1, 18, st7796.GREEN)
display.text('NOPQRSTUVWXYZ', 1, 26, st7796.CYAN)
display.text('0123456789+-*/', 1, 34, st7796.BLUE)
display.text('!@#$%^&*(),.<>?', 1, 42, st7796.MAGENTA)
display.refresh()
