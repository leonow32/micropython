from machine import Pin, SPI
# spi = SPI(1, baudrate=10000, polarity=1, phase=1, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# spi = SPI(1, baudrate=27_000_000, polarity=0, phase=0, sck=Pin(0), mosi=Pin(13), miso=Pin(12))
#spi = SPI(2, baudrate=60_000_000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(13), miso=Pin(12))
spi = SPI(2, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))     # Titan Proto ESP32-S3
print(spi)
cs = Pin(15, Pin.OUT)

# Signature
# buf = bytearray(b'\xAB\x01\xFF\x00')
# out = bytearray(4)

# Status register
# buf = bytearray(b'\x05\x00')
# out = bytearray(2)

# Write enable
# buf = bytearray(1)
# buf = b'\x06'
# out = bytearray(1)

# Write data
# buf = bytearray(b'\x02\xAA\xBB\xCC')
# buf = bytearray([0x02, 0x01, 0x02, 0xCD])

# Read data
#buf = bytearray(b'\x03\xAA\xBB\x00')
#buf = bytearray([0x03, 0x0A, 0x0B, 0x00])

# Test sequence
buf = bytearray(b'\x04\x00\x00\x00\x00')
out = buf

cs(0)
spi.write_readinto(buf, out)
cs(1)

# buf = bytearray([0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
# cs(0)
# spi.write_readinto(buf, buf)
# cs(1)

for byte in out:
    print(f"{byte:02X} ", end="")