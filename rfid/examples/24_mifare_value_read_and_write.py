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

uid, _, _ = iso.scan_and_select()

mif.authenticate(uid, 5, "A", b"\xFF\xFF\xFF\xFF\xFF\xFF")
mif.value_set(4, 12345678)
mif.value_set(5, -123)
mif.value_set(6, 0)

val4 = mif.value_get(4)
val5 = mif.value_get(5)
val6 = mif.value_get(6)

print(f"value of block 4 is {val4}")
print(f"value of block 5 is {val5}")
print(f"value of block 6 is {val6}")
