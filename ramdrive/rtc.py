import machine
BLOCKSIZE = 32


#rtc = machine.RTC().memory()

# Testowa tablica bajtow
#rtc = bytes()
rtc = bytearray()
for i in range(0,256):
    rtc += bytes([i])

print("len={} type={}".format(len(rtc), type(rtc)))
print(rtc)
print("====")
machine.RTC().memory(rtc)

x = bytearray(machine.RTC().memory())
print("len={} type={}".format(len(x), type(x)))
print(x)

"""

BytesToAdd = BLOCKSIZE - len(rtc)
print("BytesToAdd={}".format(BytesToAdd))

Buffer = bytes()
Buffer = rtc + bytes([0x00] * BytesToAdd)

print(Buffer)
print(len(Buffer))
"""