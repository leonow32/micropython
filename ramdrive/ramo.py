import machine
import gc
import uos

# Oryginalna klasa do ramdrive
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        print("R init")
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)
        print("BlockSize  = {}".format(block_size))
        print("len(Data) = {}".format(len(self.data)))
        print("BlockCount = {}".format(num_blocks))
        print("===")

    def readblocks(self, block_num, buf, offset=0):
        print("readblocks(block_num={}, len(buf)={}, type(buf)={}, offset={})".format(block_num, len(buf), type(buf), offset))
        addr = block_num * self.block_size + offset
        for i in range(len(buf)):
            buf[i] = self.data[addr + i]
        print(buf)
        print("len(buf)={}, type(buf)={}".format(len(buf), type(buf)))
        print("===")

    def writeblocks(self, block_num, buf, offset=None):
        print("writeblocks(block_num={}, len(buf)={}, type(buf)={}, offset={})".format(block_num, len(buf), type(buf), offset))
        print(buf)
        if offset is None:
            # do erase, then write
            for i in range(len(buf) // self.block_size):
                self.ioctl(6, block_num + i)
            offset = 0
        addr = block_num * self.block_size + offset
        print("Address = {}".format(addr))
        for i in range(len(buf)):
            self.data[addr + i] = buf[i]
        print("===")

    def ioctl(self, op, arg):
        print("ioctl(op={}, arg={}) ".format(op, arg), end='')
        
        # Init
        if op == 1:
            print("Init")
           
        # Shutdown
        if op == 2:
            print("Shutdown")
            
        # Sync
        if op == 3:
            print("Sync")
        
        # Numer of blocks
        if op == 4:
            print("BlockCount={}".format(len(self.data) // self.block_size))
            return len(self.data) // self.block_size
        
        # Block size
        if op == 5:
            print("BlockSize={}".format(self.block_size))
            return self.block_size
        
        # Block erase
        if op == 6:
            print("BlockErase={}".format(arg))
            return 0
        
    def dump(self):
        print("type(self.data)={}".format(type(self.data)))
        print(self.data)

block_size = 64
num_blocks = 32
bdev = RAMBlockDev(block_size, num_blocks)
print("===Vfs===")
uos.VfsLfs2.mkfs(bdev)
print("===mount===")
uos.mount(bdev, '/ramo')

print("=== DUMP ===")
bdev.dump()