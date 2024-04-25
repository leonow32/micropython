from ubinascii import hexlify

def printHex(Data, MaxInRow=16):
    if Data == None:
        print("None")
        return
    
    Index = 0
    for Byte in Data:
        print("{:02X}".format(Byte), end=" ")
        Index += 1
        if Index % MaxInRow == 0:
            print("")
            
def printHex2(Data, Address=0, MaxInRow=16):
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


# Test
Content = bytearray()
for i in range(256+49):
    Content += bytearray([i])   # lub bytearray([i])

#print(Content)
printHex2(Content)