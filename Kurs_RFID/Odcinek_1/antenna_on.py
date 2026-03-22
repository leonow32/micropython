from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)

ver = pcd.version_get()
debug("Version", ver)
