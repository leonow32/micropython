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

# If the card is secured, you may need to perform the authetication first
# mif.authenticate(b"\xFF\xFF\xFF\xFF") # Default password
# mif.authenticate(b"\x11\x22\x33\x44") # Password from security_configure.py

debug_disable()
mif.dump()
