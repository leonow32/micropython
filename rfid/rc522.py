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
    
    def regs_read(self, register, buffer):
        write_buf = bytearray(len(buffer)+1)
        for i in range(len(write_buf)):
            write_buf[i] = (2*(register + i)) | 0x80
#             write_buf[i] = (register + i)
        write_buf[-1] = 0x00
        
        print(write_buf)
        
        read_buf = bytearray(len(buffer)+1)
        self.cs(0)
        self.spi.write_readinto(write_buf, read_buf)
        self.cs(1)
        
        print(read_buf)
        
        return read_buf[1:]
        
#         buffer = read_buf[:]

    def dump2(self):
        print("   ", end="")
        for i in range(16):
            print(f"  {i:X}", end="")
            
        for i in range(64):
            val = self.reg_read(i*2)
            
            if i%16 == 0:
                print(f"\n{i:02X}: ", end="")
                
            print(f"{val:02X} ", end="")
        
        print()
            
        
    def dump(self):
        registers = bytearray(64)
        registers = self.regs_read(0x00, registers)
        print(registers)
        
        print("   ", end="")
        for i in range(16):
            print(f"  {i:X}", end="")
        
        for i in range(len(registers)):
            if i%16 == 0:
                print(f"\n{i:02X}: ", end="")
            print(f"{registers[i]:02X} ", end="")
        
        print()
                

        

#print(reg.COMMAND)

# spi = SPI(0)
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5)
irq = Pin(6)
reset = Pin(7)

reader = RC522(spi, cs, irq, reset)

ver = reader.reg_read(reg.VERSION)
print(f"VERSION: {ver:02X}")

reader.dump()
reader.dump2()

mem_used.print_ram_used()