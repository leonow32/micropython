import machine
import gc
import os
import time

# RAM Drive
RamDrive = 0
class RamDriveBlock:
    def __init__(self, MemSize, BlockSize=64):
        print(f".init(BlockSize={BlockSize})")
        self.BlockSize = BlockSize
        self.Data = bytearray(b'\x00' * MemSize)

    def readblocks(self, block_num, buf, offset=0):
        #print(f".readblocks(block_num={block_num}, len(buf)={len(buf)}, offset={offset})")
        Address = block_num * self.BlockSize + offset
        buf[:] = self.Data[Address : Address + len(buf)]

    def writeblocks(self, block_num, buf, offset=0):
        print(f".writeblocks(block_num={block_num}, len(buf)={len(buf)} offset={offset}")
        if offset is None:
            offset = 0

        Address = block_num * self.BlockSize + offset
        self.Data[Address : Address + len(buf)] = buf

    def ioctl(self, op, arg):
        #print(f".ioctl(op={op}, arg={arg})\t", end="")
        
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
            res = len(self.Data) // self.BlockSize
            #print(f"BlockCount={res}")
            return res
        
        # Block size
        if op == 5:
            #print(f"BlockSize={self.BlockSize}")
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            #print(f"BlockErase={arg}")
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
            os.mount(RamDrive, "/ram")
        except:
            print("===Vfs===")
            os.VfsLfs2.mkfs(RamDrive)
            print("===mount===")
            os.mount(RamDrive, "/ram")
    except OSError as Error:
        print(f"Error: {Error}")
      
# Likwidacja (ale bez czyszczenia, mozna potem zamontowac dysk ponownie)
def RamRemove():
    os.umount("/ram")
    global RamDrive
    del RamDrive

# Zapisywanie testowych plików
def RamTest(BytesInFile):

    # Create dummy content to store in files
    content_to_write = bytearray()
    for i in range(BytesInFile):
        content_to_write += bytearray(b'x')   # lub bytearray([i])

    # Save as many files as possible
    print("===== MULTIPLE SAVES =====")
    TimeStart = time.ticks_us()
    i = 0
    while True:
        name = f"/ram/{i}.txt"
        print(f"Writing {name}")
        try:
            with open(name, "wb") as f:
                f.write(content_to_write)
            i += 1
        except:
            print(f"Error at {i}")
            break
    print(f"Time: {time.ticks_us()-TimeStart} us")
            
    # Try to read all saved files   
    print("===== MULTIPLE READS =====")
    TimeStart = time.ticks_us()
    files = i
    for i in range(0, files):
        name = f"/ram/{i}.txt"
        print(f"Reading {name}")
        try:
            with open(name, "rb") as f:
                content = f.read()
                #print(f"File {name} = {content}")
        except:
            print(f"File {name} = error")
    print(f"Time: {time.ticks_us()-TimeStart} us")

RamCreate(2048)
RamTest(16)
