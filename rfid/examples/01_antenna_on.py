from machine import Pin, SPI
import mem_used
from rfid.rc522 import RC522
from rfid.log import *

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)

reader = RC522(spi, cs, rst)

ver = reader.version_get()
debug("Version", ver)

mem_used.print_ram_used()
