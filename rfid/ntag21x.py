from rfid.log import *

# Driver for NTAG213, NTAG215 and NTAG216

# Card commands
GET_VERSION = const(0x60)
READ        = const(0x30) # Read 16 bytes = 4 blocks
FAST_READ   = const(0x3A) # Read selected blocks, max 15 blocks in single operation
WRITE       = const(0xA2) # Write 4 bytes = 1 block
READ_CNT    = const(0x39)
#INCR_CNT    = const(0xA5)
PWD_AUTH    = const(0x1B)
READ_SIG    = const(0x3C)
#CHECK_T_EV  = const(0x3E) # Check tearing even
#VCSL        = const(0x4B)

BLOCK_LENGTH = const(4)
   
class NTAG21X():
    
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
        elif recv_buf[0] == 0x05:
            raise Exception("NAK for EEPROM write error")
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
        
    def authenticate(self, password: bytes|bytearray) -> bytearray:
        """
        Perfrom an authentication with 4-byte password. After successful authentication, the card responds with
        2-byte PACK (password acknowledge) which is stored in EEPROM memory of the card and can be changed with
        `write` command. Default password is b"\xFF\xFF\xFF\xFF" and default PACK is b"\x00\x00".
        """
        if len(password) != 4:
            raise Exception(f"authenticate - wrong password length {len(password)}, must be 4")
        
        send_buf = bytearray([PWD_AUTH]) + password
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) == 1:
            self.validate_ack(recv_buf)
        elif len(recv_buf) == 4:
            self.pcd.crc_verify(recv_buf)
            return recv_buf[0:-2]
        else:
            raise Exception(f"authenticate - wrong response length {len(recv_buf)}")
        
    def security_configure(self, password, pack, try_times, address, mode):
        """
        `password` - 4 bytes.
        `pack` - 2 bytes, this is the response of the card after successful authentication with password.
        `try_times` - Number of failed authentications after which authentication will never be possible again. Max 7.
        If set to zero, brute force is possible and the card will not lock after unsuccessful authentication.
        `address` - the page address from which the password verification is required. Valid range is from 0x00 to 0xFF.
        If address is set to a page address which is higher than the last configuration page, the password protection
        is effectively disabled.
        `mode` - 0: write access is protected by the password verification, 1: read and write access is protected.
        """
        if len(password) != 4:
            raise Exception(f"security_configure - wrong password length {len(password)}, must be 4")
        if len(pack) != 2:
            raise Exception(f"security_configure - wrong pack length {len(pack)}, must be 2")
        if try_times > 7:
            raise Exception(f"security_configure - wrong value of try_times {try_times}, must <= 7")
        if mode > 1:
            raise Exception(f"security_configure - wrong value of mode {mode}, must 0 or 1")
        
        version = self.version_get()
        
        if version[6] == 0x0F: # NTAG213
            cfg_address   = 0x29
        elif version[6] == 0x11: # NTAG215
            cfg_address   = 0x83
        elif version[6] == 0x13: # NTAG216
            cfg_address   = 0xE3
        else:
            raise Exception(f"Unknown storage descriptor {version[6]:02X} in version data")
        
        cfg0 = self.block_read_fast(cfg_address, cfg_address)
        
        send_buf = bytearray([cfg0[0], cfg0[1], cfg0[2], address]) # block CFG0: MIRROR, RFUI, MIRROR_PAGE, AUTH0
        self.block_write(cfg_address, send_buf)
        
        send_buf = bytearray([mode << 7 | try_times, 0x05, 0x00, 0x00]) # block CFG1: ACCESS, RFUI, RFUI, RFUI
        self.block_write(cfg_address+1, send_buf)
        
        self.block_write(cfg_address+2, password) # block 18/39: PWD[0:3]
        
        send_buf = pack + bytearray([0x00, 0x00]) # block 19/40: PACK[1:0], RFUI, RFUI
        self.block_write(cfg_address+3, send_buf)
        
    def uid_change(self, new_uid: bytes|bytearray) -> None:
        """
        This command works only with some Chinese clones of MF0UL11 that allow write operations on blocks 0-3.
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
        
        version = self.version_get()
        
        if version[6] == 0x0F: # NTAG213
            block_count   = 45
            config_offset = 40
        elif version[6] == 0x11: # NTAG215
            block_count   = 135
            config_offset = 130
        elif version[6] == 0x13: # NTAG216
            block_count   = 231
            config_offset = 226
        else:
            raise Exception(f"Unknown storage descriptor {version[6]:02X} in version data")
    
        block_info = {
            0:  "UID[0:2], BCC[0]",
            1:  "UID[3:6]",
            2:  "BCC[1], INT, LOCK[0:1]",
            3:  "CC[0:3]",
            config_offset:   "LOCK[2:4], CHK",
            config_offset+1: "MIRROR, RFUI, MIRROR_PAGE, AUTH0", # tu powinny byc 4 bajty
            config_offset+2: "ACCESS, RFUI, RFUI, RFUI",
            config_offset+3: "PWD[0:3]",
            config_offset+4: "PACK[0:1], RFUI, RFUI",
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
        
        for block_adr in range(block_count):
            if block_adr%4 == 0:
                data = self.block_read(block_adr)
                
            a = (block_adr % 4) * 4
            b = a+4
            print_block(block_adr, data[a:b])

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
    mif = NTAG21X(pcd)

    iso.scan_and_select()

    # dump
    debug_disable()
    mif.dump()