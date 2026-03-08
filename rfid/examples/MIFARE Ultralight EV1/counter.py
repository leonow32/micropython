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

print("Read Counter 0")
data = mif.counter_read(0)

print(f"Counter0: {data}")

print("Increment counter 0")
mif.counter_increment(0, 1)

print("Read Counter 0")
data = mif.counter_read(0)

print(f"Counter0: {data}")
