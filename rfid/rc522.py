from machine import Pin, SPI
import time
from rfid.log import *
import rfid.reg as reg
import rfid.pcd_cmd as pcd_cmd
import rfid.picc_cmd as picc_cmd

class RC522:
    
    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs  = cs
        self.rst = rst

        self.timeout_ms = 100
        
        self.cs.init(mode=Pin.OUT, value=1)
        self.rst.init(mode=Pin.OUT, value=0)
        time.sleep_ms(50)
        self.rst(1)

        self.reg_write(reg.TxASKReg,      0b01000000) # Force a 100 % ASK modulation
        self.reg_write(reg.ModeReg,       0b00100001) # Set the initial value for the CRC coprocessor to 0x6363
            
    def reg_read(self, register: int) -> int:
        """
        Read single register. Register name should come from reg.py file.
        """
        temp = bytearray([0x80 | register, 0x00])
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1]
    
    def reg_reads(self, register: int, length: int) -> bytearray:
        """
        Read more bytes from a single register. Register name should come from reg.py file.
        This function is useful to read data from FIFO buffer.
        """
        temp = bytearray([0x80 | register] * (length + 1))
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1:]
        
    def reg_write(self, register: int, value: int|bytes|bytearray) -> None:
        """
        Write a value or buffer of values into a register. Register name should come from reg.py file.
        """
        self.cs(0)
        
        if isinstance(value, int):
            self.spi.write(bytes([register, value]))
        else:
            self.spi.write(bytes([register]))
            self.spi.write(value)
            
        self.cs(1)
            
    def reg_set_bit(self, register: int, mask: int) -> None:
        """
        Read a register, set bit of bit mask to this register and then write it to RC522.
        """
        temp = self.reg_read(register)
        temp |= mask
        self.reg_write(register, temp)
        
    def reg_clr_bit(self, register: int, mask: int) -> None:
        """
        Read a register, clear bit of bit mask to this register and then write it to RC522.
        """
        temp = self.reg_read(register)
        temp = (temp & ~mask) & 0xFF
        self.reg_write(register, temp)
        
    def version_get(self) -> None:
        """
        Get version of RC522.
        """
        return self.reg_read(reg.VersionReg)
    
    def antenna_enable(self) -> None:
        """
        Turn on the antenna and wait 5ms, which is enough time for any card to start up.
        """
        self.reg_set_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def antenna_disable(self) -> None:
        """
        Turn off the antenna and wait 5ms for the card to discharge its power capacitor.
        """
        self.reg_clr_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def gain_set(self, value: int) -> None:
        """
        Set the gain value in the range of 0...7
        """
        if value < 0: value = 0
        if value > 7: value = 7
        temp = self.reg_read(reg.RFCfgReg)
        temp = temp & 0b10001111
        temp = temp | (value << 4)
        self.reg_write(reg.RFCfgReg, temp)
    
    def gain_get(self) -> int:
        """
        Set the gain value in the range of 0...7
        """
        value = self.reg_read(reg.RFCfgReg)
        value = (value >> 4) & 0b111
        return value
        
    def crypto1_stop(self) -> None:
        """
        This command resets Crypto1 engine. Use it to terminate communication with authenticated MIFARE Classic card.
        """
        self.reg_clr_bit(reg.Status2Reg, 0b00001000)
        
    def wait_for_irq(self) -> None:
        for i in range(self.timeout_ms // 10):
            if self.reg_read(reg.ComIrqReg) & 0b00110000: # check RxIRq and IdleIRq
                return
            else:
                time.sleep_ms(10)
        
        raise Exception("Timeout")
    
    def crc_calculate(self, data: bytes|bytearray) -> int:
        """
        The function calculates the CRC from the given data buffer.
        """
        self.reg_write(reg.FIFOLevelReg, 0x80);          # Clear all the data in FIFO buffer
        self.reg_write(reg.CommandReg, pcd_cmd.CalcCRC)  # Enable CRC coprocessor
        self.reg_write(reg.FIFODataReg, data)            # Transmit the data to FIFO buffer
        # The CRC result is ready almost instantly, so there is no need to wait or check anything
        crc_h  = self.reg_read(reg.CRCResultRegH)
        crc_l  = self.reg_read(reg.CRCResultRegL)
        result = crc_h << 8 | crc_l
        return result    
    
    def crc_calculate_and_append(self, buffer: bytearray) -> None:
        """
        Calculates the CRC from given buffer and appends the result to the end of the buffer, so it can be transmitted to
        the PICC in the following line.
        """
        crc = self.crc_calculate(buffer)
        buffer.append(crc & 0xFF) # CRC_L
        buffer.append(crc >> 8)   # CRC_H
        
    def crc_verify(self, buffer: bytes|bytearray) -> None:
        """
        The function checks the buffer returned by PICC, which contains some data and the CRC at the end of the buffer.
        The function calculates the CRC from the received data and checks whether it matches the received CRC.
        This function rises an exception in case of wrong CRC.
        """
        crc_calculated = self.crc_calculate(buffer[0:-2])
        crc_received   = buffer[-1] << 8 | buffer[-2]
        if crc_calculated != crc_received:
            raise Exception(f"Wrong CRC, received {crc_received:04X}, expected {crc_calculated:04X}")
        
    def transmit(self, send_buf: bytearray) -> bytearray:
        """

        """
        debug("Send", send_buf)
        self.reg_write(reg.CommandReg, pcd_cmd.Idle)        # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, send_buf)           # Copy the buffer to FIFO buffer in RC522
        self.reg_write(reg.BitFramingReg, 0)                # Set transfer length to 8 bits
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive)  # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        self.wait_for_irq()                                 # Wait for receive interrupt flag
        length   = self.reg_read(reg.FIFOLevelReg)          # Check how many bytes are received            
        recv_buf = self.reg_reads(reg.FIFODataReg, length)  # Read the response
        debug("Recv", recv_buf)
        return recv_buf
        
    def transmit_7bit(self, command_7bit: int) -> bytearray:
        """

        """
        debug("Send[s]", command_7bit)
        self.reg_write(reg.CommandReg, pcd_cmd.Idle)        # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, command_7bit)       # Store data to FIFO buffer
        self.reg_write(reg.BitFramingReg, 7)                # Set transfer length to 7 bits instead of 8
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive)  # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        self.wait_for_irq()                                 # Wait for receive interrupt flag
        length   = self.reg_read(reg.FIFOLevelReg)          # Check how many bytes are received
        recv_buf = self.reg_reads(reg.FIFODataReg, length)  # Read the response
        debug("Recv", recv_buf)
        return recv_buf
        
if __name__ == "__main__":
    import mem_used
    import measure_time
    spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    rst = Pin(7)

    reader = RC522(spi, cs, rst)

    ver = reader.version_get()
    debug("Version", ver)
    
    reader.antenna_enable()
    reader.gain_set(7)
    
#     try:
#         uid, atqa, sak = reader.picc_scan_and_select()
#         print("Card found")
#         reader.debug_print("UID", uid)
#         print(f"ATQA: {atqa:04X}")
#         print(f"SAK:  {sak:02X}")
#     except:
#         print("No card")
        
    # Memory dump test
#     reader.debug = False
#     reader.mifare_1k_dump(uid)
#     reader.mifare_4k_dump(uid)

    # Backdoor key test
#     reader.debug = False
#     reader.mifare_try_backdoor_keys()
    
    # Value read
#     reader.mifare_auth(uid, 5, picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF")
#     for i in range(4, 7, 1):
#         value = reader.mifare_value_get(i)
#         print(f"block {i} value = {value}")

#     reader.mifare_backdoor()
#     reader.debug = False
#     reader.mifare_1k_dump(uid, keys=None, use_authentication=False)

#     key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

    mem_used.print_ram_used()
