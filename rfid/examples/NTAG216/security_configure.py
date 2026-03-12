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

# If the card is already secured, we need to authenticate first. b"\xFF\xFF\xFF\xFF" is the default password.
# pack = mif.authenticate(b"\xFF\xFF\xFF\xFF")
pack = mif.authenticate(b"\x11\x22\x33\x44")

# You should verify of PACK returned by the card matches with PACK that you expect
debug("PACK", pack)

# Configure the securyty features
# try_times=7 - if wrong password is entered for 7 times, the card will lock and authentication will be never possible
# address=10 - All memory blocks starting from 10 and beyond will require authentication
# mode=1 - authentication is required for read and write
# mif.security_configure(password=b"\x11\x22\x33\x44", pack=b"\xAB\xCD", try_times=7, address=10, mode=1)

# Default configuration
mif.security_configure(password=b"\xFF\xFF\xFF\xFF", pack=b"\x00\x00", try_times=0, address=0xFF, mode=0)
