from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
from rfid.mifare_classic import MifareClassic
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)
iso = ISO_IEC_14443_3(pcd)
mif = MifareClassic(pcd, iso)

adr = 1
key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

uid, _, _ = iso.scan_and_select()
mif.authenticate(uid, adr, "A", key)
mif.block_write(adr, b"Some new data...")

print(f"Block {adr} saved")