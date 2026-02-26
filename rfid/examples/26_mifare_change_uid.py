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

uid, atqa, sak = iso.scan_and_select()
print("Before operation")
debug("UID", uid)
print(f"ATQA: {atqa:04X}")
print(f"SAK:  {sak:02X}")

mif.backdoor_enable()
mif.backdoor_change_uid(b"\x12\x34\x56\x78", b"\xAB\xCD", 0xFF, b"Extronic")

uid, atqa, sak = iso.scan_and_select()
print("After operation")
debug("UID", uid)
print(f"ATQA: {atqa:04X}")
print(f"SAK:  {sak:02X}")
