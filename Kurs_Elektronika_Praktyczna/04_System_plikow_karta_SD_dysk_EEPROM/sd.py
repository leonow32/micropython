# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import os
import machine
       
sd = machine.SDCard(slot=3, width=1, cs=13, miso=2, mosi=15, sck=14, freq=20000000)   # Płytka TTGO-T8 v1.8
#sd = machine.SDCard(slot=2, width=1, cs=5, miso=13, mosi=11, sck=12, freq=20000000)
vfs = os.VfsFat(sd)
os.mount(vfs, ".sd")    # znak / nie ma żadnego znaczenia i może być dowolny inny

print(os.listdir(""))
print(os.listdir("sd"))
