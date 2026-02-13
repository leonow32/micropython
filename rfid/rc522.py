from machine import Pin, SPI
import time
import rfid.reg as reg
import rfid.pcd_cmd as pcd_cmd
import rfid.picc_cmd as picc_cmd

class RC522:
    
    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs  = cs
        self.rst = rst

        self.debug = False
        self.timeout_ms = 100
        
        self.cs.init(mode=Pin.OUT, value=1)
        self.rst.init(mode=Pin.OUT, value=0)
        time.sleep_ms(50)
        self.rst(1)

        self.reg_write(reg.TxASKReg,      0b01000000) # Force a 100 % ASK modulation
        self.reg_write(reg.ModeReg,       0b00100001) # Set the initial value for the CRC coprocessor to 0x6363
            
    def reg_read(self, register: int) -> None:
        """
        Read single register. Register name should come from reg.py file.
        """
        temp = bytearray([0x80 | register, 0x00])
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1]
    
    def reg_reads(self, register: int, length: int) -> bytearray:
        temp = bytearray([0x80 | register] * (length + 1))
        self.cs(0)
        self.spi.write_readinto(temp, temp)
        self.cs(1)
        return temp[1:]
        
    def reg_write(self, register: int, value: int|bytes|bytearray) -> None:
        """
        Write a value or buffer of values into a register. Register name should come from reg.py file.
        """
        self.cs(0)
        
        if isinstance(value, int):
            self.spi.write(bytes([register, value]))
        else:
            self.spi.write(bytes([register]))
            self.spi.write(value)
            
        self.cs(1)
            
    def reg_set_bit(self, register: int, mask: int) -> None:
        """

        """
        temp = self.reg_read(register)
        temp |= mask
        self.reg_write(register, temp)
        
    def reg_clr_bit(self, register: int, mask: int) -> None:
        """
        
        """
        temp = self.reg_read(register)
        temp = (temp & ~mask) & 0xFF
        self.reg_write(register, temp)
                
    def reset(self) -> None:
        self.reg_write(reg.CommandReg, pcd_cmd.SoftReset)

        timeout_counter = 0
        while self.reg_read(reg.CommandReg) & 0b00010000:
            timeout_counter += 1
            if(timeout_counter == 10):
                raise Exception(0, "No response after reset")
            time.sleep_ms(10)
            
#     def dump(self) -> None:
#         """
#         Read all the registers of RC522 and print them to the console.
#         """
#         registers = bytearray(64)
#         self.regs_read(0x00, registers)
#         
#         print("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F", end="")
#         
#         for i in range(len(registers)):
#             if i%16 == 0:
#                 print(f"\n{i:02X}: ", end="")
#             print(f"{registers[i]:02X} ", end="")
#         
#         print()
        
    def version_get(self) -> None:
        return self.reg_read(reg.VersionReg)
    
    def antenna_enable(self) -> None:
        self.reg_set_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def antenna_disable(self) -> None:
        self.reg_clr_bit(reg.TxControlReg, 0x03)
        time.sleep_ms(5)
        
    def gain_set(self, value: int) -> None:
        if value < 0: value = 0
        if value > 7: value = 7
        temp = self.reg_read(reg.RFCfgReg)
        temp = temp & 0b10001111
        temp = temp | (value << 4)
        self.reg_write(reg.RFCfgReg, temp)
        pass
    
    def gain_get(self) -> int:
        value = self.reg_read(reg.RFCfgReg)
        value = (value >> 4) & 0b111
        return value
        
    def crypto1_stop(self) -> None:
        """
        This command resets Crypto1 engine. Use it to terminate communication with authenticated PICC.
        """
        self.reg_clr_bit(reg.Status2Reg, 0b00001000)
        
    def wait_for_rx_irq(self) -> None:
        for i in range(self.timeout_ms // 10):
            if self.reg_read(reg.ComIrqReg) & 0b00110000:  # transmisja 0b00100000
                return
            else:
                time.sleep_ms(10)
        
        raise Exception(0, "Timeout")     
    
    def crc_coprocessor(self, data: bytes|bytearray) -> int:
        self.reg_write(reg.FIFOLevelReg, 0x80);          # Clear all the data in FIFO buffer
        self.reg_write(reg.CommandReg, pcd_cmd.CalcCRC)  # Enable CRC coprocessor
        self.reg_write(reg.FIFODataReg, data)            # Transmit the data to FIFO buffer
        crc_h  = self.reg_read(reg.CRCResultRegH)
        crc_l  = self.reg_read(reg.CRCResultRegL)
        result = crc_h << 8 | crc_l
        return result    
    
    def crc_calculate_and_append(self, buffer: bytearray) -> None:
        """
        Calculates the CRC from given buffer and appends the result to the end of the buffer, so it can be transmitted to
        the PICC in the following line.
        """
        crc = self.crc_coprocessor(buffer)
        buffer.append(crc & 0xFF) # CRC_L
        buffer.append(crc >> 8)   # CRC_H
        
    def crc_verify(self, buffer: bytes|bytearray) -> bool:
        """
        The function checks the buffer returned by PICC, which contains some data and the CRC at the end of the buffer.
        The function calculates the CRC from the received data and checks whether it matches the received CRC.
        """
        crc_calculated = self.crc_coprocessor(buffer[0:-2])
        crc_received   = buffer[-1] << 8 | buffer[-2]
        return crc_calculated == crc_received
        
    def transmit(self, buffer: bytearray) -> bytearray:
        self.debug_print("Send", buffer)
        self.reg_write(reg.CommandReg, pcd_cmd.Idle)        # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, buffer)             # Copy the buffer to FIFO buffer in RC522
        self.reg_write(reg.BitFramingReg, 0)                # Set transfer length to 8 bits
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive)  # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        self.wait_for_rx_irq()                              # Wait for receive interrupt flag
        
        lenght = self.reg_read(reg.FIFOLevelReg)            # Check how many bytes are received            
        response_buf = self.reg_reads(reg.FIFODataReg, lenght)
        
        self.debug_print("Recv", response_buf)
        return response_buf
        
    def transmit_7bit(self, command_7bit: int) -> bytearray:
        self.debug_print("Send[s]", command_7bit)
        self.reg_write(reg.CommandReg, pcd_cmd.Idle)        # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, command_7bit)       # Store data to FIFO buffer
        self.reg_write(reg.BitFramingReg, 7)                # Set transfer length to 7 bits instead of 8
        self.reg_write(reg.CommandReg, pcd_cmd.Transceive)  # Enter new command
        self.reg_set_bit(reg.BitFramingReg, 0x80)           # Start data transfer, bit StartSend=1
        self.wait_for_rx_irq()                              # Wait for receive interrupt flag
        
        lenght = self.reg_read(reg.FIFOLevelReg)            # Check how many bytes are received
        response_buf = self.reg_reads(reg.FIFODataReg, lenght)
        
        self.debug_print("Recv", response_buf)
        return response_buf
    
    def picc_send_wupa(self):
        """
        Senf WUPA (Wake Up Type A) to PICC that is in idle or power-on state.
        PICC responds with ATQA data. This function may raise timeout exception.
        """
        return self.transmit_7bit(picc_cmd.WUPA_7bit)
    
    def picc_send_reqa(self):
        """

        """
        return self.transmit_7bit(picc_cmd.REQA_7bit)
        
    def picc_scan_and_select(self) -> bytearray|None:
        
        # The UID that will be returned if operation is successful
        uid = bytearray()
        
        self.crypto1_stop()
        
        # Try to send WUPA twice
        try:
            self.picc_send_wupa()
        except:
            try:
                self.picc_send_wupa()
            except:
                print("Error when sending WUPA")
                return None
            
        for loop in range(3):
            print(f"Anticollision loop {loop+1}")
            
            # This operation should return 5 bytes: [uid0, uid1, uid2, uid3, BCC] or [CT, uid0, uid1, uid2, BCC]
            # where CT is cascade tag and BCC is a check byte calculated as a XOR of first 4 bytes
            cmd1 = bytearray([picc_cmd.SEL_CL1 + 2*loop, picc_cmd.NVB_20])
            ans1 = self.transmit(cmd1)
        
            # Verification of BCC
            if ans1[0] ^ ans1[1] ^ ans1[2] ^ ans1[3] != ans1[4]:
                print("BCC incorrect")
                return
            else:
                print("BCC correct")
            
            # Select PICC with UID that was received in the step above
            # This operation should return 3 bytes: [SAK, CRC_L, CRC_H]
            cmd2 = bytearray([picc_cmd.SEL_CL1 + 2*loop, picc_cmd.NVB_70, ans1[0], ans1[1], ans1[2], ans1[3], ans1[4]])
            self.crc_calculate_and_append(cmd2)
            ans2 = self.transmit(cmd2)
        
            # Verification of CRC
            if not self.crc_verify(ans2):
                print("Received wrong CRC")
                return None
        
            print(f"SAK: {ans2[0]:02X}")
        
            # If first byte of the response is Cascade Tag then we need another loop
            if ans1[0] == picc_cmd.CASCADE_TAG:
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
            else:
                uid.append(ans1[0])
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
                return uid
            
    def picc_select(self, uid: bytes|bytearray):
        if len(uid) == 4:
            bcc = uid[0] ^ uid[1] ^ uid[2] ^ uid[3]
            cmd = bytearray([picc_cmd.SEL_CL1, picc_cmd.NVB_70, uid[0], uid[1], uid[2], uid[3], bcc])
            self.crc_calculate_and_append(cmd)
            ans = self.transmit(cmd)
            if not self.crc_verify(ans):
                print("Received wrong CRC")
                return False
            else:
                return True 
        elif len(uid) == 7:
            bcc = picc_cmd.CASCADE_TAG ^ uid[0] ^ uid[1] ^ uid[2]
            cmd = bytearray([picc_cmd.SEL_CL1, picc_cmd.NVB_70, picc_cmd.CASCADE_TAG, uid[0], uid[1], uid[2], bcc])
            self.crc_calculate_and_append(cmd)
            ans = self.transmit(cmd)
            if not self.crc_verify(ans):
                print("Received wrong CRC")
                return False
            
            bcc = uid[3] ^ uid[4] ^ uid[5] ^ uid[6]
            cmd = bytearray([picc_cmd.SEL_CL2, picc_cmd.NVB_70, uid[3], uid[4], uid[5], uid[6], bcc])
            self.crc_calculate_and_append(cmd)
            ans = self.transmit(cmd)
            if not self.crc_verify(ans):
                print("Received wrong CRC")
                return False
            else:
                return True
            
        else:
            print(f"UID length {len(uid)} is not supported")
    
    def picc_test_all_7bit_commands(self):
        """
        Loop through all 128 7-bit commands. Before sending each command, the antenna is
        turned off and on to reset the PICC. If the card responds to any comments, the
        response is printed to the console.
        """
        for i in range(128):
            try:
                self.antenna_disable()
                self.antenna_enable()
                response = self.transmit_7bit(i)
                print(f"cmd {i:02X}: response[{len(response)}] ", end="")
                for byte in response:
                    print(f"{byte:02X} ", end="")
                print("")
            except:
                pass
            
    ###################
    # MIFARE Commands #
    ###################
    
    def mifare_validate_ack(self, recv_buf):
        if recv_buf[0] == 0x0A:
            return
        elif recv_buf[0] == 0x00:
            raise Exception("buffer valid, operation invalid")
        elif recv_buf[0] == 0x01:
            raise Exception("buffer valid, parity or CRC error")
        elif recv_buf[0] == 0x04:
            raise Exception("buffer invalid, operation invalid")
        elif recv_buf[0] == 0x04:
            raise Exception("buffer invalid, parity or CRC error")
        else:
            raise Exception(f"unsupported ack response {recv_buf[0]}")
    
    def mifare_auth(self, auth_cmd, block_adr, key, uid):        
        buffer = bytes([auth_cmd, block_adr]) + key + uid
        
#         print("Authentication cmd: ")
#         for byte in buffer:
#             print(f"{byte:02X} ", end="")
#         print()
        
#         self.crypto1_stop()
        self.reg_write(reg.CommandReg, pcd_cmd.Idle)        # Stop any ongoing command and set RC522 to idle state
        self.reg_write(reg.ComIrqReg, 0x7F)                 # Clear interrupt flags
        self.reg_write(reg.FIFOLevelReg, 0x80)              # Clear FIFO buffer
        self.reg_write(reg.FIFODataReg, buffer)             # Store data to FIFO buffer
        self.reg_write(reg.CommandReg, pcd_cmd.MFAuthent)   # Enter new command
        self.wait_for_rx_irq()
        
        if self.reg_read(reg.Status2Reg) & 0b00001000:      # Check bit MFCrypto1On
            return True
        else:
            return False
        
    def mifare_read(self, block_adr):
        send_buf = bytearray([picc_cmd.MIFARE_READ, block_adr])
        self.crc_calculate_and_append(send_buf)
        recv_buf = self.transmit(send_buf)
        if not self.crc_verify(recv_buf):
            print("Wrong CRC")
        
        return recv_buf[:-2]
        
    def mifare_write(self, block_adr, data):
        # First step
        send_buf = bytearray([picc_cmd.MIFARE_WRITE, block_adr])
        self.crc_calculate_and_append(send_buf)
        recv_buf = self.transmit(send_buf)
        self.mifare_validate_ack(recv_buf)
        
        # Second step
        send_buf = bytearray(data)
        self.crc_calculate_and_append(send_buf)
        recv_buf = self.transmit(send_buf)
        self.mifare_validate_ack(recv_buf)
        
    def mifare_1k_dump(self, key, uid, keys=None):
        
        # If key list is not provided then use default keys for each sector
        if keys == None:
            keys = [
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 0
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 1
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 2
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 3
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 4
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 5
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 6
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 7
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 8
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 9
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 10
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 11
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 12
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 13
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF"),   # Sector 14
                (picc_cmd.AUTH_KEY_A, b"\xFF\xFF\xFF\xFF\xFF\xFF")    # Sector 15
            ]

        print("| Sector | Block |                       Data                      |       ASCII      |")
        print("|        |       |  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F |                  |")
        for block_adr in range(0, 64):
            
            # At the beginning of every block me must perfor authentication
            if block_adr % 4 == 0:
                res = reader.mifare_auth(keys[block_adr//4][0], block_adr, keys[block_adr//4][1], uid)
                if res == False:
                    print("Can't authenticate block {block_adr}")
                    continue
            
            # Read the block
            data = self.mifare_read(block_adr)
            
            # Print the result
            if block_adr % 4 == 0:
                print(f"| {block_adr//4:6} ", end="")
            else:
                print("|        ", end="")
                
            print(f"| {block_adr:5} | ", end="")
            
            for byte in data:
                print(f"{byte:02X} ", end="")
            
            print("| ", end="")
            
            for byte in data:
                if byte >= 32 and byte <= 126:
                    print(chr(byte), end="")
                else:
                    print(" ", end="")
            
            print(" |")
            
            
    
    def debug_print(self, caption:str, data: bytes) -> None:
        if self.debug:
            if isinstance(data, int):
                print(f"{caption}: {data:02X}")
                
            elif isinstance(data, bytearray) or isinstance(data, bytes):           
                print(f"{caption}[{len(data)}]: ", end="")
                for byte in data:
                    print(f"{byte:02X} ", end="")
                print()
                
            else:
                print(f"{caption}")
        
if __name__ == "__main__":
    import mem_used
    import measure_time
    spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    rst = Pin(7)

    reader = RC522(spi, cs, rst)
    reader.debug = True

#     ver = reader.version_get()
#     print(f"VERSION: {ver:02X}")

#     reader.dump()
    
    reader.antenna_enable()
    reader.gain_set(7)
    uid = reader.picc_scan_and_select()
    
    print("UID: ", end="")
    if isinstance(uid, bytearray):
        for byte in uid:
            print(f"{byte:02X} ", end="")
        print()
    else:
        print(uid)
        
    key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
#     res = reader.mifare_auth(picc_cmd.AUTH_KEY_A, 0, key, uid)
#     print(f"Authentication result: {res}")
    
    
    
#     print("Read block 0")
#     for i in range(4):
#         data = reader.mifare_read(i)
#         reader.debug_print(f"Block {i}", data)

    reader.debug = False
    reader.mifare_1k_dump(key, uid)

    mem_used.print_ram_used()
