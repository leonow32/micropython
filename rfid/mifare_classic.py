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
    
class MifareClassic():
    
    def __init__(self, pcd, iso):
        self.iso = iso
        self.pcd = pcd
    
    def validate_ack(self, recv_buf):
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
            raise Exception(f"unsupported ack response {recv_buf[0]}")
        
    def authenticate(self, uid: bytes|bytearray, block_adr:int, key_type:str, key: bytes|bytearray) -> None:
        self.pcd.authenticate(uid, 0, AUTH_KEY_A if key_type=="A" else AUTH_KEY_B, key)
        
    def read_block(self, block_adr: int) -> bytearray:
        send_buf = bytearray([READ, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
        
    def write_block(self, block_adr: int, data: bytes|bytearray) -> None:
        # First step
        send_buf = bytearray([WRITE, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
        # Second step
        send_buf = bytearray(data)
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
    def get_value(self, block_adr):
        """
        Reads and returns a value from a memory block. The value is a signed 32-bit variable.
        """
        data = self.read_block(block_adr)
        value = data[3] << 24 | data[2] << 16 | data[1] << 8 | data[0]
        
        # Convert binary to U2
        if value & 0x80000000:
            value = (value & 0x7FFFFFFF) - 0x80000000
            
        return value
    
    def set_value(self, block_adr: int, value: int) -> None:
        """
        Formats a block of memory to hold a 32-bit signed variable. Blocks formatted in this way can be manipulated using
        the mifare_value_increment, mifare_value_decrement, mifare_value_decrement, mifare_value_restore, and, of course,
        mifare_value_get functions.
        """
        
        # Convert value to bytearray
        x = bytearray(4)
        value = value & 0xFFFFFFFF
        x[0] = value & 0xFF
        x[1] = (value >> 8) & 0xFF
        x[2] = (value >> 16) & 0xFF
        x[3] = (value >> 24) & 0xFF
        
        send_buf = bytearray(16)
        send_buf[0]  = x[0]
        send_buf[1]  = x[1]
        send_buf[2]  = x[2]
        send_buf[3]  = x[3]
        send_buf[4]  = ~x[0] & 0xFF
        send_buf[5]  = ~x[1] & 0xFF
        send_buf[6]  = ~x[2] & 0xFF
        send_buf[7]  = ~x[3] & 0xFF
        send_buf[8]  = x[0]
        send_buf[9]  = x[1]
        send_buf[10] = x[2]
        send_buf[11] = x[3]
        send_buf[12] = block_adr
        send_buf[13] = ~block_adr & 0xFF
        send_buf[14] = block_adr
        send_buf[15] = ~block_adr & 0xFF
        
        self.write_block(block_adr, send_buf)
    
    def increment_value(self, block_adr: int, value: int) -> None:
        """
        This command increments the number in the specified block by the given value. The result of the operation is
        written to the Transfer Buffer. After executing this command, you must call the mifare_value_transfer function
        and specify the memory block where the result should be written.
        """
        # First step
        send_buf = bytearray([INCREMENT, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
        # Second step
        send_buf[0] = value & 0xFF
        send_buf[1] = (value >> 8) & 0xFF
        send_buf[2] = (value >> 16) & 0xFF
        send_buf[3] = (value >> 24) & 0xFF
        self.pcd.crc_calculate_and_append(send_buf)
        try:
            recv_buf = self.pcd.transmit(send_buf)
        except:
            return              # if this command does not respond and raises a timeout error - it means SUCCESSFUL operation
        
        # This may happen only if something goes wrong
        self.validate_ack(recv_buf)
    
    def decrement_value(self, block_adr: int, value: int) -> None:
        """
        This command decrements the number in the specified block by the given value. The result of the operation is
        written to the Transfer Buffer. After executing this command, you must call the mifare_value_transfer function
        and specify the memory block where the result should be written.
        """
        # First step
        send_buf = bytearray([DECREMENT, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
        # Second step
        send_buf[0] = value & 0xFF
        send_buf[1] = (value >> 8) & 0xFF
        send_buf[2] = (value >> 16) & 0xFF
        send_buf[3] = (value >> 24) & 0xFF
        self.pcd.crc_calculate_and_append(send_buf)
        try:
            recv_buf = self.pcd.transmit(send_buf)
        except:
            return              # if this command does not respond and raises a timeout error - it means SUCCESSFUL operation
        
        # This may happen only if something goes wrong
        self.validate_ack(recv_buf)
    
    def restore_value(self, block_adr: int) -> None:
        """
        Copy the value from a memory block into the Transfer Buffer.
        """
        # First step
        send_buf = bytearray([RESTORE, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
        # Second step
        send_buf[0] = 0
        send_buf[1] = 0
        send_buf[2] = 0
        send_buf[3] = 0
        self.pcd.crc_calculate_and_append(send_buf)
        try:
            recv_buf = self.pcd.transmit(send_buf)
        except:
            return              # if this command does not respond and raises a timeout error - it means SUCCESSFUL operation
        
        # This may happen only if something goes wrong
        self.validate_ack(recv_buf)
    
    def transfer_value(self, block_adr) -> None:
        """
        Copy the value from Transfer Buffer into a memory block.
        """
        send_buf = bytearray([TRANSFER, block_adr])
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
                data = self.read_block(address)
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
            
            print(" |")
            
    def dump_1k(self, uid, keys=None, use_authentication=True):
        
        # If key list is not provided then use default keys for each sector
        if keys == None:
            keys = list()
            for i in range(16):
                keys.append((AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"))  # Factory default key
#                 keys.append((AUTH_KEY_A, b"\xA3\x96\xEF\xA4\xE2\x4F"))  # Backdoor
#                 keys.append((AUTH_KEY_A, b"\xA3\x16\x67\xA8\xCE\xC1"))  # Backdoor
#                 keys.append((AUTH_KEY_A, b"\x51\x8B\x33\x54\xE7\x60"))  # Backdoor

        print("| Sector | Block |                       Data                      |       ASCII      |")
        print("|        |       |  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F |                  |")
        
        # Read 16 sectors with 4 blocks each
        for sector in range(16):
            self._dump_block(uid, keys[sector][0], keys[sector][1], sector, sector*4, sector*4+3, use_authentication)
            
    def dump_4k(self, uid, keys=None, use_authentication=True):
        
        # If key list is not provided then use default keys for each sector
        if keys == None:
            keys = list()
            for i in range(40):
                keys.append((AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"))  # Factory default key
#                 keys.append((AUTH_KEY_A, b"\xA3\x96\xEF\xA4\xE2\x4F"))  # Backdoor
#                 keys.append((AUTH_KEY_A, b"\xA3\x16\x67\xA8\xCE\xC1"))  # Backdoor
#                 keys.append((AUTH_KEY_A, b"\x51\x8B\x33\x54\xE7\x60"))  # Backdoor

        # Print header
        print("| Sector | Block |                       Data                      |       ASCII      |")
        print("|        |       |  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F |                  |")
        
        # First, read 32 sectors with 4 blocks each
        for sector in range(32):
            self._dump_block(uid, keys[sector][0], keys[sector][1], sector, sector*4, sector*4+3, use_authentication)
            
        # Second, read 8 sectors with 16 blocks each
        for sector in range(32, 40):
            self._dump_block(uid, keys[sector][0], keys[sector][1], sector, 128+(sector-32)*16, 15+128+(sector-32)*16, use_authentication)    
            
    def backdoor_enable(self):
        """
        This function enables backdoor in some Chinese counterfeit MIFARE cards.
        """
        self.pcd.crypto1_stop()
        self.pcd.antenna_disable()
        self.pcd.antenna_enable()
        
        # At first try to send 40 or 4F command in 7-bit mode
        try:
            self.pcd.transmit_7bit(BACKDOOR_40_7bit)
        except:
            try:
                self.pcd.transmit_7bit(BACKDOOR_4F_7bit)
            except:
                raise Exception("Can't execute the backdoor command")
            
        try:
            send_buf = bytearray([GOD_MODE])
            self.pcd.crc_calculate_and_append(send_buf)
            recv_buf = self.pcd.transmit(send_buf)
        except:
            raise Exception("Can't execute the God Mode command")
        
        self.validate_ack(recv_buf)
        
    def backdoor_try_keys(self):
        keys = (
            b"\xA3\x96\xEF\xA4\xE2\x4F",
            b"\xA3\x16\x67\xA8\xCE\xC1",
            b"\xFF\xFF\xFF\xFF\xFF\xFF",
            b"\x51\x8B\x33\x54\xE7\x60",
        )

        for key in keys:
            self.pcd.crypto1_stop()
            self.pcd.antenna_disable()
            self.pcd.antenna_enable()
            
            try:
                uid, atqa, sak = self.picc_scan_and_select()
            except:
                pass
            
            print("Testing key ", end="")
            for byte in key:
                print(f"{byte:02X} ", end="")
            
            try:
                self.pcd.authenticate(uid, 4, AUTH_KEY_A, key)
                print(" - ok")
            except:
                print(" - fail")
                
if __name__ == "__main__":
    import mem_used
    import measure_time
    from machine import Pin, SPI
    import rfid.rc522
    import rfid.iso_iec_14443_3
    from rfid.log import *
    
    spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    rst = Pin(7)

    pcd = rfid.rc522.RC522(spi, cs, rst)
    
    iso = rfid.iso_iec_14443_3.ISO_IEC_14443_3(pcd)
    
    mif = MifareClassic(pcd, iso)
    
    uid, atqa, sak = iso.scan_and_select()
    print("Card found")
    debug("UID", uid)
    print(f"ATQA: {atqa:04X}")
    print(f"SAK:  {sak:02X}")

        
    
#     pcd.debug = False
#     mif.dump_1k(uid)
    key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    pcd.authenticate(uid, 0, AUTH_KEY_A, key)
    data = mif.read_block(0)
    debug("Block 0", data)
    
    mem_used.print_ram_used()
    