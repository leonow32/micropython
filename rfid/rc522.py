from machine import Pin, SPI
import time
import rfid.reg as reg
import rfid.pcd_cmd as pcd_cmd
import rfid.picc_cmd as picc_cmd

class RC522:
    
    def __init__(self, spi, cs, irq, rst):
        self.spi = spi
        self.cs  = cs
        self.irq = irq
        self.rst = rst
        self.crc = 0x6363
        
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
        
#     def regs_write(self, register: int, buffer: bytes | bytearray) -> None:
#         """
# 
#         """
#         for i in range(len(buffer)):
#             self.reg_write(register + 2*i, buffer[i])
            
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
        self.reg_write(reg.TxModeReg,     0x00) # Reset baud rates
        self.reg_write(reg.RxModeReg,     0x00) # Reset baud rates
        self.reg_write(reg.ModWidthReg,   0x26) # Reset ModWidthReg
        
        # When communicating with a PICC we need a timeout if something goes wrong.
        # f_timer = 13.56 MHz / (2*TPreScaler+1) where TPreScaler = [TPrescaler_Hi:TPrescaler_Lo].
        # TPrescaler_Hi are the four low bits in TModeReg. TPrescaler_Lo is TPrescalerReg.
        self.reg_write(reg.TModeReg,      0x80) # TAuto=1; timer starts automatically at the end of the transmission in all communication modes at all speeds
        self.reg_write(reg.TPrescalerReg, 0xA9) # TPreScaler = TModeReg[3..0]:TPrescalerReg, ie 0x0A9 = 169 => f_timer=40kHz, ie a timer period of 25μs.
        self.reg_write(reg.TReloadRegH,   0x03) # Reload timer with 0x3E8 = 1000, ie 25ms before timeout.
        self.reg_write(reg.TReloadRegL,   0xE8)    
        self.reg_write(reg.TxASKReg,      0x40) # Default 0x00. Force a 100 % ASK modulation independent of the ModGsPReg register setting
        self.reg_write(reg.ModeReg,       0x3D) # Default 0x3F. Set the preset value for the CRC coprocessor for the CalcCRC command to 0x6363 (ISO 14443-3 part 6.2.4)
        
    def reset(self) -> None:
        self.reg_write(reg.CommandReg, pcd_cmd.SoftReset)

        timeout_counter = 0
        while self.reg_read(reg.CommandReg) & 0b00010000:
            timeout_counter += 1
            if(timeout_counter == 10):
                raise Exception(0, "No response after reset")
            time.sleep_ms(10)
            
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
        
    def crypto1_stop(self) -> None:
        """
        This command resets Crypto1 engine. Use it to terminate communication with authenticated PICC.
        """
        self.reg_clr_bit(reg.Status2Reg, 0b00001000)
        
    def wait_for_rx_irq(self, timeout_ms=100) -> None:
        for i in range(timeout_ms // 10):
            if self.reg_read(reg.ComIrqReg) & 0b00100000:
                return
            else:
                time.sleep_ms(10)
        
        raise Exception(0, "Timeout")
        
    def transmit(self, buffer, timeout_ms=100):
        self.reg_write(reg.CommandReg, pcd_cmd.Idle);       # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F);                # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80);             # Clear FIFO buffer
        for byte in buffer:
            self.reg_write(reg.FIFODataReg, byte);          # Copy the buffer to FIFO buffer in RC522
        self.reg_write(reg.BitFramingReg, 0)                # Set transfer length to 8 bits
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive); # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        
        self.wait_for_rx_irq(timeout_ms)                    # Wait for receive interrupt flag
        
        lenght = self.reg_read(reg.FIFOLevelReg)            # Check how many bytes are received
        print(f"received length: {lenght}")
        
        response_buf = bytearray(lenght)
        
        for i in range(lenght):
            recv_byte = self.reg_read(reg.FIFODataReg)
            response_buf[i] = recv_byte
            print(f"{recv_byte:02X}", end="")
        print()
        
        return response_buf

        
        
    def transmit_7bit(self, byte, timeout_ms=100):
        self.reg_write(reg.CommandReg, pcd_cmd.Idle);       # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F);                # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80);             # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, byte);              # Store data to FIFO buffer
        self.reg_write(reg.BitFramingReg, 7)                # Set transfer length to 7 bits instead of 8
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive); # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        
        self.wait_for_rx_irq(timeout_ms)                    # Wait for receive interrupt flag
        
        lenght = self.reg_read(reg.FIFOLevelReg)            # Check how many bytes are received
#         print(f"received length: {lenght}")
        
        response_buf = bytearray(lenght)
        
        for i in range(lenght):
            recv_byte = self.reg_read(reg.FIFODataReg)
            response_buf[i] = recv_byte
#             print(f"{recv_byte:02X}", end="")
#         print()
        
        return response_buf
    
    def picc_wupa_send(self):
        """
        Senf WUPA (Wake Up Type A) to PICC that is in idle or power-on state.
        PICC responds with ATQA data. This function may raise timeout exception.
        """
        return self.transmit_7bit(picc_cmd.WUPA_7bit)
    
    def picc_reqa_send(self):
        return self.transmit_7bit(picc_cmd.REQA_7bit)
    
    def scan_all_7bit_commands(self):
        for i in range(128):
            try:
                self.antenna_disable()
                self.antenna_enable()
                response = self.transmit_7bit(i)
                print(f"cmd {i:02X}: response[{len(response)}] ", end="")
                for byte in response:
                    print(f"{byte:02X} ", end="")
                print("")
            except:
                pass
    
    def response_read(self, recv_buf):
        
        # Czekanie na odpowiedź
        for i in range(10):
            
            # Sprawdzanie czy jest RxIrq
            if self.reg_read(reg.ComIrqReg) & 0b00100000:
                
                lenght = self.reg_read(reg.FIFOLevelReg)
                print(f"FIFOLevelReg: {lenght}")
                
                print("FIFODataReg: ", end="")
                for j in range(lenght):
                    
                    recv_buf[j] = self.reg_read(reg.FIFODataReg)
                    print(f"{recv_buf[j]:02X}", end="")
                print()
                
                print("Wyjście z transmit")
                return
            else:
                print("_", end="")
                time.sleep_ms(10)
        
        print("Receive timeout")
        raise TimeoutError
        

if __name__ == "__main__":
    import mem_used
    spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    irq = Pin(6)
    rst = Pin(7)

    reader = RC522(spi, cs, irq, rst)

    ver = reader.version_get()
    print(f"VERSION: {ver:02X}")

    reader.dump()
    
    reader.antenna_enable()

    mem_used.print_ram_used()
