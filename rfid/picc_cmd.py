# Commands for prximity card (PICC)

# ISO/IEC 14443-3 basic commands
REQA_7bit        = const(0x26) # Request Command Type A, Set PICC from idle state to ready state
WUPA_7bit        = const(0x52) # Wake-Up Command Type A, Set PICC from idle or halt state to ready state
BACKDOOR_40_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
BACKDOOR_4F_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
HLTA             = const(0x50) # Set PICC to halt state
RATS             = const(0xE0) # Request for Answer To Select

SEL_CL1          = const(0x93) # First iteration of anticollision loop
SEL_CL2          = const(0x95) # Second iteration of anticollision loop
SEL_CL3          = const(0x97) # Third iteration of anticollision loop
NVB_20           = const(0x20) # Number of valid bits, byte count = 2
NVB_70           = const(0x70) # Number of valid bits, byte count = 7