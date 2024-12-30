from machine import Pin, I2C
import framebuf
import ssd1309
import mem_used
import time

#dos16_F = bytearray(b'\x10\x08\x00\x04\xfc\xfcD\xe4\x0c\x1c\x00\x08\x0f\x0f\x08\x00\x00\x00\x00')
#dos16_j = bytearray(b'\x10\x08\x00\x00\x00\x00\x00 \xec\xec\x00\x000p@@\x7f?\x00')

dos16 = {
    "\x00": bytearray(b'\x10\x08\x00\xff\x01\x01\x01\x01\x01\x01\xff\xff\x80\x80\x80\x80\x80\x80\xff'),
    "F": bytearray(b'\x10\x08\x00\x04\xfc\xfcD\xe4\x0c\x1c\x00\x08\x0f\x0f\x08\x00\x00\x00\x00'),
    "j": bytearray(b'\x10\x08\x00\x00\x00\x00\x00 \xec\xec\x00\x000p@@\x7f?\x00'),
}

def print_char(screen, char, x, y):
    buf = framebuf.FrameBuffer(char[3:], char[1], char[0], framebuf.MONO_VLSB)
    screen.blit(buf, x, y)
    return char[1] + char[2]

def print_text(screen, text, x, y):
    for char in text:
        try:
            x += print_char(screen, dos16[char], x, y)
        except:
            x += print_char(screen, dos16["\x00"], x, y)
            print(f"Char {char} doesn't exist in font")
        

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
start_time = time.ticks_us()

#print_char(display, dos16["F"], 0, 0)
#print_char(display, dos16["j"], 8, 0)
print_text(display, "FFF\x00jjFjąFFF", 5, 20)

display.refresh()

end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
mem_used.print_ram_used()
