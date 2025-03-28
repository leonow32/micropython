# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C
import gc
import os
import mem24
import time

# DEVICE_ADDRESS = 0x50
# MEMORY_SIZE = 4096
# BLOCK_SIZE = 64
# PAGE_SIZE = 32
# WRITE_DELAY_MS = 2



#drive = 0

class DriveBlock:
    def __init__(self, memory):
#         print(f".init()")
        self.memory = memory
        
        if memory.page_size < 64:
#             print(f"memory.page_size = {self.memory.page_size}")
            self.block_size = 64
        else:
            self.block_size = memory.page_size
        
    def readblocks(self, block_num, buf, offset=0):
#         print(f".readblocks(block_num={block_num}, len(buf)={len(buf)}, offset={offset})")
        address = block_num * self.block_size + offset
#         i2c.readfrom_mem_into(DEVICE_ADDRESS, address, buf, addrsize=16)
        
        self.memory.read_into(address, buf)

    def writeblocks(self, block_num, buf, offset=0):
#         print(f".writeblocks(block_num={block_num}, len(buf)={len(buf)} offset={offset}")
        
        if offset is None:
            offset = 0
            print("offset is None")

        address = block_num * self.block_size + offset
        
        self.memory.write(address, buf)
        
        
#         length = len(buf)
#         fragment = 0
#         
#         while length >= PAGE_SIZE:
#             i2c.writeto_mem(DEVICE_ADDRESS, address, buf[fragment : fragment+PAGE_SIZE], addrsize=16)
#             time.sleep_ms(WRITE_DELAY_MS)
#             length   -= PAGE_SIZE
#             address  += PAGE_SIZE
#             fragment += PAGE_SIZE

    def ioctl(self, op, arg):
#         print(f".ioctl(op={op}, arg={arg})\t", end="")
        
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
            res = self.memory.memory_size // self.block_size
#             print(f"BlockCount={res}")
            return res
        
        # Block size
        if op == 5:
            res = self.block_size
#             print(f"BlockSize={res}")
            return res
        
        # Block erase
        if op == 6: 
#             print(f"BlockErase={arg}")
            address = arg * self.block_size
            buffer = bytes(b'\x00' * self.block_size)
            
            self.memory.write(address, buffer)
            
            
#             i2c.writeto_mem(DEVICE_ADDRESS, address, data_to_write, addrsize=16)
#             time.sleep_ms(WRITE_DELAY_MS)
#             i2c.writeto_mem(DEVICE_ADDRESS, address + PAGE_SIZE, data_to_write, addrsize=16)
#             time.sleep_ms(WRITE_DELAY_MS)
            return 0
    
#     def format_disk(self):
#         print("format_disk")
#         global drive
#         os.VfsLfs2.mkfs(drive)
#         
#     def mount_disk(self):
#         print("mount")
#         global drive
#         os.mount(drive, "/at24c32")

# Tworzenie RAM Drive
"""
def drive_create():

    global drive
    drive = DriveBlock()
    
    try:
        try:
            print("===mount===")
            #os.mount(drive, "/at24c32")
            drive.mount_disk()
        except:
            print("===Vfs===")
            #os.VfsLfs2.mkfs(drive)
            drive.format_disk()
            print("===mount===")
            #os.mount(drive, "/at24c32")
            drive.mount_disk()
    except OSError as Error:
        print(f"Error: {Error}")
      """

# Likwidacja (ale bez czyszczenia, mozna potem zamontowac dysk ponownie)
def drive_remove():
    os.umount("/at24c32")
    global drive
    del drive

# Zapisywanie testowych plików
def drive_test(path, bytes_in_file):

    # Create dummy content to store in files
    content_to_write = bytearray()
    for i in range(bytes_in_file):
        content_to_write += bytearray(b'x')   # lub bytearray([i])

    # Save as many files as possible
    print("===== MULTIPLE SAVES =====")
    TimeStart = time.ticks_ms()
    i = 0
    while True:
        name = f"{path}/{i}.txt"
        print(f"Writing {name}")
        try:
            with open(name, "wb") as f:
                f.write(content_to_write)
            i += 1
        except:
            print(f"Error at {i}")
            break
    print(f"Time: {time.ticks_ms()-TimeStart} ms")
            
    # Try to read all saved files   
    print("===== MULTIPLE READS =====")
    TimeStart = time.ticks_ms()
    files = i
    for i in range(0, files):
        name = f"{path}/{i}.txt"
        print(f"Reading {name}")
        try:
            with open(name, "rb") as f:
                content = f.read()
                #print(f"File {name} = {content}")
        except:
            print(f"File {name} = error")
    print(f"Time: {time.ticks_ms()-TimeStart} ms")

if __name__ == "__main__":
    i2c    = I2C(0)
#     eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=4096, page_size=32, addr_size=16)
    eeprom = mem24.Mem24(i2c, device_address=0x50, memory_size=65536, page_size=128, addr_size=16)
    drive  = DriveBlock(eeprom)
    
    print("format")
    os.VfsLfs2.mkfs(drive)
    
    print("mount")
    os.mount(drive, "/eeprom")
    
    
#     drive = DriveBlock()
#     drive.format_disk()
#     drive.mount_disk()
    drive_test("/eeprom", 1000)


