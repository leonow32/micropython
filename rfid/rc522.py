from machine import Pin, SPI
import time
import rfid.reg as reg

class RC522:
    
    def __init__(self, spi, cs, irq, rst):
        self.spi = spi
        self.cs = cs
        self.irq = irq
        self.rst = rst
        
        self.cs.init(mode=Pin.OUT, value=1)
        self.irq.init(mode=Pin.IN)
        self.rst.init(mode=Pin.OUT, value=0)
        time.sleep_ms(50)
        self.rst(1)

        self.regs_init()
            
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
        
    def reg_write(self, register: int, value: int) -> None:
        """

        """
        temp = bytes([register, value])
        self.cs(0)
        self.spi.write(temp)
        self.cs(1)
        
    def regs_write(self, register: int, buffer: bytes | bytearray) -> None:
        """

        """
        for i in range(len(buffer)):
            self.reg_write(register + 2*i, buffer[i])
            
    def reg_set_bit(self, register: int, mask: int) -> None:
        """

        """
        temp = self.reg_read(register)
        temp |= mask
        self.reg_write(register, temp)
        
    def reg_clr_bit(self, register: int, mask: int) -> None:
        """
        
        """
        temp = self.reg_read(register)
        temp = (temp & ~mask) & 0xFF
        self.reg_write(register, temp)
        
    def regs_init(self) -> None:
        self.reg_write(reg.TxModeReg, 0x00);
        self.reg_write(reg.RxModeReg, 0x00);
        self.reg_write(reg.ModWidthReg, 0x26);
        self.reg_write(reg.TModeReg, 0x80);
        self.reg_write(reg.TPrescalerReg, 0xA9);
        self.reg_write(reg.TReloadRegH, 0x03);
        self.reg_write(reg.TReloadRegL, 0xE8);    
        self.reg_write(reg.TxASKReg, 0x40);
        self.reg_write(reg.ModeReg, 0x3D);
        
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
        
    def version_get(self) -> None:
        return self.reg_read(reg.VersionReg)
    
    def antenna_enable(self) -> None:
        self.reg_set_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def antenna_disable(self) -> None:
        self.reg_clr_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)

if __name__ == "__main__":
    import mem_used
    spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    irq = Pin(6)
    rst = Pin(7)

    reader = RC522(spi, cs, irq, rst)

    ver = reader.version_get()
    print(f"VERSION: {ver:02X}")

#     reader.regs_write(reg.TModeReg, b"\x01\x01\x01\x01")
    reader.dump()
    
    reader.antenna_enable()

    mem_used.print_ram_used()
