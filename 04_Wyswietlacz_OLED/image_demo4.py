from machine import Pin, I2C
import framebuf
import images4
import ssd1309
import mem_used
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)

start_time = time.ticks_us()
display.bitmap4(images4.ok_32x32,        0,  0)
display.bitmap4(images4.back_32x32,      0, 32)
display.bitmap4(images4.clock_32x32,    32,  0)
display.bitmap4(images4.settings_32x32, 32, 32)
display.bitmap4(images4.book_32x32,     64,  0)
display.bitmap4(images4.light_32x32,    64, 32)
display.bitmap4(images4.up_32x32,       96,  0)
display.bitmap4(images4.down_32x32,     96, 32)

# bg, fg = 0, 1
# palette = framebuf.FrameBuffer(bytearray(1), 1, 2, framebuf.MONO_VLSB)
# palette.pixel(1, 0, fg)
# palette.pixel(0, 0, bg)
# 
# new = bytearray(32*32//8)
# newbuf = framebuf.FrameBuffer(new, 32, 32, framebuf.MONO_VLSB)
# newbuf.blit(newbuf, images3.down_32x32[0], images3.down_32x32[0], -1, palette)
# 
# display.bitmap3(new,     96, 32)
#images.up_32x32[2]

# display.blit(images.world_128x64, 0, 0)
# display.blit(images.world_128x64, 0, 0, 0)  # tło przezroczyste

# display.blit(images.ep_logo_128x40, 0, 0)

end_time = time.ticks_us()
display.refresh()

print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()



