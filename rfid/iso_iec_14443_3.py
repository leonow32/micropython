import rfid.picc_cmd as picc_cmd
from rfid.log import *

class ISO_IEC_14443_3():
    
    def __init__(self, pcd):
        self.pcd = pcd
        
    def bcc_verify(self, buffer: bytes|bytearray) -> None:
        if buffer[0] ^ buffer[1] ^ buffer[2] ^ buffer[3] != buffer[4]:
            raise Exception("BCC incorrect")    
    
    def picc_send_wupa(self):
        """
        Send WUPA (Wake Up Type A) to PICC that is in idle or power-on state.
        PICC responds with ATQA data. This function may raise timeout exception.
        """
        return self.pcd.transmit_7bit(picc_cmd.WUPA_7bit)
    
    def picc_send_reqa(self):
        """

        """
        return self.pcd.transmit_7bit(picc_cmd.REQA_7bit)
            
    def picc_send_hlta(self):
        """
        Send HLTA (halt) command to deselect the PICC. This command does not return any value so we don't know if it has been
        received correctly.
        """
        cmd = bytearray([picc_cmd.HLTA, 0x00])
        self.pcd.crc_calculate_and_append(cmd)
        try:
            self.pcd.transmit(cmd)
        except:
            pass
        
    def picc_scan_and_select(self):
        
        # The UID, ATQO and SAK that will be returned if operation is successful
        uid  = bytearray()
        atqa = 0
        sak  = 0
        
        self.pcd.antenna_disable()
        self.pcd.antenna_enable()
        self.pcd.crypto1_stop()
        
        wupa_ans = self.picc_send_wupa()
        atqa = wupa_ans[0] << 8 | wupa_ans[1]
            
        for loop in range(3):
            debug(f"Anticollision loop", loop+1)
            
            # This operation should return 5 bytes: [uid0, uid1, uid2, uid3, BCC] or [CT, uid0, uid1, uid2, BCC]
            # where CT is cascade tag and BCC is a check byte calculated as a XOR of first 4 bytes
            cmd1 = bytearray([picc_cmd.SEL_CL1 + 2*loop, picc_cmd.NVB_20])
            ans1 = self.pcd.transmit(cmd1)
            
            # Verification of BCC
            self.bcc_verify(ans1)
            
            # Select PICC with UID that was received in the step above. This operation should return 3 bytes: [SAK, CRC_L, CRC_H]
            cmd2 = bytearray([picc_cmd.SEL_CL1 + 2*loop, picc_cmd.NVB_70, ans1[0], ans1[1], ans1[2], ans1[3], ans1[4]])
            self.pcd.crc_calculate_and_append(cmd2)
            ans2 = self.pcd.transmit(cmd2)
            self.pcd.crc_verify(ans2)

            # Store SAK
            sak = ans2[0]
        
            # If first byte of the response is Cascade Tag then we need another loop. Otherwise the process is done.
            if ans1[0] == picc_cmd.CASCADE_TAG:
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
            else:
                uid.append(ans1[0])
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
                return uid, atqa, sak
            
    def picc_select(self, uid: bytes|bytearray) -> None:
        if len(uid) == 4:
            bcc = uid[0] ^ uid[1] ^ uid[2] ^ uid[3]
            cmd = bytearray([picc_cmd.SEL_CL1, picc_cmd.NVB_70, uid[0], uid[1], uid[2], uid[3], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)

        elif len(uid) == 7:
            bcc = picc_cmd.CASCADE_TAG ^ uid[0] ^ uid[1] ^ uid[2]
            cmd = bytearray([picc_cmd.SEL_CL1, picc_cmd.NVB_70, picc_cmd.CASCADE_TAG, uid[0], uid[1], uid[2], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)
            
            bcc = uid[3] ^ uid[4] ^ uid[5] ^ uid[6]
            cmd = bytearray([picc_cmd.SEL_CL2, picc_cmd.NVB_70, uid[3], uid[4], uid[5], uid[6], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)

        else:
            print(f"UID length {len(uid)} is not supported")
    
    def picc_test_all_7bit_commands(self):
        """
        Loop through all 128 7-bit commands. Before sending each command, the antenna is
        turned off and on to reset the PICC. If the card responds to any comments, the
        response is printed to the console.
        """
        debug_enable = False
        for i in range(128):
            try:
                self.pcd.antenna_disable()
                self.pcd.antenna_enable()
                response = self.pcd.transmit_7bit(i)
                
                debug_enable = True
                debug(f"cmd: {i:02X} -> response", response)
                debug_enable = False
            except:
                pass
        debug_enable = True
            
   

if __name__ == "__main__":
    import mem_used
    import measure_time
    from machine import Pin, SPI
    import rfid.rc522
    
    spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs  = Pin(5)
    rst = Pin(7)

    pcd = rfid.rc522.RC522(spi, cs, rst)
    
    iso = ISO_IEC_14443_3(pcd)
    
    try:
        uid, atqa, sak = iso.picc_scan_and_select()
        print("Card found")
        debug("UID", uid)
        print(f"ATQA: {atqa:04X}")
        print(f"SAK:  {sak:02X}")
    except:
        print("No card")
    
    mem_used.print_ram_used()
    