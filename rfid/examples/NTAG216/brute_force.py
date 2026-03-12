from machine import Pin, SPI
from rfid.rc522 import RC522
from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
from rfid.ntag21x import NTAG21X
from rfid.log import *
from struct import pack
import measure_time

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5)
rst = Pin(7)
pcd = RC522(spi, cs, rst)
iso = ISO_IEC_14443_3(pcd)
mif = NTAG21X(pcd)

uid, _, _ = iso.scan_and_select()

debug("Found card with UID", uid)
debug_disable()

pwd = bytearray(4)

measure_time.begin()
for i in range(0xFFFFFF00, 0xFFFFFFFF+1):
    print(f"Try {i:08X}: ", end="")
    
    try:
        pwd[0] = (i >> 24) & 0xFF
        pwd[1] = (i >> 16) & 0xFF
        pwd[2] = (i >> 8) & 0xFF
        pwd[3] = i & 0xFF
        mif.authenticate(pwd)
        
#         mif.authenticate(pack(">I", i))
        
        print("success")
        break
    except:
        print("fail")
        iso.wupa()
        iso.select(uid)
        
measure_time.end("Brute force done")