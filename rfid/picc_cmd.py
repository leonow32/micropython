# Commands for proximity card (PICC)

BACKDOOR_40_7bit = const(0x40) # Unlocks some Chinese MIFARE Classic cards
BACKDOOR_4F_7bit = const(0x4F) # Unlocks some Chinese MIFARE Classic cards
GOD_MODE         = const(0x43) # Access restricted blocks with any password

AUTH_KEY_A       = const(0x60) # Perform sector authentication with key A
AUTH_KEY_B       = const(0x61) # Perform sector authentication with key B
MIFARE_READ      = const(0x30) # Read 16-byte block (must be authenticated)
MIFARE_WRITE     = const(0xA0) # Write 16-byte block (must be authenticated)
MIFARE_DECREMENT = const(0xC0) # Decrement value of the block (must be authenticated)
MIFARE_INCREMENT = const(0xC1) # Increment value of the block (must be authenticated)
MIFARE_RESTORE   = const(0xC2) # Copy value from the block to transfer buffer (must be authenticated)
MIFARE_TRANSFER  = const(0xB0) # Copy value from transfer buffer to the block (must be authenticated)
