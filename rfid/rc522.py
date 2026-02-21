import time
from machine import Pin, SPI
from rfid.log import *

# Commands for RC522 Proximity Coupling Device. Please write them to CommandReg register.
Idle             = const(0b0000) # no action, cancels current command execution
Mem              = const(0b0001) # stores 25 bytes into the internal buffer
GenerateRandomID = const(0b0010) # generates a 10-byte random ID number
CalcCRC          = const(0b0011) # activates the CRC coprocessor or performs a self test
Transmit         = const(0b0100) # transmits data from the FIFO buffer
NoCmdChange      = const(0b0111) # no command change, can be used to modify the CommandReg register bits without 
                                 # affecting the command, for example, the PowerDown bit
Receive          = const(0b1000) # activates the receiver circuits
Transceive       = const(0b1100) # transmits data from FIFO buffer to antenna and then activates the receiver
MFAuthent        = const(0b1110) # performs the MIFARE standard authentication as a reader
SoftReset        = const(0b1111) # resets the MFRC522

# Register addresses are shifter left by 1 bit position

# Page 0: Command and status
CommandReg      = const(0x02) # (0x01) starts and stops command execution
ComlEnReg       = const(0x04) # (0x02) enable and disable interrupt request control bits
DivlEnReg       = const(0x06) # (0x03) enable and disable interrupt request control bits
ComIrqReg       = const(0x08) # (0x04) interrupt request bits
DivIrqReg       = const(0x0A) # (0x05) interrupt request bits
ErrorReg        = const(0x0C) # (0x06) error bits showing the error status of the last command e
Status1Reg      = const(0x0E) # (0x07) communication status bits
Status2Reg      = const(0x10) # (0x08) receiver and transmitter status bits
FIFODataReg     = const(0x12) # (0x09) input and output of 64 byte FIFO buffer
FIFOLevelReg    = const(0x14) # (0x0A) number of bytes stored in the FIFO buffer
WaterLevelReg   = const(0x16) # (0x0B) level for FIFO underflow and overflow warning
ControlReg      = const(0x18) # (0x0C) miscellaneous control registers
BitFramingReg   = const(0x1A) # (0x0D) adjustments for bit-oriented frames
CollReg         = const(0x1C) # (0x0E) bit position of the first bit-collision detected on the R

# Page 1: Command
ModeReg         = const(0x22) # (0x11) defines general modes for transmitting and receiving
TxModeReg       = const(0x24) # (0x12) defines transmission data rate and framing
RxModeReg       = const(0x26) # (0x13) defines reception data rate and framing
TxControlReg    = const(0x28) # (0x14) controls the logical behavior of the antenna driver pins
TxASKReg        = const(0x2A) # (0x15) controls the setting of the transmission modulation
TxSelReg        = const(0x2C) # (0x16) selects the internal sources for the antenna driver
RxSelReg        = const(0x2E) # (0x17) selects internal receiver settings
RxThresholdReg  = const(0x30) # (0x18) selects thresholds for the bit decoder
DemodReg        = const(0x32) # (0x19) defines demodulator settings
MfTxReg         = const(0x38) # (0x1C) controls some MIFARE communication transmit parameters
MfRxReg         = const(0x3A) # (0x1D) controls some MIFARE communication receive parameters
SerialSpeedReg  = const(0x3E) # (0x1F) selects the speed of the serial UART interface

# Page 2: Configuration00
CRCResultRegH   = const(0x42) # (0x21) shows the MSB and LSB values of the CRC calculation
CRCResultRegL   = const(0x44) # (0x22) 
ModWidthReg     = const(0x48) # (0x24) controls the ModWidth setting?
RFCfgReg        = const(0x4C) # (0x26) configures the receiver gain
GsNReg          = const(0x4E) # (0x27) selects the conductance of the antenna driver pins TX1 an
CWGsPReg        = const(0x50) # (0x28) defines the conductance of the p-driver output during per
ModGsPReg       = const(0x52) # (0x29) defines the conductance of the p-driver output during per
TModeReg        = const(0x54) # (0x2A) defines settings for the internal timer
TPrescalerReg   = const(0x56) # (0x2B) the lower 8 bits of the TPrescaler value. The 4 high bits
TReloadRegH     = const(0x58) # (0x2C) defines the 16-bit timer reload value
TReloadRegL     = const(0x5A) # (0x2D) 
TCounterValRegH = const(0x5C) # (0x2E) shows the 16-bit timer value
TCounterValRegL = const(0x5E) # (0x2F) 

# Page 3: Test Registers00
TestSel1Reg     = const(0x62) # (0x31) general test signal configuration
TestSel2Reg     = const(0x64) # (0x32) general test signal configuration
TestPinEnReg    = const(0x66) # (0x33) enables pin output driver on pins D1 to D7
TestPinValueReg = const(0x68) # (0x34) defines the values for D1 to D7 when it is used as an I/O
TestBusReg      = const(0x6A) # (0x35) shows the status of the internal test bus
AutoTestReg     = const(0x6C) # (0x36) controls the digital self-test
VersionReg      = const(0x6E) # (0x37) shows the software version, value 0x91 for version 1, 0x92 for version 2
AnalogTestReg   = const(0x70) # (0x38) controls the pins AUX1 and AUX2
TestDAC1Reg     = const(0x72) # (0x39) defines the test value for TestDAC1
TestDAC2Reg     = const(0x74) # (0x3A) defines the test value for TestDAC2
TestADCReg      = const(0x76) # (0x3B) shows the value of ADC I and Q channels

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

        self.write_reg(TxASKReg, 0b01000000) # Force a 100 % ASK modulation
        self.write_reg(ModeReg,  0b00100001) # Set the initial value for the CRC coprocessor to 0x6363
        self.write_reg(RFCfgReg, 0b01111000) # Set antenna gain to maximum
        self.antenna_enable()
            
    def read_reg(self, register: int) -> int:
        """
        Read single register. Register name should come from py file.
        """
        temp = bytearray([0x80 | register, 0x00])
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1]
    
    def read_regs(self, register: int, length: int) -> bytearray:
        """
        Read more bytes from a single register. Register name should come from py file.
        This function is useful to read data from FIFO buffer.
        """
        temp = bytearray([0x80 | register] * (length + 1))
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1:]
        
    def write_reg(self, register: int, value: int|bytes|bytearray) -> None:
        """
        Write a value or buffer of values into a register. Register name should come from py file.
        """
        self.cs(0)
        
        if isinstance(value, int):
            self.spi.write(bytes([register, value]))
        else:
            self.spi.write(bytes([register]))
            self.spi.write(value)
            
        self.cs(1)
            
    def set_bits(self, register: int, mask: int) -> None:
        """
        Read a register, set bit of bit mask to this register and then write it to RC522.
        """
        temp = self.read_reg(register)
        temp |= mask
        self.write_reg(register, temp)
        
    def clear_bits(self, register: int, mask: int) -> None:
        """
        Read a register, clear bit of bit mask to this register and then write it to RC522.
        """
        temp = self.read_reg(register)
        temp = (temp & ~mask) & 0xFF
        self.write_reg(register, temp)
        
    def version_get(self) -> None:
        """
        Get version of RC522.
        """
        return self.read_reg(VersionReg)
    
    def antenna_enable(self) -> None:
        """
        Turn on the antenna and wait 5ms, which is enough time for any card to start up.
        """
        self.set_bits(TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def antenna_disable(self) -> None:
        """
        Turn off the antenna and wait 5ms for the card to discharge its power capacitor.
        """
        self.clear_bits(TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def crypto1_stop(self) -> None:
        """
        This command resets Crypto1 engine. Use it to terminate communication with authenticated MIFARE Classic card.
        """
        self.clear_bits(Status2Reg, 0b00001000)
        
    def wait_for_irq(self) -> None:
        """
        Check ComIrqReg register periodically every 10ms. Finish when RxIRq or IdleIRq bits are 1.
        This function rises an exception in case of timeout.
        """
        for i in range(self.timeout_ms // 10):
            if self.read_reg(ComIrqReg) & 0b00110000: # check RxIRq and IdleIRq
                return
            else:
                time.sleep_ms(10)
        
        raise Exception("Timeout")
    
    def crc_calculate(self, data: bytes|bytearray) -> int:
        """
        The function calculates the CRC from the given data buffer.
        """
        self.write_reg(FIFOLevelReg, 0x80);          # Clear all the data in FIFO buffer
        self.write_reg(CommandReg, CalcCRC)          # Enable CRC coprocessor
        self.write_reg(FIFODataReg, data)            # Transmit the data to FIFO buffer
        # The CRC result is ready almost instantly, so there is no need to wait or check anything
        crc_h  = self.read_reg(CRCResultRegH)
        crc_l  = self.read_reg(CRCResultRegL)
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
        Transmit a bytearray buffer to the card, wait for the response, read it and return as a bytearray.
        This function rises an exception in case there's no response from the card.
        """
        debug("Send", send_buf)
        self.write_reg(CommandReg, Idle)                # Stop any ongoing command and set RC522 to idle state
        self.write_reg(ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.write_reg(FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.write_reg(FIFODataReg, send_buf)           # Copy the buffer to FIFO buffer in RC522
        self.write_reg(BitFramingReg, 0)                # Set transfer length to 8 bits
        self.write_reg(CommandReg, Transceive)          # Enter new command
        self.set_bits(BitFramingReg, 0x80)              # Start data transfer, bit StartSend=1
        self.wait_for_irq()                             # Wait for receive interrupt flag
        length   = self.read_reg(FIFOLevelReg)          # Check how many bytes are received            
        recv_buf = self.read_regs(FIFODataReg, length)  # Read the response
        debug("Recv", recv_buf)
        return recv_buf
        
    def transmit_7bit(self, command_7bit: int) -> bytearray:
        """
        Transmit a 7-bit command to the card, wait for the response, read it and return as a bytearray.
        This function rises an exception in case there's no response from the card.
        """
        debug("Send[s]", command_7bit)
        self.write_reg(CommandReg, Idle)                # Stop any ongoing command and set RC522 to idle state
        self.write_reg(ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.write_reg(FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.write_reg(FIFODataReg, command_7bit)       # Store data to FIFO buffer
        self.write_reg(BitFramingReg, 7)                # Set transfer length to 7 bits instead of 8
        self.write_reg(CommandReg, Transceive)          # Enter new command
        self.set_bits(BitFramingReg, 0x80)              # Start data transfer, bit StartSend=1
        self.wait_for_irq()                             # Wait for receive interrupt flag
        length   = self.read_reg(FIFOLevelReg)          # Check how many bytes are received
        recv_buf = self.read_regs(FIFODataReg, length)  # Read the response
        debug("Recv", recv_buf)
        return recv_buf
        