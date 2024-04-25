import machine
import gc
import uos
import ubinascii
from micropython import const
from micropython import mem_info

#dummybytes = bytearray(b'\xff' * 35800)

def printHex(arg):
    #string = ubinascii.hexlify(arg, ' ').decode("utf-8")
    string = ubinascii.hexlify(arg).decode("utf-8")
    print(string, end=" ")

    #num = 0
    for i in arg:
        try:
            t = i.decode("utf-8")
            print(i, end="")
        except:
            print(" ", end="")
        #num += 1
        #print(num)
        #if num % 16 == 0:
        #    print("x")
    print(" ")


def test():
    temp = bytearray()
    for i in range(256):
        temp += bytearray([i])
        
    printHex(temp)
    
"""
# Ram Drive RTC - nowy
_RTC_SIZE = const(2048)
class RtcDriveBlock:
    def __init__(self, BlockSize=128):
        #print("R init")
        self.BlockSize = BlockSize
        #print("BlockSize  = {}".format(BlockSize))
        #print("len(Data) = {}".format(2048))
        #print("BlockCount = {}".format(2048 // BlockSize))
        #print("===")
        
        # Read RTC memory and check if it has valid length
        self.Data = bytearray(machine.RTC().memory())
        if(len(self.Data) != _RTC_SIZE):
            self.Data = bytearray(b'\x00' * _RTC_SIZE)

    def readblocks(self, block_num, buf, offset=0):
        #print("=== read  {} {} {}".format(block_num, len(buf), offset), end="\t")
        Address = block_num * self.BlockSize + offset
        #Data = bytearray(machine.RTC().memory())
        
        # Rozciaganie
        #BytesToAdd = 2048-len(Data)
        #Data = Data + bytes(b'\x00' * BytesToAdd)
        
        # Zapis do bufora wyjsciowego
        #for i in range(len(buf)):
        #    buf[i] = self.Data[Address + i]
        
        #buf[0 : len(buf)] = self.Data[Address : Address + len(buf)]
        buf[:] = self.Data[Address : Address + len(buf)]
        
        # Debug
        #printHex(buf)

    def writeblocks(self, block_num, buf, offset=0):
        #print("=== write {} {} {}".format(block_num, len(buf), offset), end="\t")
        if offset is None:
            offset = 0
        
        # Odczytanie aktualnej pamieci
        #Data = machine.RTC().memory()
        
        # Rozciaganie
        #BytesToAdd = 2048-len(Data)
        #Data = Data + bytes(b'\x00' * BytesToAdd)
        #print("len(Data)={}, BytesToAdd={}".format(len(Data), BytesToAdd))
        
        Address = block_num * self.BlockSize + offset
        #print("Address = {}".format(Address))
        
        # Wstawienie nowego bufora w blok danych
        self.Data[Address : Address + len(buf)] = buf
        
        #if Address == 0:
        #    #Data = buf + Data[len(buf):]
        #    self.Data[0:len(buf)] = buf
        #else:
        #    #Data = Data[0:Address] + buf + Data[Address+len(buf):]
        #    self.Data[Address : Address+len(buf)] = buf
        
        # Debug
        #printHex(buf)
        
        # Zapisanie w pamicie RTC
        machine.RTC().memory(self.Data)

    def ioctl(self, op, arg):
        #print("=== ioctl {} {} ".format(op, arg), end='')
        
        # Init
        if op == 1:
            #print("Init")
            pass
            
        # Shutdown
        if op == 2:
            #print("Shutdown")
            pass
            
        # Sync
        if op == 3:
            #print("Sync")
            pass
        
        # Number of blocks
        if op == 4:
            res = _RTC_SIZE // self.BlockSize
            #print("BlockCount={}".format(res))
            return res
        
        # Block size
        if op == 5:
            #print("BlockSize={}".format(self.BlockSize))
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            #print("BlockErase={}".format(arg))
            #Data = machine.RTC().memory()
            Address = arg * self.BlockSize
            #Empty = bytearray(b'\x00' * self.BlockSize)
            
            self.Data[Address : Address + self.BlockSize] = bytearray(b'\x00' * self.BlockSize)
            #if Address == 0:
            #    #Data = Empty + Data[self.BlockSize:]
            #    self.Data[0 : self.BlockSize] = bytearray(b'\x00' * self.BlockSize)
            #else:
            #    Data = Data[0:Address] + Empty + Data[Address+self.BlockSize:]
            #    self.Data[]
            machine.RTC().memory(self.Data)
            return 0
"""

# Ram Drive RTC - stary
_RTC_SIZE = const(2048)
class RtcDriveBlock:
    def __init__(self, BlockSize=128):
        #print("R init")
        self.BlockSize = BlockSize
        #print("BlockSize  = {}".format(BlockSize))
        #print("len(Data) = {}".format(2048))
        #print("BlockCount = {}".format(2048 // BlockSize))
        #print("===")
        
        # Read RTC memory and check if it has valid length
        #self.Data = bytearray(machine.RTC().memory())
        
        #if(len(self.Data) != _RTC_SIZE):
        #    self.Data = bytearray(b'\x00' * _RTC_SIZE)

    def readblocks(self, block_num, buf, offset=0):
        #print("=== read  {} {} {}".format(block_num, len(buf), offset), end="\t")
        Address = block_num * self.BlockSize + offset
        Data = bytearray(machine.RTC().memory())
        
        # Rozciaganie
        BytesToAdd = 2048-len(Data)
        Data = Data + bytes(b'\x00' * BytesToAdd)
        
        # Zapis do bufora wyjsciowego
        for i in range(len(buf)):
            buf[i] = Data[Address + i]
        
        #buf[0 : len(buf)] = self.Data[Address : Address + len(buf)]
        #buf[:] = self.Data[Address : Address + len(buf)]
        
        # Debug
        #printHex(buf)

    def writeblocks(self, block_num, buf, offset=0):
        #print("=== write {} {} {}".format(block_num, len(buf), offset), end="\t")
        if offset is None:
            offset = 0
        
        # Odczytanie aktualnej pamieci
        Data = machine.RTC().memory()
        
        # Rozciaganie
        BytesToAdd = 2048-len(Data)
        Data = Data + bytes(b'\x00' * BytesToAdd)
        #print("len(Data)={}, BytesToAdd={}".format(len(Data), BytesToAdd))
        
        Address = block_num * self.BlockSize + offset
        #print("Address = {}".format(Address))
        
        # Wstawienie nowego bufora w blok danych
        #self.Data[Address : Address + len(buf)] = buf
        
        if Address == 0:
            Data = buf + Data[len(buf):]
            #self.Data[0:len(buf)] = buf
        else:
            Data = Data[0:Address] + buf + Data[Address+len(buf):]
            #self.Data[Address : Address+len(buf)] = buf
        
        # Debug
        #printHex(buf)
        
        # Zapisanie w pamicie RTC
        machine.RTC().memory(Data)

    def ioctl(self, op, arg):
        #print("=== ioctl {} {} ".format(op, arg), end='')
        
        # Init
        if op == 1:
            #print("Init")
            pass
            
        # Shutdown
        if op == 2:
            #print("Shutdown")
            pass
            
        # Sync
        if op == 3:
            #print("Sync")
            pass
        
        # Number of blocks
        if op == 4:
            res = _RTC_SIZE // self.BlockSize
            #print("BlockCount={}".format(res))
            return res
        
        # Block size
        if op == 5:
            #print("BlockSize={}".format(self.BlockSize))
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            #print("BlockErase={}".format(arg))
            Data = machine.RTC().memory()
            Address = arg * self.BlockSize
            Empty = bytearray(b'\x00' * self.BlockSize)
            
            
            if Address == 0:
                Data = Empty + Data[self.BlockSize:]
                #self.Data[0 : self.BlockSize] = bytearray(b'\x00' * self.BlockSize)
            else:
                Data = Data[0:Address] + Empty + Data[Address+self.BlockSize:]
            machine.RTC().memory(Data)
            return 0

        
gc.collect()
BlockSize = 128

# kasowanie
machine.RTC().memory(bytes([0x00]*2048))

RamDrive = RtcDriveBlock(BlockSize)
#print("RamDrive = {}".format(RamDrive))

try:
    print("===Vfs===")
    uos.VfsLfs2.mkfs(RamDrive)
    print("===mount===")
    uos.mount(RamDrive, '/rtc')
except OSError as Error:
    print("Error: {}".format(Error))
    

BYTES_IN_FILE = 16

# Create dummy content to store in files
content_to_write = bytearray()
for i in range(BYTES_IN_FILE):
    # inserty bytes from 00 to BYTES_IN_FILE
    #content_to_write += bytearray([i])   
    
    # instart multiple 'x' characters 
    content_to_write += bytearray('x')  


# Save as many files as possible
print("===== MULTIPLE SAVES =====")

i = 0
while True:
    name = "/rtc/{}.txt".format(i)
    print("Saving {}".format(name))
    try:
        with open(name, "wb") as f:
            f.write(content_to_write)
        i += 1
    except:
        print("Error at {}".format(i))
        break
        
# Try to read all saved files   
print("===== MULTIPLE READS =====")
files = i
for i in range(0, files):
    name = "/rtc/{}.txt".format(i)
    try:
        with open(name, "rb") as f:
            content = f.read()
            print("File {} = {}".format(name, content))
    except:
        print("File {} = error".format(name))

