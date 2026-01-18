from micropython import const
from machine import Pin, SPI
import time
import mem_used
import rfid.reg as reg

class RC522:
    
    def __init__(self, spi, cs, irq, reset):
        self.spi = spi
        self.cs = cs
        self.irq = irq
        self.reset = reset
        
        self.cs.init(mode=Pin.OUT, value=1)
        self.irq.init(mode=Pin.IN)
        self.reset.init(mode=Pin.OUT, value=0)
        time.sleep_ms(50)
        self.reset(1)
        
    def reg_read(self, register):
        write_buf = bytes([0x80 | register, 0x00])
        read_buf = bytearray(2)
        self.cs(0)
        self.spi.write_readinto(write_buf, read_buf)
        self.cs(1)
        return read_buf[1]

        

#print(reg.COMMAND)

spi = SPI(0)
#spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5)
irq = Pin(6)
reset = Pin(7)

reader = RC522(spi, cs, irq, reset)

ver = reader.reg_read(reg.VERSION)
print(f"VERSION: {ver:02X}")

mem_used.print_ram_used()