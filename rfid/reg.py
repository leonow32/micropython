# Register addresses are shifter left by 1 bit position

# Page 0: Command and status
COMMAND         = const(0x02) # starts and stops command execution
COM_IEN         = const(0x04) # enable and disable interrupt request control bits
DIV_IEN         = const(0x06) # enable and disable interrupt request control bits
COM_IRQ         = const(0x08) # interrupt request bits
DIV_IRQ         = const(0x0A) # interrupt request bits
ERROR           = const(0x0C) # error bits showing the error status of the last command e
STATUS1         = const(0x0E) # communication status bits
STATUS2         = const(0x10) # receiver and transmitter status bits
FIFO_DATA       = const(0x12) # input and output of 64 byte FIFO buffer
FIFO_LEVEL      = const(0x14) # number of bytes stored in the FIFO buffer
WATER_LEVEL     = const(0x16) # level for FIFO underflow and overflow warning
CONTROL         = const(0x18) # miscellaneous control registers
BIT_FRAMING     = const(0x1A) # adjustments for bit-oriented frames
COLL            = const(0x1C) # bit position of the first bit-collision detected on the R

# Page 1: Command
MODE            = const(0x22) # defines general modes for transmitting and receiving
TX_MODE         = const(0x24) # defines transmission data rate and framing
RX_MODE         = const(0x26) # defines reception data rate and framing
TX_CONTROL      = const(0x28) # controls the logical behavior of the antenna driver pins
TX_ASK          = const(0x2A) # controls the setting of the transmission modulation
TX_SEL          = const(0x2C) # selects the internal sources for the antenna driver
RX_SEL          = const(0x2E) # selects internal receiver settings
RX_THRES        = const(0x30) # selects thresholds for the bit decoder
DEMOD           = const(0x32) # defines demodulator settings
TX_MIFARE       = const(0x38) # controls some MIFARE communication transmit parameters
RX_MIFARE       = const(0x3A) # controls some MIFARE communication receive parameters
SERIAL_SPEED    = const(0x3E) # selects the speed of the serial UART interface

# Page 2: Configuration00
CRC_RESULT_H    = const(0x42) # shows the MSB and LSB values of the CRC calculation
CRC_RESULT_L    = const(0x44)
MOD_WIDTH       = const(0x48) # controls the ModWidth setting?
RF_CFG          = const(0x4C) # configures the receiver gain
GSN             = const(0x4E) # selects the conductance of the antenna driver pins TX1 an
CWGSP           = const(0x50) # defines the conductance of the p-driver output during per
MODGSP          = const(0x52) # defines the conductance of the p-driver output during per
TIMER_MODE      = const(0x54) # defines settings for the internal timer
TIMER_PRESCALER = const(0x56) # the lower 8 bits of the TPrescaler value. The 4 high bits
TIMER_RELOAD_H  = const(0x58) # defines the 16-bit timer reload value
TIMER_RELOAD_L  = const(0x5A)
TIMER_VALUE_H   = const(0x5C) # shows the 16-bit timer value
TIMER_VALUE_L   = const(0x5E)

# Page 3: Test Registers00
TEST_SEL1       = const(0x62) # general test signal configuration
TEST_SEL2       = const(0x64) # general test signal configuration
TEST_PIN_EN     = const(0x66) # enables pin output driver on pins D1 to D7
TEST_PIN_VALUE  = const(0x68) # defines the values for D1 to D7 when it is used as an I/O
TEST_BUS        = const(0x6A) # shows the status of the internal test bus
TEST_AUTO       = const(0x6C) # controls the digital self-test
VERSION         = const(0x6E) # shows the software version
TEST_ANALOG     = const(0x70) # controls the pins AUX1 and AUX2
TEST_DAC1       = const(0x72) # defines the test value for TestDAC1
TEST_DAC2       = const(0x74) # defines the test value for TestDAC2
TEST_ADC        = const(0x76) # shows the value of ADC I and Q channels

