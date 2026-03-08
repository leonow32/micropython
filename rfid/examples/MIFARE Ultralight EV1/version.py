from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
from rfid.mifare_ultralight_ev1 import MifareUltralightEV1
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)
iso = ISO_IEC_14443_3(pcd)
mif = MifareUltralightEV1(pcd)

iso.scan_and_select()

print("Get version")
version = mif.version_get()
debug("Version info", version)

print(f"- fixed header:          {version[0]:02X} ")

print(f"- vendor ID:             {version[1]:02X} ", end="")
if version[1]==0x04: print("NXP")

print(f"- product type:          {version[2]:02X} ", end="")
if version[2]==0x03: print("MIFARE Ultralight")

print(f"- product subtype:       {version[3]:02X} ", end="")
if version[3] == 0x01: print("15pF")
elif version[3] == 0x02: print("50pF")

print(f"- major product version: {version[4]:02X} ", end="")
if version[4]==0x01: print("EV1")

print(f"- minor product version: {version[5]:02X} ", end="")
if version[5]==0x00: print("0")

print(f"- storage size:          {version[6]:02X} ", end="")
if version[6] == 0x0B: print("MF0UL11, 48 bytes")
elif version[6] == 0x0E: print("MF0UL21, 128 bytes")

print(f"- protocol type:         {version[7]:02X} ", end="")
if version[7]==0x03: print("ISO/IEC 14443-3 compliant")
