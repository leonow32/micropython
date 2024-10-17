import machine
import gc
import uos
import ubinascii
import utime
from micropython import const
from micropython import mem_info

# Garbage Collector
gc.enable()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# RAM Drive
RamDrive = 0
class RamDriveBlock:
    def __init__(self, MemSize, BlockSize=128):
        self.BlockSize = BlockSize
        self.Data = bytearray(b'\x00' * MemSize)

    def readblocks(self, block_num, buf, offset=0):
        Address = block_num * self.BlockSize + offset
        buf[:] = self.Data[Address : Address + len(buf)]

    def writeblocks(self, block_num, buf, offset=0):
        if offset is None:
            offset = 0

        Address = block_num * self.BlockSize + offset
        self.Data[Address : Address + len(buf)] = buf

    def ioctl(self, op, arg):
        
        # Number of blocks
        if op == 4:
            return len(self.Data) // self.BlockSize
        
        # Block size
        if op == 5:
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            Address = arg * self.BlockSize 
            self.Data[Address : Address + self.BlockSize] = bytearray(b'\x00' * self.BlockSize)
            return 0






# Tworzenie RAM Drive
def RamCreate(Size):

    global RamDrive
    RamDrive = RamDriveBlock(Size)
    
    try:
        try:
            print("===mount===")
            uos.mount(RamDrive, "/ram")
        except:
            print("===Vfs===")
            uos.VfsLfs2.mkfs(RamDrive)
            print("===mount===")
            uos.mount(RamDrive, "/ram")
    except OSError as Error:
        print("Error: {}".format(Error))
      
# Likwidacja (ale bez czyszczenia, mozna potem zamontowac dysk ponownie)
def RamRemove():
    uos.umount("/ram")
    global RamDrive
    del RamDrive

# Zapisywanie testowych plików
def RamTest(BytesInFile):

    # Create dummy content to store in files
    content_to_write = bytearray()
    for i in range(BytesInFile):
        content_to_write += bytearray(b'x')   # lub bytearray([i])

    # Save as many files as possible
    #print("===== MULTIPLE SAVES =====")
    TimeStart = utime.ticks_us()
    i = 0
    while True:
        name = "/ram/{}.txt".format(i)
        #print("Saving {}".format(name))
        try:
            with open(name, "wb") as f:
                f.write(content_to_write)
            i += 1
        except:
            print("Error at {}".format(i))
            break
    print("Time: {}ms".format(utime.ticks_us()-TimeStart))
            
    # Try to read all saved files   
    #print("===== MULTIPLE READS =====")
    TimeStart = utime.ticks_us()
    files = i
    for i in range(0, files):
        name = "/ram/{}.txt".format(i)
        try:
            with open(name, "rb") as f:
                content = f.read()
                #print("File {} = {}".format(name, content))
        except:
            print("File {} = error".format(name))
    print("Time: {}ms".format(utime.ticks_us()-TimeStart))


RamCreate(2048)
RamTest(16)
