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
        if len(recv_buf) != 18:
            raise Exception(f"block_read - wrong response length {len(recv_buf)}")
        self.pcd.crc_verify(recv_buf)
        return recv_buf[:-2]
        
    def block_write(self, block_adr: int, data: bytes|bytearray) -> None:
        """
        Write 4 bytes of data (1 block).
        """
        if block_adr >= BLOCK_COUNT:
            raise Exception(f"block_write({block_adr}, {data}) - block_adr over limit {BLOCK_COUNT-1}")
        
        if len(data) != BLOCK_LENGTH:
            raise Exception(f"block_write({block_adr}, {data}) - wrong data length {len(data)}, should be {BLOCK_LENGTH}")
        
        send_buf = bytearray([WRITE, block_adr]) + data
        self.pcd.crc_calculate_and_append(send_buf)
        recv_buf = self.pcd.transmit(send_buf)
        if len(recv_buf) != 1:
            raise Exception(f"block_write - wrong response length {len(recv_buf)}")
        self.validate_ack(recv_buf)
                
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

    mif.version_get()
    