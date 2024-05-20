from machine import SPI
from machine import Pin
from ubinascii import hexlify
Spi = 0
Cs = 0

__READ = 0x03               # Read data from memory array beginning at selected address
__WRITE = 0x02              # Write data to memory array beginning at selected address
__WRITE_ENABLE = 0x06       # Set the write enable latch (enable write operations)
__WRITE_DISABLE = 0x04      # Reset the write enable latch (disable write operations)
__STATUS_READ = 0x05        # Read STATUS register
__STATUS_WRITE = 0x01       # Write STATUS register
__ERASE_PAGE = 0x42         # Page Erase – erase one page in memory array
__ERASE_SECTOR = 0xD8       # Sector Erase – erase one sector in memory array
__ERASE_CHIP = 0xC7         # Chip Erase – erase all sectors in memory array
__WAKE = 0xAB               # Release from Deep power-down and read electronic signature
__SLEEP = 0xB9              # Deep Power-Down mode

def printHex(Data, MaxInRow=16):
    Index = 0
    for Byte in Data:
        String = hexlify(Data[Index:Index+1], ' ').decode("utf-8")
        String = String.upper()
        print(String, end=" ")
        Index += 1
        if Index % MaxInRow == 0:
            print("")
    print("")

"""
def dump(Data, MaxInRow=16):
    Address = 0
    BytesLeft = len(Data)

    print("Length: {}".format(BytesLeft))
    print("Addr:\t 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    
    def PrintHex(Address, Bytes):
        if Bytes > MaxInRow:
            Bytes = MaxInRow
        String = hexlify(Data[Address:Address+Bytes], ' ').decode("ascii")
        String = String.upper()
        print(String, end="")
        
        # Wypełniacz
        print("   " * (MaxInRow-Bytes+1), end="")
        
    def PrintAscii(Address, Bytes):
        if Bytes > MaxInRow:
            Bytes = MaxInRow
        for i in range(Bytes):
            Char = Data[Address]
            if Char >= 32: 
                print(chr(Char), end="")
            else:
                print(" ", end="")
            Address += 1
    
    while BytesLeft:
        print("%04X" % Address + ":", end="\t")
        PrintHex(Address, BytesLeft)
        PrintAscii(Address, BytesLeft)      
        print("")
        
        Address += MaxInRow
        BytesLeft -= MaxInRow
        if BytesLeft <= 0:
            return
"""

def SpiInit():
    global Spi
    global Cs
    Spi = SPI(2, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    
    Cs = Pin(5, Pin.OUT)
    Cs.value(1)
    
def MemStatusRead():
    Buf = bytearray([__STATUS_READ, 0])
    printHex(Buf)
    Cs(0)
    Spi.write_readinto(Buf, Buf)
    Cs(1)
    printHex(Buf)
    return Buf[1]

def MemWaitForReady():
    Buf = bytearray([__STATUS_READ, 0])
    while True:
        Cs(0)
        Spi.write_readinto(Buf, Buf)
        Cs(1)
        if Buf[1] & 0x01 == 0:
            return
        print(".", end="")


# Przetestować to
def MemStatusWrite(Data):
    Buf = bytearray([__STATUS_WRITE, Data])
    printHex(Buf)
    Cs(0)
    Spi.write(Buf)
    Cs(1)
    
def MemWriteEnable():
    Cs(0)
    Spi.write(bytes([__WRITE_ENABLE]));
    Cs(1)
    
def MemWrite(Address, Buffer):
    print("size(Buffer)={}".format(len(Buffer)))
    
    MemWaitForReady()
    
    MemWriteEnable()
    
    Cmd = bytearray([__WRITE, (Address & 0xFF00)>>8, Address & 0x00FF])
    Cs(0)
    Spi.write(Cmd)
    Spi.write(Buffer)
    Cs(1)

def MemPageErase(Address):
    
    
def MemRead(Address, Buffer):
    print("size(Buffer)={}".format(len(Buffer)))
    Cmd = bytearray([__READ, (Address & 0xFF00)>>8, Address & 0x00FF])
    Cs(0)
    Spi.write(Cmd)
    Spi.readinto(Buffer)
    Cs(1)



def MemDump(Address, Length):

    print("Length: {}".format(Length))
    print("Addr:\t 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")
    
    # Rozpoczęcie odczytywania
    Cs(0)
    Spi.write(bytearray([__READ, (Address & 0xFF00)>>8, Address & 0x00FF]))
    
    while Length:
        Data = Spi.read(16)
        print("%04X" % Address + ":", end="\t")
        print(hexlify(Data, ' ').decode("ascii").upper(), end="   ")
        for Char in Data: print(chr(Char) if Char >= 32 else " ", end="")
        print("")
        
        Address += 16
        Length -= 16
        if Length <= 0:
            Cs(1)
            return
    

    
    
SpiInit()
#SpiTest()

#Res = MemStatusRead()
#print(Res)


#Buffer = bytearray(b'\x00' * 256)
#dump(Buffer)

#MemRead(0xABCD, Buffer)
#MemRead(0x0000, Buffer)
#dump(Buffer)


print(1)
MemWrite(0xFFA0, bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
print(2)
MemWrite(0xFFB0, bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
print(3)
MemWaitForReady()

MemDump(0xFF00, 0x0200)

