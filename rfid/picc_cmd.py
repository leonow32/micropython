# Commands for prximity card (PICC)

# ISO/IEC 14443-3 basic commands
REQA_7bit        = const(0x26) # Request Command Type A, Set PICC from idle state to ready state
WUPA_7bit        = const(0x52) # Wake-Up Command Type A, Set PICC from idle or halt state to ready state
HLTA             = const(0x50) # Set PICC to halt state
RATS             = const(0xE0) # Request for Answer To Select
BACKDOOR_40_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
BACKDOOR_4F_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
GOD_MODE_7bit    = const(0x43) # Access restricted blocks with any password

SEL_CL1          = const(0x93) # First iteration of anticollision loop
SEL_CL2          = const(0x95) # Second iteration of anticollision loop
SEL_CL3          = const(0x97) # Third iteration of anticollision loop
NVB_20           = const(0x20) # Number of valid bits, byte count = 2
NVB_70           = const(0x70) # Number of valid bits, byte count = 7
CASCADE_TAG      = const(0x88) # Indicates that some more UID bytes remain to be read

AUTH_KEY_A       = const(0x60) # Perform sector authentication with key A
AUTH_KEY_B       = const(0x61) # Perform sector authentication with key A
MIFARE_READ      = const(0x30)
MIFARE_WRITE     = const(0xA0)
MIFARE_DECREMENT = const(0xC0)
MIFARE_INCREMENT = const(0xC1)
MIFARE_RESTORE   = const(0xC2)
MIFARE_TRANSFER  = const(0xB0)

