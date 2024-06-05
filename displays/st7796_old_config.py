def init():
    rst(0)
    sleep_ms(15)
    rst(1)
    sleep_ms(15)
    
#     write_cmd(0xF0)             # Command Set Control
#     write_data(0xC3)            # Enable command 2 part I
#     
#     write_cmd(0xF0)             # Command Set Control
#     write_data(0x96)            # Enable command 2 part II
    
    write_cmd(0x3A)             # COLMOD: Pixel Format Set
    write_data(0x05)            # 16-bit pixel format
    
#     write_cmd(0xB0)             # Interface Mode Control
#     write_data(0x80)            # SPI Enable
    
    write_cmd(0xB6)             # Display Function Control
    write_data(0x00)
    write_data(0b11100010);     # ISC[3:0]=2 GS=1 SS=0
    
#     write_cmd(0xB5)             # Blanking Porch Control
#     write_data(0x02)
#     write_data(0x03)
#     write_data(0x00)
#     write_data(0x04)
    
#     write_cmd(0xB1)             # Frame Rate Control (In Normal Mode/Full Colors)
#     write_data(0x80)
#     write_data(0x10)
    
#     write_cmd(0xB4)             # Display Inversion Control
#     write_data(0x00)
    
#     write_cmd(0xB7)             # Entry Mode Set
#     write_data(0xC6)
    
#     write_cmd(0xC5)             # VCom control
#     write_data(0x24)
    
#     write_cmd(0xE4)             # UNDOCUMMENTED
#     write_data(0x31)
    
#     write_cmd(0xE8)             # Display Output
#     write_data(0x40)
#     write_data(0x8A)
#     write_data(0x00)
#     write_data(0x00)
#     write_data(0x29)
#     write_data(0x19)
#     write_data(0xA5)
#     write_data(0x33)
    
#    write_cmd(0xC2)             # Power control 3
    
#     write_cmd(0xA7)             # UNDOCUMMENTED
    
    # Better color quality is without these settings below
#     write_cmd(0xE0)             # Positive Gamma Control
#     write_data(0xF0)
#     write_data(0x09)
#     write_data(0x13)
#     write_data(0x12)
#     write_data(0x12)
#     write_data(0x2B)
#     write_data(0x3C)
#     write_data(0x44)
#     write_data(0x4B)
#     write_data(0x1B)
#     write_data(0x18)
#     write_data(0x17)
#     write_data(0x1D)
#     write_data(0x21)
#      
#     write_cmd(0XE1)             # Negative Gamma Control
#     write_data(0xF0)
#     write_data(0x09)
#     write_data(0x13)
#     write_data(0x0C)
#     write_data(0x0D)
#     write_data(0x27)
#     write_data(0x3B)
#     write_data(0x44)
#     write_data(0x4D)
#     write_data(0x0B)
#     write_data(0x17)
#     write_data(0x17)
#     write_data(0x1D)
#     write_data(0x21)
     
    write_cmd(0x36)             # Memory Access Control
    write_data(0b00101100);     # MY=0 MX=0 MV=1 ML=0 MH=1 BGR=1
        
#     write_cmd(0xF0)             # Command Set Control
#     write_data(0xC3)
#     
#     write_cmd(0xF0)             # Command Set Control
#     write_data(0x69)
    
#     write_cmd(0x13)             # Normal Display Mode ON
    write_cmd(0x11)             # Sleep Out
    write_cmd(0x29)             # Display ON