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
