from rfid.log import *

# MIFARE Classic commands
AUTH_KEY_A = const(0x60) # Perform sector authentication with key A
AUTH_KEY_B = const(0x61) # Perform sector authentication with key B
READ       = const(0x30) # Read 16-byte block (must be authenticated)
WRITE      = const(0xA0) # Write 16-byte block (must be authenticated)
DECREMENT  = const(0xC0) # Decrement value of the block (must be authenticated)
INCREMENT  = const(0xC1) # Increment value of the block (must be authenticated)
RESTORE    = const(0xC2) # Copy value from the block to transfer buffer (must be authenticated)
TRANSFER   = const(0xB0) # Copy value from transfer buffer to the block (must be authenticated)

# Backdoor commands
BACKDOOR_40_7bit = const(0x40) # Unlocks some Chinese MIFARE Classic cards
BACKDOOR_4F_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
GOD_MODE         = const(0x43) # Access restricted blocks without authentication
    
class MifareUltralight():
    
    def __init__(self, pcd, iso):
        self.iso = iso
        self.pcd = pcd
    
    def validate_ack(self, recv_buf):
        if len(recv_buf) != 1:
            raise Exception(f"Wrong response length ({len(recv_buf)}), should be 1")
        
        if recv_buf[0] == 0x0A:
            return
        elif recv_buf[0] == 0x00:
            raise Exception("buffer valid, operation invalid")
        elif recv_buf[0] == 0x01:
            raise Exception("buffer valid, parity or CRC error")
        elif recv_buf[0] == 0x04:
            raise Exception("buffer invalid, operation invalid")
        elif recv_buf[0] == 0x05:
            raise Exception("buffer invalid, parity or CRC error")
        else:
            raise Exception(f"Unsupported ACK response {recv_buf[0]:02X}")
        
    def block_read(self, block_adr: int) -> bytearray:
        """
        Read 16 bytes of data (4 blocks).
        """
        send_buf = bytearray([READ, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
        
    def block_write(self, block_adr: int, data: bytes|bytearray) -> None:
        """
        Write 4-byte block.
        """
        send_buf = bytearray(6)
        send_buf[0] = WRITE
        send_buf[1] = block_adr
        send_buf[2] = data[0]
        send_buf[3] = data[1]
        send_buf[4] = data[2]
        send_buf[5] = data[3]
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
    def _dump_block(self, uid, key_ab, key_value, sector, block_start, block_end, use_authentication=True):
        if use_authentication:
            try:
                self.pcd.authenticate(uid, block_start, key_ab, key_value)
            except:
                print(f"Can't authenticate block {block_start}")
                self.iso.wupa()
                self.iso.select(uid)
                return
        
        for address in range(block_start, block_end+1):
            # Read the block
            try:
                data = self.block_read(address)
            except:
                print(f"Can't read block {address}")
                return
            
            # Print the result
            if address == block_start:
                print(f"| {sector:6} ", end="")
            else:
                print("|        ", end="")
                
            print(f"| {address:5} | ", end="")
            
            for byte in data:
                print(f"{byte:02X} ", end="")
            
            print("| ", end="")
            
            for byte in data:
                if byte >= 32 and byte <= 126:
                    print(chr(byte), end="")
                else:
                    print(" ", end="")
            
            print(" | ", end="")
            
            value = self.value_check(data)
            if(value is not False):
                print(value)
            else:
                print()
                
    def dump2(self):
        print("Block | Data        | ASCII | Comment", end="")
        
        for block in range(0, 16, 4):
            data = self.block_read(block)
            
            
            
    def dump(self):
        print("Block | Data        | ASCII | Comment", end="")
        
        for block in range(0, 16, 4):
            data = self.block_read(block)
            
            for i in range(16):
                if i%4 == 0:
                    print(f"\n{(block+i//4):5} | ", end="")
                    
                print(f"{data[i]:02X} ", end="")
            
            
        
                
if __name__ == "__main__":
    from machine import Pin, SPI
    from rfid.rc522 import RC522
    from rfid.iso_iec_14443_3 import ISO_IEC_14443_3
    from rfid.log import *

    spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    rst = Pin(7)
    pcd = RC522(spi, cs, rst)
    iso = ISO_IEC_14443_3(pcd)
    mif = MifareUltralight(pcd, iso)
    
    uid, _, _ = iso.scan_and_select()
    
    debug_disable()
    mif.dump()
    