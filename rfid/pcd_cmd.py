# Commands for RC522 Proximity Coupling Device
# They can be written into CommandReg register

Idle             = const(0b0000) # no action, cancels current command execution
Mem              = const(0b0001) # stores 25 bytes into the internal buffer
GenerateRandomID = const(0b0010) # generates a 10-byte random ID number
CalcCRC          = const(0b0011) # activates the CRC coprocessor or performs a self test
Transmit         = const(0b0100) # transmits data from the FIFO buffer
NoCmdChange      = const(0b0111) # no command change, can be used to modify the
                                 # CommandReg register bits without affecting the command,
                                 # for example, the PowerDown bit
Receive          = const(0b1000) # activates the receiver circuits
Transceive       = const(0b1100) # transmits data from FIFO buffer to antenna and automatically
                                 # activates the receiver after transmission
MFAuthent        = const(0b1110) # performs the MIFARE standard authentication as a reader
SoftReset        = const(0b1111) # resets the MFRC522
