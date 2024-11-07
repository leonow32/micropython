from machine import Pin, SPI, I2C
import ssd1309_i2c
import framebuf
import mem_used

WIDTH  = 128
HEIGHT = 64
ADDRESS = 0x3C

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

ssd1309_i2c.init(i2c)

array = bytearray(WIDTH * HEIGHT // 8)
fbuf = framebuf.FrameBuffer(array, WIDTH, HEIGHT, framebuf.MONO_VLSB)

fbuf.rect(0, 0, 128, 64, 1)
fbuf.text('artyrtybcdefghijklm', 1, 2, 1)
fbuf.text('nopqrstuvwxyz', 1, 10, 1)
fbuf.text('ABCDEFGHIJKLM', 1, 18, 1)
fbuf.text('NOPQRSTUVWXYZ', 1, 26, 1)
fbuf.text('0123456789+-*/', 1, 34, 1)
fbuf.text('!@#$%^&*(),.<>?', 1, 42, 1)

ssd1309_i2c.refresh(array)
mem_used.print_ram_used()