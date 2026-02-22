from rfid.log import *

# ISO/IEC 14443-3 basic commands
REQA_7bit        = const(0x26) # Request Command Type A, Set PICC from idle state to ready state
WUPA_7bit        = const(0x52) # Wake-Up Command Type A, Set PICC from idle or halt state to ready state
HLTA             = const(0x50) # Set PICC to halt state
RATS             = const(0xE0) # Request for Answer To Select
SEL_CL1          = const(0x93) # First iteration of anticollision loop
SEL_CL2          = const(0x95) # Second iteration of anticollision loop
SEL_CL3          = const(0x97) # Third iteration of anticollision loop
NVB_20           = const(0x20) # Number of valid bits, byte count = 2
NVB_70           = const(0x70) # Number of valid bits, byte count = 7

CASCADE_TAG      = const(0x88) # Indicates that some more UID bytes remain to be read

class ISO_IEC_14443_3():
    
    def __init__(self, pcd):
        self.pcd = pcd
        
    def bcc_verify(self, buffer: bytes|bytearray) -> None:
        """
        Verify BCC byte of the respinse after sending CL command. This byte shoudl be equal to XOR of byte[0...3].
        This function rises an exception in case of BCC is nor correct.
        """
        if buffer[0] ^ buffer[1] ^ buffer[2] ^ buffer[3] != buffer[4]:
            raise Exception("BCC incorrect")    
    
    def wupa(self):
        """
        Send WUPA (Wake Up Type A) to PICC that is in idle or power-on state.
        PICC responds with ATQA data. This function may raise timeout exception.
        """
        return self.pcd.transmit_7bit(WUPA_7bit)
    
    def reqa(self):
        """
        Send REQA (REQuest Type A) to PICC that is in power-on state.
        PICC responds with ATQA data. This function may raise timeout exception.
        """
        return self.pcd.transmit_7bit(REQA_7bit)
            
    def hlta(self):
        """
        Send HLTA (halt) command to deselect the PICC. This command does not return any value so we don't know if it has been
        received correctly.
        """
        cmd = bytearray([HLTA, 0x00])
        self.pcd.crc_calculate_and_append(cmd)
        try:
            self.pcd.transmit(cmd)
        except:
            pass
        
    def scan_and_select(self):
        """
        This function resets the antenna field and then performs anticollision procedure. If a card is found the function
        returns (uid, atqa, sak) that were read from the card. This function supports only singla card in RF field. In case
        more cards are in the field this function will fail.
        """
        # The UID, ATQO and SAK that will be returned if operation is successful
        uid  = bytearray()
        atqa = 0
        sak  = 0
        
        self.pcd.antenna_disable()
        self.pcd.antenna_enable()
        self.pcd.crypto1_stop()
        
        wupa_ans = self.wupa()
        atqa = wupa_ans[0] << 8 | wupa_ans[1]
            
        for loop in range(3):
            debug(f"Anticollision loop", loop+1)
            
            # This operation should return 5 bytes: [uid0, uid1, uid2, uid3, BCC] or [CT, uid0, uid1, uid2, BCC]
            # where CT is cascade tag and BCC is a check byte calculated as a XOR of first 4 bytes
            cmd1 = bytearray([SEL_CL1 + 2*loop, NVB_20])
            ans1 = self.pcd.transmit(cmd1)
            
            # Verification of BCC
            self.bcc_verify(ans1)
            
            # Select PICC with UID that was received in the step above. This operation should return 3 bytes: [SAK, CRC_L, CRC_H]
            cmd2 = bytearray([SEL_CL1 + 2*loop, NVB_70, ans1[0], ans1[1], ans1[2], ans1[3], ans1[4]])
            self.pcd.crc_calculate_and_append(cmd2)
            ans2 = self.pcd.transmit(cmd2)
            self.pcd.crc_verify(ans2)

            # Store SAK
            sak = ans2[0]
        
            # If first byte of the response is Cascade Tag then we need another loop. Otherwise the process is done.
            if ans1[0] == CASCADE_TAG:
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
            else:
                uid.append(ans1[0])
                uid.append(ans1[1])
                uid.append(ans1[2])
                uid.append(ans1[3])
                return uid, atqa, sak
            
    def select(self, uid: bytes|bytearray) -> None:
        """
        This function resets RF field and then selects a card with UID given. In case there's no card with this UID this
        function rises an exception.
        """
        self.pcd.antenna_disable()
        self.pcd.antenna_enable()
        self.pcd.crypto1_stop()
        self.wupa()
        
        if len(uid) == 4:
            bcc = uid[0] ^ uid[1] ^ uid[2] ^ uid[3]
            cmd = bytearray([SEL_CL1, NVB_70, uid[0], uid[1], uid[2], uid[3], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)

        elif len(uid) == 7:
            bcc = CASCADE_TAG ^ uid[0] ^ uid[1] ^ uid[2]
            cmd = bytearray([SEL_CL1, NVB_70, CASCADE_TAG, uid[0], uid[1], uid[2], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)
            
            bcc = uid[3] ^ uid[4] ^ uid[5] ^ uid[6]
            cmd = bytearray([SEL_CL2, NVB_70, uid[3], uid[4], uid[5], uid[6], bcc])
            self.pcd.crc_calculate_and_append(cmd)
            ans = self.pcd.transmit(cmd)
            self.pcd.crc_verify(ans)

        else:
            raise Exception(f"UID length {len(uid)} is not supported")
    
    def test_all_7bit_commands(self):
        """
        Loop through all 128 7-bit commands. Before sending each command, the antenna is turned off and on to reset the card.
        If the card responds to any commands, the response is printed to the console. The card should respond only to 0x26
        (REQA) and 0x52 (WUPA) commands. If it responds to anything else it might be a backdoor command.
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
