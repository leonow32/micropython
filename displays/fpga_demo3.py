from machine import UART

uart = UART(1, baudrate=115200, tx=16, rx=17)

uart.write(bytearray([0x1B]))
uart.write(bytearray([0xF0]))
uart.write("================================================================================")
uart.write("                             Test terminala UART-VGA                            ")
uart.write("================================================================================")

# New line
uart.write(bytearray([0x0D]))

# White foreground, black backround
uart.write(bytearray([0b11110000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Red foreground, black backround
uart.write(bytearray([0b11000000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Yellow foreground, black background
uart.write(bytearray([0b11100000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Green foreground, black background
uart.write(bytearray([0b10100000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Cyan foreground, black background
uart.write(bytearray([0b10110000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Blue foreground, black background
uart.write(bytearray([0b10010000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Magenta foreground, black background
uart.write(bytearray([0b11010000]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# New line
uart.write(bytearray([0x0D]))

# Black foreground, white backround
uart.write(bytearray([0b10000111]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, res backround
uart.write(bytearray([0b10000100]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, yellow background
uart.write(bytearray([0b10000110]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, green background
uart.write(bytearray([0b10000010]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, cyan background
uart.write(bytearray([0b10000011]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, blue background
uart.write(bytearray([0b10000001]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Black foreground, magenta background
uart.write(bytearray([0b10000101]))
uart.write("ABCDEFGHIJKLMNOPQRTSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()-=<>")

# Icons
uart.write(bytearray([0x0D]))
uart.write(bytearray([0xF0]))

for char in range(0, 0x7F):
    if char == 0x0D: # New line
        continue
    if char == 0x1B: # Home cursor
        continue;
    uart.write(bytearray([char]))