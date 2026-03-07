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

print("Write to block 10")
mif.block_write(10, b"\x11\x22\x33\x44")
print("Write to block 11")
mif.block_write(11, bytes([0x11, 0x22, 0x33, 0x44]))
print("Write to block 12")
mif.block_write(12, b"Extr")
print("Write to block 13")
mif.block_write(13, b"onic")
