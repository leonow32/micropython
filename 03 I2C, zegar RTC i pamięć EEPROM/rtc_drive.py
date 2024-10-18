import machine
import gc
import os
import free_mem

RTC_SIZE = 2048
BYTES_IN_FILE = 16            # Ile bajtow zapisac w plikach podczas testu

class RtcDriveBlock:
    def __init__(self, BlockSize=128):
        print(f".init(BlockSize={BlockSize})")
        self.BlockSize = BlockSize

    def readblocks(self, block_num, buf, offset=0):
        print(f".readblocks(block_num={block_num}, len(buf)={len(buf)}, offset={offset})")
        Address = block_num * self.BlockSize + offset
        Data = bytearray(machine.RTC().memory())
        
        # Rozciaganie
        BytesToAdd = 2048-len(Data)
        Data = Data + bytes(b'\x00' * BytesToAdd)
        
        # Zapis do bufora wyjsciowego
        for i in range(len(buf)):
            buf[i] = Data[Address + i]

    def writeblocks(self, block_num, buf, offset=0):
        print(f".writeblocks(block_num={block_num}, len(buf)={len(buf)} offset={offset}")
        if offset is None:
            offset = 0
        
        # Odczytanie aktualnej pamieci
        Data = machine.RTC().memory()
        
        # Rozciaganie
        BytesToAdd = 2048-len(Data)
        Data = Data + bytes(b'\x00' * BytesToAdd)
        
        Address = block_num * self.BlockSize + offset
        
        if Address == 0:
            Data = buf + Data[len(buf):]
        else:
            Data = Data[0:Address] + buf + Data[Address+len(buf):]
        
        # Zapisanie w pamicie RTC
        machine.RTC().memory(Data)

    def ioctl(self, op, arg):
        print(f".ioctl(op={op}, arg={arg})\t", end="")
        
        # Init
        if op == 1:
            print("Init")
            pass
            
        # Shutdown
        if op == 2:
            print("Shutdown")
            pass
            
        # Sync
        if op == 3:
            print("Sync")
            pass
        
        # Number of blocks
        if op == 4:
            res = RTC_SIZE // self.BlockSize
            print(f"BlockCount={res}")
            return res
        
        # Block size
        if op == 5:
            print(f"BlockSize={BlockSize}")
            return self.BlockSize
        
        # Block erase
        if op == 6: 
            print(f"BlockErase={arg}")
            Data = machine.RTC().memory()
            Address = arg * self.BlockSize
            Empty = bytearray(b'\x00' * self.BlockSize)
            
            if Address == 0:
                Data = Empty + Data[self.BlockSize:]
            else:
                Data = Data[0:Address] + Empty + Data[Address+self.BlockSize:]
            machine.RTC().memory(Data)
            return 0
        
gc.collect()
BlockSize = 64 # oryginalnie 128

# kasowanie
machine.RTC().memory(bytes([0x00]*2048))

print(f"RamDrive = RtcDriveBlock(BlockSize={BlockSize})")
RamDrive = RtcDriveBlock(BlockSize)

try:
    print("os.VfsLfs2.mkfs()")
    os.VfsLfs2.mkfs(RamDrive)
    print("os.mount()")
    os.mount(RamDrive, '/rtc')
except OSError as Error:
    print(f"Error: {error}")

"""
# Create dummy content to store in files
content_to_write = bytearray()
for i in range(BYTES_IN_FILE):
    content_to_write += bytearray(b'x')             # instart multiple 'x' characters 

# Save as many files as possible
print("===== MULTIPLE SAVES =====")

i = 0
while True:
    name = f"/rtc/{i}.txt"
    print(f"Saving {name}")
    try:
        with open(name, "wb") as f:
            f.write(content_to_write)
        i += 1
    except:
        print(f"Error at {i}")
        break
        
# Try to read all saved files   
print("===== MULTIPLE READS =====")
files = i
for i in range(0, files):
    name = f"/rtc/{i}.txt"
    try:
        with open(name, "rb") as f:
            content = f.read()
            print(f"File {name} = {content}")
    except:
        print(f"File {name} = error")

"""
free_mem.ram_free()
