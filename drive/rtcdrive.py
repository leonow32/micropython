import machine
import gc
import uos
import ubinascii
import utime
from micropython import const
from micropython import mem_info

# Garbage Collector - automatic
gc.enable()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# Garbage Collector - manual
gc.collect()


# RAM Drive RTC
RtcDrive = 0
_RTC_SIZE = const(2048)
class RtcDriveBlock:
    def __init__(self, BlockSize=128):
        self.BlockSize = BlockSize
        
        # Read RTC memory and check if it has valid length
        self.Data = bytearray(machine.RTC().memory())
        if(len(self.Data) != _RTC_SIZE):
            self.Data = bytearray(b'\x00' * _RTC_SIZE)

    def readblocks(self, block_num, buf, offset=0):
        Address = block_num * self.BlockSize + offset
        buf[:] = self.Data[Address : Address + len(buf)]

    def writeblocks(self, block_num, buf, offset=0):
        if offset is None:
            offset = 0

        Address = block_num * self.BlockSize + offset
        self.Data[Address : Address + len(buf)] = buf
        machine.RTC().memory(self.Data)

    def ioctl(self, op, arg):
        
        # Number of blocks
        if op == 4:
            return _RTC_SIZE // self.BlockSize
        
        # Block size
        if op == 5:
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            Address = arg * self.BlockSize 
            self.Data[Address : Address + self.BlockSize] = bytearray(b'\x00' * self.BlockSize)
            machine.RTC().memory(self.Data)
            return 0


        



# Tworzenie RAM Drive RTC
def RtcCreate():

    global RtcDrive
    RtcDrive = RtcDriveBlock()
    
    try:
        try:
            print("Trying to mount RTC mem as it is now")
            uos.mount(RtcDrive, "/rtc")
        except:
            print("Failed; formatting memory as LittleFS2")
            uos.VfsLfs2.mkfs(RtcDrive)
            print("Mounting")
            uos.mount(RtcDrive, "/rtc")
            print("Done")
        else:
            print("Done, RTC has been already formatted as LittleFS2")
    except OSError as Error:
        print("Error: {}".format(Error))
      
# Likwidacja (ale bez czyszczenia, mozna potem zamontowac dysk ponownie)
def RtcRemove():
    uos.umount("/rtc")

# Czyszczenie pamięci RTC
def RtcClear():
    machine.RTC().memory(bytes([0x00]*2048))

# Zapisywanie testowych plików
def RtcTest(BytesInFile):

    # Create dummy content to store in files
    content_to_write = bytearray()
    for i in range(BytesInFile):
        content_to_write += bytearray('x')   # lub bytearray([i])

    # Save as many files as possible
    print("===== MULTIPLE SAVES =====")
    TimeStart = utime.ticks_us()
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
    print("Time: {}ms".format(utime.ticks_us()-TimeStart))
            
    # Try to read all saved files   
    print("===== MULTIPLE READS =====")
    TimeStart = utime.ticks_us()
    files = i
    for i in range(0, files):
        name = "/rtc/{}.txt".format(i)
        try:
            with open(name, "rb") as f:
                content = f.read()
                print("File {} = {}".format(name, content))
        except:
            print("File {} = error".format(name))
    print("Time: {}ms".format(utime.ticks_us()-TimeStart))


def printHex(arg):
    string = ubinascii.hexlify(arg, ' ').decode("utf-8")
    print(string)


def Test1():
    # Zapis
    try:
        with open("/rtc/test1.txt", "a") as f:
            f.write("Some content to write\r\n")
    except:
        print("Can't save")
        
    # Odczyt
    try:
        with open("/rtc/test1.txt") as f:
            print(f.read())
    except:
        print("Can't read")


def Test2():
    Data = bytearray(b'\x00\x01\x02\x03\x04')
    print(Data)
    print("len(Data)={}".format(len(Data)))
    
    # Zapis
    try:
        with open("/rtc/test2.bin", "a") as f:
            f.write(Data)
    except:
        print("Can't save")
        
    # Odczyt
    try:
        with open("/rtc/test2.bin") as f:
            Data = bytearray(f.read())
            print("type(Data)={}".format(type(Data)))
            print("Data={}".format(Data))
            printHex(Data)
    except:
        print("Can't read")

#RtcCreate()
#RtcTest(16)
