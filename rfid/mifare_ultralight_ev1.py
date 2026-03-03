from rfid.log import *

# Driver for MF0UL11 and MF0UL21

# MIFARE Ultralight EV1 commands
GET_VERSION = const(0x60)
READ        = const(0x30) # Read 16 bytes = 4 blocks
FAST_READ   = const(0x3A)
WRITE       = const(0xA2) # Write 4 bytes = 1 block
READ_CNT    = const(0x39)
INCR_CNT    = const(0xA5)
PWD_AUTH    = const(0x1B)
READ_SIG    = const(0x3C)
CHECK_T_EV  = const(0x3E) # Chech teating even
VCSL        = const(0x4B)

BLOCK_COUNT  = const(20)
BLOCK_LENGTH = const(4)
   
class MifareUltralightEV1():
    
    def __init__(self, pcd):
        self.pcd = pcd
    
    def validate_ack(self, recv_buf):
        if len(recv_buf) != 1:
            raise Exception(f"Wrong response length ({len(recv_buf)}), should be 1")
        
        if recv_buf[0] == 0x0A:
            return
        elif recv_buf[0] == 0x00:
            raise Exception("NAK for invalid argument")
        elif recv_buf[0] == 0x01:
            raise Exception("NAK for parity or CRC error")
        elif recv_buf[0] == 0x04:
            raise Exception("NAK for counter overflow")
        elif recv_buf[0] == 0x05 or recv_buf[0] == 0x07:
            raise Exception("NAK for EEPROM write error")
        elif recv_buf[0] == 0x06 or recv_buf[0] == 0x09:
            raise Exception("NAK for other error")
        else:
            raise Exception(f"Unsupported ACK response {recv_buf[0]:02X}")
        
    def version_get(self):
        """
        This function sends GET_VERSION to the card and returns 8-byte bytearray object with detailed information about the
        card. See explanation in Table 15 of the MF0ULx1 datasheet for more details.
        Try example 40_mifare_ultralight_ev1_version.py
        """
        send_buf = bytearray([GET_VERSION])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) != 10:
            raise Exception(f"version_get - wrong response length {len(recv_buf)}")
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
    
    def block_read(self, block_adr: int) -> bytearray:
        """
        Read 16 bytes of data (4 blocks).
        """
        if block_adr >= BLOCK_COUNT:
            raise Exception(f"block_read({block_adr}) - block_adr over limit {BLOCK_COUNT-1}")
            
        send_buf = bytearray([READ, block_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        if len(recv_buf) != 18:
            raise Exception(f"block_read - wrong response length {len(recv_buf)}")
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
    
    def block_read_fast(self, begin_adr: int, end_adr: int) -> bytearray:
        """
        Read multiple blocks of memory. You can read up to 15 blocks = 60 bytes.
        """
        send_buf = bytearray([FAST_READ, begin_adr, end_adr])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
        
    def block_write(self, block_adr: int, data: bytes|bytearray) -> None:
        """
        Write 4 bytes of data (1 block).
        """
#         if block_adr >= BLOCK_COUNT:
#             raise Exception(f"block_write({block_adr}, {data}) - block_adr over limit {BLOCK_COUNT-1}")
        
        if len(data) != BLOCK_LENGTH:
            raise Exception(f"block_write({block_adr}, {data}) - wrong data length {len(data)}, should be {BLOCK_LENGTH}")
        
        send_buf = bytearray([WRITE, block_adr]) + data
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) != 1:
            raise Exception(f"block_write - wrong response length {len(recv_buf)}")
        self.validate_ack(recv_buf)
    
    def counter_read(self, num: int) -> int:
        """
        Read value of the counter 0, 1 or 2.
        """
        send_buf = bytearray([READ_CNT, num])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        elif len(recv_buf) == 5:
            self.pcd.crc_verify(recv_buf)
            value = recv_buf[2]  << 16 | recv_buf[1] << 8 | recv_buf[0]
            return value
        else:
            raise Exception(f"counter_read - wrong response length {len(recv_buf)}")
        
    def counter_increment(self, num: int, value: int) -> None:
        """
        Increment selected counter by the given value. Important - counters are one way and can't be cleared.
        """
        if value > 0xFFFFFF:
            raise Exception(f"counter_increment - value {value} over range")
        
        send_buf = bytearray(6)
        send_buf[0] = INCR_CNT
        send_buf[1] = num
        send_buf[2] = value & 0xFF
        send_buf[3] = (value >> 8) & 0xFF
        send_buf[4] = (value >> 16) & 0xFF
        send_buf[5] = 0x00 # dummy byte
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        self.validate_ack(recv_buf)
        
    def signature_read(self) -> bytearray:
        """
        This function returns an IC-specific, 32-byte ECC signature, to verify NXP Semiconductors as the silicon vendor
        """
        send_buf = bytearray([READ_SIG, 0x00])
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        elif len(recv_buf) == 34:
            self.pcd.crc_verify(recv_buf)
            return recv_buf[0:-2]
        else:
            raise Exception(f"signature_read - wrong response length {len(recv_buf)}")
        
    def authenticate(self, key: bytes|bytearray) -> bytearray:
        """
        Perfrom an authentication with 4-byte password. After successful authentication, the card responds with
        2-byte PACK (password acknowledge) which is stored in EEPROM memory of the card and can be changed with
        `write` command. Default password is b"\xFF\xFF\xFF\xFF" and default PACK is b"\x00\x00".
        """
        if len(key) != 4:
            raise Exception(f"authenticate - wrong key length {len(key)}, must be 4")
        
        send_buf = bytearray([PWD_AUTH]) + key
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        elif len(recv_buf) == 4:
            self.pcd.crc_verify(recv_buf)
            return recv_buf[0:-2]
        else:
            raise Exception(f"authenticate - wrong response length {len(recv_buf)}")
        
    def uid_change(self, new_uid: bytes|bytearray) -> None:
        """

        """
        if len(new_uid) != 7:
            raise Exception(f"change_uid - wrong length {len(new_uid)}, must be 7")
        
        # Step 1
        buf = bytearray(4)
        buf[0] = new_uid[0]
        buf[1] = new_uid[1]
        buf[2] = new_uid[2]
        buf[3] = 0x88 ^ new_uid[0] ^ new_uid[1] ^ new_uid[2]
        self.block_write(0, buf)
        
        # Step 2
        print(f"len(buf) = {len(buf)}")
        buf[0] = new_uid[3]
        buf[1] = new_uid[4]
        buf[2] = new_uid[5]
        buf[3] = new_uid[6]
        self.block_write(1, buf)
        
        # Step 3
        buf = self.block_read(2)[0:4]
        debug("Buffer after step 3", buf)
        
        # Step 4
        buf[0] = new_uid[3] ^ new_uid[4] ^ new_uid[5] ^ new_uid[6]
        self.block_write(2, buf)
        
        
    def dump(self) -> None:
        """
        Read the whole memory and print it in HEX and ASCII format.
        """
        
        block_info = {
            0:  "UID[0:2], BCC[0]",
            1:  "UID[3:6]",
            2:  "BCC[1], INT, LOCK[0:1]",
            3:  "OTP[0:3]",
            16: "MOD, RFUI, RFUI, AUTH[0]",
            17: "ACCESS, VCTID, RFUI, RFUI",
            18: "PWD",
            19: "PACK[0:1], RFUI, RFUI",
        }
        
        def print_block(block_adr: int, data: bytearray) -> None:
            print(f"{block_adr:5} | ", end="")
            
            for byte in data:
                print(f"{byte:02X} ", end="")
                
            print("| ", end="")
            
            for byte in data:
                if byte >= 32 and byte <= 126:
                    print(chr(byte), end="")
                else:
                    print(" ", end="")
            
            print("  | ", end="")
            print(block_info.get(block_adr, "User data"))
        
        print("Block | Data        | ASCII | Comment")
        
        for block_adr in range(BLOCK_COUNT):
            if block_adr%4 == 0:
                data = self.block_read(block_adr)
                
            a = (block_adr % 4) * 4
            b = a+4
            print_block(block_adr, data[a:b])
            
        data = mif.counter_read(0)
        print(f"Counter 0: {data}")
        data = mif.counter_read(1)
        print(f"Counter 1: {data}")
        data = mif.counter_read(2)
        print(f"Counter 2: {data}")
                
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
    mif = MifareUltralightEV1(pcd)
    
    iso.scan_and_select()
    
    # dump
#     debug_disable()
#     mif.dump()

#     mif.version_get()

#     # Counters
#     print("Counter demo")
#     data = mif.counter_read(0)
#     print(f"Counter0: {data}")
#     data = mif.counter_read(1)
#     print(f"Counter1: {data}")
#     data = mif.counter_read(2)
#     print(f"Counter2: {data}")
    
    # ECC Signature
#     data = mif.signature_read()
#     debug("Signature", data)

    print("Authentication")
#     data = mif.authenticate(b"\xFF\xFF\xFF\xFF")
#     data = mif.authenticate(b"\x00\x11\x22\x33")
    
    print("Change UID")
    mif.uid_change(b"\x12\x34\x56\x78\x9A\xBC\xDE")
    