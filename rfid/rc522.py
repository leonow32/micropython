from machine import Pin, SPI
import time
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
        
    def reg_read(self, register: int) -> None:
        """
        Read single register. Argument should be given as a register name from reg.py file.
        """
        temp = bytearray([0x80 | register, 0x00])
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1]
    
    def regs_read(self, register: int, buffer: bytearray) -> None:
        """
        Read one or more registers. Argument should be given as a register name from reg.py file.
        Result is stored in given buffer that must be a bytearray.
        """
        temp = bytearray(len(buffer) + 1)
        for i in range(len(temp)):
            temp[i] = (2*(register + i)) | 0x80
        temp[-1] = 0x00
        
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        
        buffer[:] = temp[1:]
        
    def dump(self) -> None:
        """
        Read all the registers of RC522 and print them to the console.
        """
        registers = bytearray(64)
        self.regs_read(0x00, registers)
        
        print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F", end="")
        
        for i in range(len(registers)):
            if i%16 == 0:
                print(f"\n{i:02X}: ", end="")
            print(f"{registers[i]:02X} ", end="")
        
        print()

if __name__ == "__main__":
    import mem_used
    spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs = Pin(5)
    irq = Pin(6)
    reset = Pin(7)

    reader = RC522(spi, cs, irq, reset)

    ver = reader.reg_read(reg.VERSION)
    print(f"VERSION: {ver:02X}")

    reader.dump()
    

    mem_used.print_ram_used()
