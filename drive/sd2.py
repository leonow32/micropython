import machine
import uos
import utime

global SD2

def SDmount2():
    global SD2
    #SD2 = machine.SDCard(slot=3)
    #SD2 = machine.SDCard(slot=3, freq=10000000)
    #SD2 = machine.SDCard(slot=3, width=1, cs=13, miso=12, mosi=15, sck=14, freq=20000000)
    
    #SD2 = machine.SDCard(slot=2, width=1, freq=20000000, cs=4)
    #SD2 = machine.SDCard(slot=2, width=1, freq=20000000)
    #SD2 = machine.SDCard(slot=2, width=1, freq=160000000)
    #SD2 = machine.SDCard(slot=2, width=1, freq=20000000, mosi=22)
    #SD2 = machine.SDCard(slot=2, width=1, freq=40000000, mosi=22)
    SD2 = machine.SDCard(slot=2, mosi=22, miso=21, cs=18, sck=19)
    uos.mount(SD2, "/sd2")
    
def SDtest2():
    Start = utime.ticks_ms()
    
    for i in range(5):
        with open("sd2/test.txt", "w") as file:
            for i in range(10001):
                file.write("12345678\r\n")
    
        
    End = utime.ticks_ms()
    print((End-Start) / 5)
    