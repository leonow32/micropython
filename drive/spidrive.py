import machine
import gc
import uos
import ubinascii
import utime
from micropython import const
from micropython import mem_info
from machine import Pin
from machine import SPI

# Garbage Collector
gc.enable()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

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


Spi = 0
Cs = 0  

# SPI Drive
SpiDrive = 0
class SpiDriveBlock:
    
    
    
    def __init__(self):
        self.Spi = SPI(2, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        self.Cs = Pin(5, Pin.OUT)
        self.Cs.value(1)

    def readblocks(self, block_num, buf, offset=0):
        Address = block_num * 128 + offset
        Cmd = bytearray([__READ, (Address & 0xFF00)>>8, Address & 0x00FF])
        self.Cs(0)
        self.Spi.write(Cmd)
        self.Spi.readinto(buf)
        self.Cs(1)

    def writeblocks(self, block_num, buf, offset=0):
        if offset is None:
            offset = 0
            
        Address = block_num * 128 + offset
        
        # Wait for ready
        Buf = bytearray([__STATUS_READ, 0])
        while True:
            self.Cs(0)
            self.Spi.write_readinto(Buf, Buf)
            self.Cs(1)
            if Buf[1] & 0x01 == 0:
                return
            print(".", end="")
        
        # Write enable
        self.Cs(0)
        self.Spi.write(bytes([__WRITE_ENABLE]));
        self.Cs(1)
        
        # Write
        Cmd = bytearray([__WRITE, (Address & 0xFF00)>>8, Address & 0x00FF])
        self.Cs(0)
        self.Spi.write(Cmd)
        self.Spi.write(buf)
        self.Cs(1)

        Address = block_num * 128 + offset
        self.Data[Address : Address + len(buf)] = buf

    def ioctl(self, op, arg):
        
        # Number of blocks
        if op == 4:
            return 65536 // 128
        
        # Block size
        if op == 5:
            return 128
        
        # Block erase
        if op == 6: 
            blank = bytearray(b'\x00' * 128)
            self.writeblocks(arg, blank)
            return 0






# Tworzenie SPI Drive
def SpiCreate():

    global SpiDrive
    SpiDrive = SpiDriveBlock()
    
    try:
        try:
            print("===mount===")
            uos.mount(SpiDrive, "/spi")
        except:
            print("===Vfs===")
            uos.VfsLfs2.mkfs(SpiDrive)
            print("===mount===")
            uos.mount(SpiDrive, "/spi")
    except OSError as Error:
        print("Error: {}".format(Error))
      
# Likwidacja (ale bez czyszczenia, mozna potem zamontowac dysk ponownie)
def SpiRemove():
    uos.umount("/spi")
    global SpiDrive
    del SpiDrive

# Zapisywanie testowych plików
def SpiTest(BytesInFile):

    # Create dummy content to store in files
    content_to_write = bytearray()
    for i in range(BytesInFile):
        content_to_write += bytearray('x')   # lub bytearray([i])

    # Save as many files as possible
    #print("===== MULTIPLE SAVES =====")
    TimeStart = utime.ticks_us()
    i = 0
    while True:
        name = "/spi/{}.txt".format(i)
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
        name = "/spi/{}.txt".format(i)
        try:
            with open(name, "rb") as f:
                content = f.read()
                #print("File {} = {}".format(name, content))
        except:
            print("File {} = error".format(name))
    print("Time: {}ms".format(utime.ticks_us()-TimeStart))




SpiCreate()
#SpiTest(16)
