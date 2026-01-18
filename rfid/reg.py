# Page 0: Command and status
COMMAND         = const(0x01 << 1) # starts and stops command execution
COM_IEN         = const(0x02 << 1) # enable and disable interrupt request control bits
DIV_IEN         = const(0x03 << 1) # enable and disable interrupt request control bits
COM_IRQ         = const(0x04 << 1) # interrupt request bits
DIV_IRQ         = const(0x05 << 1) # interrupt request bits
ERROR           = const(0x06 << 1) # error bits showing the error status of the last command executed
STATUS1         = const(0x07 << 1) # communication status bits
STATUS2         = const(0x08 << 1) # receiver and transmitter status bits
FIFO_DATA       = const(0x09 << 1) # input and output of 64 byte FIFO buffer
FIFO_LEVEL      = const(0x0A << 1) # number of bytes stored in the FIFO buffer
WATER_LEVEL     = const(0x0B << 1) # level for FIFO underflow and overflow warning
CONTROL         = const(0x0C << 1) # miscellaneous control registers
BIT_FRAMING     = const(0x0D << 1) # adjustments for bit-oriented frames
COLL            = const(0x0E << 1) # bit position of the first bit-collision detected on the RF interface

# Page 1: Command
MODE            = const(0x11 << 1) # defines general modes for transmitting and receiving
TX_MODE         = const(0x12 << 1) # defines transmission data rate and framing
RX_MODE         = const(0x13 << 1) # defines reception data rate and framing
TX_CONTROL      = const(0x14 << 1) # controls the logical behavior of the antenna driver pins TX1 and TX2
TX_ASK          = const(0x15 << 1) # controls the setting of the transmission modulation
TX_SEL          = const(0x16 << 1) # selects the internal sources for the antenna driver
RX_SEL          = const(0x17 << 1) # selects internal receiver settings
RX_THRES        = const(0x18 << 1) # selects thresholds for the bit decoder
DEMOD           = const(0x19 << 1) # defines demodulator settings
TX_MIFARE       = const(0x1C << 1) # controls some MIFARE communication transmit parameters
RX_MIFARE       = const(0x1D << 1) # controls some MIFARE communication receive parameters
SERIAL_SPEED    = const(0x1F << 1) # selects the speed of the serial UART interface

# Page 2: Configuration
CRC_RESULT_H    = const(0x21 << 1) # shows the MSB and LSB values of the CRC calculation
CRC_RESULT_L    = const(0x22 << 1)
MOD_WIDTH       = const(0x24 << 1) # controls the ModWidth setting?
RF_CFG          = const(0x26 << 1) # configures the receiver gain
GSN             = const(0x27 << 1) # selects the conductance of the antenna driver pins TX1 and TX2 for modulation
CWGSP           = const(0x28 << 1) # defines the conductance of the p-driver output during periods of no modulation
MODGSP          = const(0x29 << 1) # defines the conductance of the p-driver output during periods of modulation
TIMER_MODE      = const(0x2A << 1) # defines settings for the internal timer
TIMER_PRESCALER = const(0x2B << 1) # the lower 8 bits of the TPrescaler value. The 4 high bits are in TModeReg.
TIMER_RELOAD_H  = const(0x2C << 1) # defines the 16-bit timer reload value
TIMER_RELOAD_L  = const(0x2D << 1)
TIMER_VALUE_H   = const(0x2E << 1) # shows the 16-bit timer value
TIMER_VALUE_L   = const(0x2F << 1)

# Page 3: Test Registers
TEST_SEL1       = const(0x31 << 1) # general test signal configuration
TEST_SEL2       = const(0x32 << 1) # general test signal configuration
TEST_PIN_EN     = const(0x33 << 1) # enables pin output driver on pins D1 to D7
TEST_PIN_VALUE  = const(0x34 << 1) # defines the values for D1 to D7 when it is used as an I/O bus
TEST_BUS        = const(0x35 << 1) # shows the status of the internal test bus
TEST_AUTO       = const(0x36 << 1) # controls the digital self-test
VERSION         = const(0x37 << 1) # shows the software version
TEST_ANALOG     = const(0x38 << 1) # controls the pins AUX1 and AUX2
TEST_DAC1       = const(0x39 << 1) # defines the test value for TestDAC1
TEST_DAC2       = const(0x3A << 1) # defines the test value for TestDAC2
TEST_ADC        = const(0x3B << 1) # shows the value of ADC I and Q channels
