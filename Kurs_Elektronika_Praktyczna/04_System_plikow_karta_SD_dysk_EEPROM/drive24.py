# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import os

class DriveBlock:
    def __init__(self, memory, path):
        self.memory = memory
        self.path = path
        
        if memory.page_size < 64:
            self.block_size = 64
        else:
            self.block_size = memory.page_size
            
        try:
            os.mount(self, path)
        except:
            os.VfsLfs2.mkfs(self)
            os.mount(self, path)
            
    def format(self):
        os.VfsLfs2.mkfs(self)
    
    def deinit(self):
        os.umount(self.path)
        
    def readblocks(self, block_num, buf, offset=0):
        address = block_num * self.block_size + offset
        self.memory.read_into(address, buf)

    def writeblocks(self, block_num, buf, offset=0):
        if offset is None:
            offset = 0

        address = block_num * self.block_size + offset
        self.memory.write(address, buf)

    def ioctl(self, op, arg):
        
        # Number of blocks
        if op == 4:
            return self.memory.memory_size // self.block_size
        
        # Block size
        if op == 5:
            return self.block_size
        
        # Block erase
        if op == 6: 
            address = arg * self.block_size
            buffer = bytes(b'\x00' * self.block_size)
            self.memory.write(address, buffer)
            return 0
