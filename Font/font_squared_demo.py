from machine import Pin, I2C
from font.squared16_unicode import *
from font.squared16B_unicode import *
# from mpy.squared16_unicode import *
# from mpy.squared16B_unicode import *
import framebuf
import ssd1309
import simulator
import mem_used
import time       

button = Pin(0, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
try:
    display = ssd1309.SSD1309(i2c)
except:
    display = simulator.SIM()

display.print_text(squared16_unicode,  "ABCDEFGHIJKL", 0, 0, "C")
display.print_text(squared16B_unicode, "ABCDEFGHIJKL", 0, 16, "C")
display.print_text(squared16_unicode,  "MNOPQRSTUVWXYZ", 0, 32, "C")
display.print_text(squared16B_unicode, "MNOPQRSTUVWXYZ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "abcdefghijkl", 0, 0, "C")
display.print_text(squared16B_unicode, "abcdefghijkl", 0, 16, "C")
display.print_text(squared16_unicode,  "mnopqrstuvwxyz", 0, 32, "C")
display.print_text(squared16B_unicode, "mnopqrstuvwxyz", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "aąäáàâåāæcćčçdďđ", 0, 0, "C")
display.print_text(squared16B_unicode, "aąäáàâåāæcćčçdďđ", 0, 16, "C")
display.print_text(squared16_unicode,  "eęéěèêëēėgğģiíîïīiįkķ", 0, 32, "C")
display.print_text(squared16B_unicode, "eęéěèêëēėgğģiíîïīiįkķ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "lłļnńňņñoóöõôørřsśšş", 0, 0, "C")
display.print_text(squared16B_unicode, "lłļnńňņñoóöõôørřsśšş", 0, 16, "C")
display.print_text(squared16_unicode,  "tťuüúůûùūųyýÿzźżžß", 0, 32, "C")
display.print_text(squared16B_unicode, "tťuüúůûùūųyýÿzźżžß", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "@0123456789.,:;+-*/", 0, 0, "C")
display.print_text(squared16B_unicode, "@0123456789.,:;+-*/", 0, 16, "C")
display.print_text(squared16_unicode,  "!¡?¿#$%^&*(){}[]<>", 0, 32, "C")
display.print_text(squared16B_unicode, "!¡?¿#$%^&*(){}[]<>", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "AĄÄÁÀÂÅĀÆCĆČÇ", 0, 0, "C")
display.print_text(squared16B_unicode, "AĄÄÁÀÂÅĀÆCĆČÇ", 0, 16, "C")
display.print_text(squared16_unicode,  "DĎĐEĘÉĚÈÊËĒĖGĞĢ", 0, 32, "C")
display.print_text(squared16B_unicode, "DĎĐEĘÉĚÈÊËĒĖGĞĢ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "IÍÎÏĪİĮKĶLŁĻNŃŇŅÑ", 0, 0, "C")
display.print_text(squared16B_unicode, "IÍÎÏĪİĮKĶLŁĻNŃŇŅÑ", 0, 16, "C")
display.print_text(squared16_unicode,  "OÓÖÕÔØRŘ", 0, 32, "C")
display.print_text(squared16B_unicode, "OÓÖÕÔØRŘ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "SŚŠŞTŤUÜÚŮÛÙŪŲ", 0, 0, "C")
display.print_text(squared16B_unicode, "SŚŠŞTŤUÜÚŮÛÙŪŲ", 0, 16, "C")
display.print_text(squared16_unicode,  "YÝŸZŹŻŽß", 0, 32, "C")
display.print_text(squared16B_unicode, "YÝŸZŹŻŽß", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "АБВГДЕЁЖЗИЙ", 0, 0, "C")
display.print_text(squared16B_unicode, "АБВГДЕЁЖЗИЙ", 0, 16, "C")
display.print_text(squared16_unicode,  "КЛМНОПРСТУФ", 0, 32, "C")
display.print_text(squared16B_unicode, "КЛМНОПРСТУФ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "ХЦЧШЩЪЫЬЭЮЯ", 0, 0, "C")
display.print_text(squared16B_unicode, "ХЦЧШЩЪЫЬЭЮЯ", 0, 16, "C")
display.print_text(squared16_unicode,  "ҐЄІЇЋЏЂЈЉЊ", 0, 32, "C")
display.print_text(squared16B_unicode, "ҐЄІЇЋЏЂЈЉЊ", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "абвгдеёжзий", 0, 0, "C")
display.print_text(squared16B_unicode, "абвгдеёжзий", 0, 16, "C")
display.print_text(squared16_unicode,  "клмнопрстуф", 0, 32, "C")
display.print_text(squared16B_unicode, "клмнопрстуф", 0, 48, "C")
display.refresh()

time.sleep_ms(100)
while button(): pass
display.fill(0)
display.print_text(squared16_unicode,  "хцчшщъыьэюя", 0, 0, "C")
display.print_text(squared16B_unicode, "хцчшщъыьэюя", 0, 16, "C")
display.print_text(squared16_unicode,  "ґєіїћџђјљњ", 0, 32, "C")
display.print_text(squared16B_unicode, "ґєіїћџђјљњ", 0, 48, "C")
display.refresh()

mem_used.print_ram_used()

