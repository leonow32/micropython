from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
from rfid.ntag21x import NTAG21X
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)
iso = ISO_IEC_14443_3(pcd)
mif = NTAG21X(pcd)

iso.scan_and_select()

print("Get version")
version = mif.version_get()
debug("Version info", version)

print(f"- fixed header:          {version[0]:02X} ")

print(f"- vendor ID:             {version[1]:02X} ", end="")
if version[1]==0x04: print("NXP")
else: print("unknown")

print(f"- product type:          {version[2]:02X} ", end="")
if version[2]==0x04: print("NTAG")
else: print("unknown")

print(f"- product subtype:       {version[3]:02X} ", end="")
if version[3] == 0x02: print("50pF")
else: print("unknown")

print(f"- major product version: {version[4]:02X} ", end="")
if version[4]==0x01: print("1")
else: print("unknown")

print(f"- minor product version: {version[5]:02X} ", end="")
if version[5]==0x00: print("V0")
else: print("unknown")

print(f"- storage size:          {version[6]:02X} ", end="")
if version[6] == 0x0F: print("NTAG213, 144 bytes")
elif version[6] == 0x11: print("NTAG215, 504 bytes")
elif version[6] == 0x13: print("NTAG216, 888 bytes")
else: print("unknown")

print(f"- protocol type:         {version[7]:02X} ", end="")
if version[7]==0x03: print("ISO/IEC 14443-3 compliant")
else: print("unknown")
