from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
from rfid.mifare_ultralight import MifareUltralight
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)
iso = ISO_IEC_14443_3(pcd)
mif = MifareUltralight(pcd)

iso.scan_and_select()

print("Read blocks from 0 to 3")
block0_3 = mif.block_read(0)
print("Read blocks from 4 to 7")
block4_7 = mif.block_read(4)

debug("Blocks from 0 to 3", block0_3)
debug("Blocks from 4 to 7", block4_7)
