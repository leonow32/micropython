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

debug_disable()

# Enables the counter and makes it possible to be read without authentication
mif.counter_configure(enable=True, protect=False)

# Enable the mirror of UID and counter. Place it byte 0 of page 200.
mif.mirror_configure(mode=0b11, page=200, byte=0)

# Check what's in page 200.
mif.dump()
