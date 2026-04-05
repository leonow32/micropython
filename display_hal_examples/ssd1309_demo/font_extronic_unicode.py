# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# MicroPython 1.27.0 ESP32 Pico

from machine import I2C
from display_hal.display_hal import *
from display_hal.driver.ssd1309 import *

from display_hal.font.extronic16_unicode import *
from display_hal.font.extronic16B_unicode import *

import mem_used
import measure_time   

i2c     = I2C(0) # use default pinout and clock frequency
display = SSD1309(i2c, rotate=False, address=0x3C)
dihal   = DisplayHAL(display)
print(dihal)

dihal.text("ABCDEFGHIJKL",   0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("ABCDEFGHIJKL",   0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("MNOPQRSTUVWXYZ", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("MNOPQRSTUVWXYZ", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("abcdefghijkl",   0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("abcdefghijkl",   0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("mnopqrstuvwxyz", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("mnopqrstuvwxyz", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("aąäáàâåāæcćčçdďđ",      0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("aąäáàâåāæcćčçdďđ",      0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("eęéěèêëēėgğģiíîïīiįkķ", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("eęéěèêëēėgğģiíîïīiįkķ", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("lłļnńňņñoóöõôørřsśšş", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("lłļnńňņñoóöõôørřsśšş", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("tťuüúůûùūųyýÿzźżžß",   0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("tťuüúůûùūųyýÿzźżžß",   0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()

dihal.refresh()
input("Press enter")
dihal.fill(0)
dihal.text("@0123456789.,:;+-*/", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("@0123456789.,:;+-*/", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("!¡?¿#$%^&*(){}[]<>",  0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("!¡?¿#$%^&*(){}[]<>",  0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("AĄÄÁÀÂÅĀÆCĆČÇ",   0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("AĄÄÁÀÂÅĀÆCĆČÇ",   0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("DĎĐEĘÉĚÈÊËĒĖGĞĢ", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("DĎĐEĘÉĚÈÊËĒĖGĞĢ", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("IÍÎÏĪİĮKĶLŁĻNŃŇŅÑ", 0, 0,  1, extronic16_unicode, "CENTER")
dihal.text("IÍÎÏĪİĮKĶLŁĻNŃŇŅÑ", 0, 16, 1, extronic16B_unicode,"CENTER")
dihal.text("OÓÖÕÔØRŘ",          0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("OÓÖÕÔØRŘ",          0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("SŚŠŞTŤUÜÚŮÛÙŪŲ", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("SŚŠŞTŤUÜÚŮÛÙŪŲ", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("YÝŸZŹŻŽß",       0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("YÝŸZŹŻŽß",       0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("АБВГДЕЁЖЗИЙ", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("АБВГДЕЁЖЗИЙ", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("КЛМНОПРСТУФ", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("КЛМНОПРСТУФ", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("ХЦЧШЩЪЫЬЭЮЯ", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("ХЦЧШЩЪЫЬЭЮЯ", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("ҐЄІЇЋЏЂЈЉЊ",  0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("ҐЄІЇЋЏЂЈЉЊ",  0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("абвгдеёжзий", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("абвгдеёжзий", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("клмнопрстуф", 0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("клмнопрстуф", 0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

dihal.fill(0)
dihal.text("хцчшщъыьэюя", 0, 0,  1, extronic16_unicode,  "CENTER")
dihal.text("хцчшщъыьэюя", 0, 16, 1, extronic16B_unicode, "CENTER")
dihal.text("ґєіїћџђјљњ",  0, 32, 1, extronic16_unicode,  "CENTER")
dihal.text("ґєіїћџђјљњ",  0, 48, 1, extronic16B_unicode, "CENTER")
dihal.refresh()
input("Press enter")

mem_used.print_ram_used()
