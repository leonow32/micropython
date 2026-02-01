# Commands for prximity card (PICC)

# ISO/IEC 14443-3 basic commands
REQA_7bit = const(0x26) # Request Command Type A, Set PICC from idle state to ready state
WUPA_7bit = const(0x52) # Wake-Up Command Type A, Set PICC from idle or halt state to ready state
HLTA      = const(0x50) # Set PICC to halt state
RATS      = const(0xE0) # Request for Answer To Select
