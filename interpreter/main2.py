# Interpreter poleceń odwróconej notacji polskiej
from interpreter_core import *
import gc
import os
import uos
import machine
import network
import socket
import ubinascii
import time
from machine import Pin
from machine import PWM
from machine import ADC
from machine import Timer
from machine import SDCard

Sta = network.WLAN(network.STA_IF)
RamDrive = 0
SD = 0
bdev = 0

# Tablica wszystkich poleceń
Commands = {
    "ram":              lambda ii: CmdRam(ii),
    "gc":               lambda ii: CmdGarbageCollector(ii),
    
    "ramd":             lambda ii: CmdRamDrive(ii),
    "ramdformat":       lambda ii: CmdRamDriveFormat(ii),
    "ramm":             lambda ii: CmdRamDriveMount(ii),
    "ramu":             lambda ii: CmdRamDriveUnmount(ii),
    "rami":             lambda ii: CmdRamDriveInit(ii),
    
    "ramf":             lambda ii: CmdRamDriveTestFile(ii),
    "ramwb":            lambda ii: CmdRamDriveWriteBlock(ii),
    "ramb":             lambda ii: CmdRamDriveReadBlocks(ii),
    
    "ramo":             lambda ii: CmdRamDriveOriginal(ii),
    "ramodump":         lambda ii: CmdRamDriveOriginalDump(ii),
    
    # Pliki
    "dir":              lambda ii: CmdFileList(ii),
    "read":             lambda ii: CmdFileRead(ii),
    "write":            lambda ii: CmdFileWrite(ii),
    
    "sd":               lambda ii: CmdSDmount(ii),
    "sdu":              lambda ii: CmdSDunmount(ii),
    "script":           lambda ii: CmdSDrunScript(ii),
    
    # Pamięć RTC
    "rtcr":             lambda ii: CmdRtcMemRead(ii),
    "rtcw":             lambda ii: CmdRtcMemWrite(ii),
    
    "exit":             lambda ii: CmdExit(ii),
    "all":              lambda ii: CmdAllCommands(ii),
    "vars":             lambda ii: CmdVariables(ii),
    "=":                lambda ii: CmdSetVariable(ii),
    "const":            lambda ii: CmdConst(ii),
    "echo":             lambda ii: CmdEcho(ii),
    "inc":              lambda ii: CmdOperatorInc(ii),
    "dec":              lambda ii: CmdOperatorDec(ii),
    "+":                lambda ii: CmdOperatorAdd(ii),
    "-":                lambda ii: CmdOperatorSub(ii),
    "*":                lambda ii: CmdOperatorMul(ii),
    "/":                lambda ii: CmdOperatorDiv(ii),
    "led":              lambda ii: CmdLed(ii),
    "pin":              lambda ii: CmdPinRead(ii),
    "pins":             lambda ii: CmdPinReadAll(ii),
    "inall":            lambda ii: CmdPinInputAll(ii),
    "out":              lambda ii: CmdPinOutput(ii),
    "pwm":              lambda ii: CmdPWM(ii),
    "adc":              lambda ii: CmdAdc(ii),
    "timer":            lambda ii: CmdTimer(ii),
    "timerd":           lambda ii: CmdTimerDeinit(ii),
    
    # WIFI
    "sta":              lambda ii: CmdWifiIP(ii),
    "connect":          lambda ii: CmdWifiConnect(ii),
    "disconnect":       lambda ii: CmdWifiDisconnect(ii),
    "starwars":         lambda ii: CmdStarWars(ii),
    "get":              lambda ii: CmdGet(ii),
    "scan":             lambda ii: CmdScan(ii),
}

# Ile wolnej pamieci RAM
def CmdRam(ii):
    return gc.mem_free()

# Garbage Collector
def CmdGarbageCollector(ii):
    gc.collect()
    return gc.mem_free()

# Ram Drive RTC to emulate physical memory
class RtcDriveBlock:
    def __init__(self, BlockSize=64):
        self.block_size = BlockSize

    def readblocks(self, block_num, buf, offset=0):
        
        # Read RTC and adjust to 2048 byles length
        Data = machine.RTC().memory()
        BytesToAdd = 2048 - len(Data)
        #Data = Data + bytes([0x00] * BytesToAdd)
        Data = Data + bytearray(b'\x00' * BytesToAdd)
        
        # Save to output
        Address = block_num * self.block_size + offset
        for i in range(len(buf)):
            buf[i] = Data[Address + i]

    def writeblocks(self, block_num, buf, offset=0):
        if offset is None:
            offset = 0
        
        # Read RTC and adjust to 2048 byles length
        Data = machine.RTC().memory()
        BytesToAdd = 2048-len(Data)
        #Data = Data + bytes([0x00] * BytesToAdd)
        Data = Data + bytearray(b'\x00' * BytesToAdd)
        
        # Insert new block into Data buffer
        Address = block_num * self.block_size + offset
        if Address == 0:
            Data = buf + Data[len(buf):]
        else:
            Data = Data[0:Address] + buf + Data[Address+len(buf):]
        
        # Save to RTC memory
        machine.RTC().memory(Data)

    def ioctl(self, op, arg):
        
        # Number of blocks
        if op == 4:
            return 2048 // self.block_size
        
        # Block size
        if op == 5:
            return self.block_size
        
        # Block erase
        if op == 6: 
            print("BlockErase={}".format(arg))
            Data = machine.RTC().memory()
            Address = arg * self.block_size
            Empty = bytearray(b'\x00'*64)
            if Address == 0:
                Data = Empty + Data[64:]
            else:
                Data = Data[0:Address] + Empty + Data[Address+64:]
            machine.RTC().memory(Data)
            return 0
        
# Utworzenie RAM Drive
def CmdRamDrive(ii):
    gc.collect()
    #BlockSize = int(ii.Interpreter(ii))
    BlockSize = 64
    #Blocks = int(ii.Interpreter(ii))
    
    # kasowanie
    #machine.RTC().memory(bytes([0x00]*2048))
    
    global RamDrive
    RamDrive = RtcDriveBlock()
    #print("RamDrive = {}".format(RamDrive))
    
    # Sprawdzanie czy mozna zamonotwac (jezeli nie to pamiec jest pusta i trzeba ja sformatowac)
    try:
        print("===mount===")
        os.mount(RamDrive, "/rtc")
    except:
        print("===Can't mount===")
        print("===Vfs===")
        #os.VfsFat.mkfs(RamDrive)
        os.VfsLfs2.mkfs(RamDrive)
        print("===mount===")
        os.mount(RamDrive, "/rtc")
    
# Zamontowanie dysku ktory juz istnieje w pamieci RTC
def CmdRamDriveMount(ii):
    global RamDrive
    RamDrive = RtcDriveBlock(64)
    os.mount(RamDrive, '/rtc')
    
# Odmontowanie
def CmdRamDriveUnmount(ii):
    os.umount('/rtc')
    
# Wpisanie testowej zawartosci do RTC
def CmdRamDriveInit(ii):
    machine.RTC().memory(b'\x03\x00\x00\x00\xf0\x0f\xff\xf7littlefs/\xe0\x00\x10\x00\x00\x02\x00@\x00\x00\x00 \x00\x00\x00\xff\x00\x00\x00\xff\xff\xff\x7f\xfe\x03\x00\x00@\x0f\xfc\x10\t\x00\x00\x00\n\x00\x00\x000\x10\x00\x0c\x8b]\x1f\x0f\x02\x00\x00\x00\xf0\x0f\xff\xf7littlefs/\xe0\x00\x10\x00\x00\x02\x00@\x00\x00\x00 \x00\x00\x00\xff\x00\x00\x00\xff\xff\xff\x7f\xfe\x03\x00\x00p\x1f\xfc\x08I\x0f\x05\xf3\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xff\xef\xff\xfaa.txt \x00\x00\x05p\x0f\xfc\x0b\x1c\xe7\xd4/\xff\xff\xff\xff\xff\xff\xff\xf0\x0f\xfc\x08aaa\x10\x00\x00\x0b\x90v\x1e\xc3\xd6L#\r`\x1f\xfc\x01o\xed\xbe\xb6\xff\xff\xff\xff\xff\x02\x00\x00\x00\xff\xef\xff\xfaa.txt \x00\x00\x06aaa\x10\x00\x00\x0b\x90v\x1e\xc3\xd6L#\rP\x0f\xfc\x00\x0b\x00\x00\x00\x0c\x00\x00\x000\x10\x00\x18\xed\x00\x05}\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x00\x00\x00\xff\xef\xff\xfab.txt \x00\x00\x05p\x0f\xfc\x0b\xd2\x8b\x1e\x92\xff\xff\xff\xff\xff\xff\xff\xf0\x0f\xfc\x0ebbbbb\x10\x00\x00\r\x88Lv\xc3\xd8L#\r`\x1f\xfc\x0f\x85v\xc2\xbf\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def CmdRamDriveTestFile(ii):
    temp = bytearray()
    for i in range(256):
        temp += bytearray([i])
        
    f=open("/rtc/bytes.txt", "wb")
    f.write(temp)
    f.close()

def CmdRamDriveWriteBlock(ii):
    #block = ii.Interpreter(ii)
    
    buf = bytearray()
    #for i in range(192,256):
    #    buf += bytearray([i])
        
    #RamDrive.writeblocks(block, buf, 0)
    for block in range(2,32):
        buf = bytearray([block] * 64)
        RamDrive.writeblocks(block, buf, 0)
    

def CmdRamDriveReadBlocks(ii):
    RamDrive = RtcDriveBlock()
    for block in range(32):
        buf = bytearray([0x00] * 64)
        RamDrive.readblocks(block, buf, 0)
        print("=={}== ".format(block), end="")
        print(buf)

# Oryginalna klasa do ramdrive
class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)
        print("BlockSize  = {}".format(block_size))
        print("len(Data) = {}".format(len(self.data)))
        print("Data = {}".format(self.data))

    def readblocks(self, block_num, buf, offset=0):
        print("readblocks(block_num={}, len(buf)={}, type(buf)={}, offset={})".format(block_num, len(buf), type(buf), offset))
        addr = block_num * self.block_size + offset
        for i in range(len(buf)):
            buf[i] = self.data[addr + i]

    def writeblocks(self, block_num, buf, offset=None):
        print("writeblocks(block_num={}, len(buf)={}, type(buf)={}, offset={})".format(block_num, len(buf), type(buf), offset))
        print(buf)
        if offset is None:
            # do erase, then write
            for i in range(len(buf) // self.block_size):
                self.ioctl(6, block_num + i)
            offset = 0
        addr = block_num * self.block_size + offset
        for i in range(len(buf)):
            self.data[addr + i] = buf[i]

    def ioctl(self, op, arg):
        print("ioctl(op={}, arg={}) ".format(op, arg), end='')
        if op == 4: # block count
            return len(self.data) // self.block_size
        if op == 5: # block size
            return self.block_size
        if op == 6: # block erase
            return 0
        
    def dump(self):
        print("type(self.data)={}".format(type(self.data)))
        print(self.data)

def CmdRamDriveOriginal(ii):
    #block_size = int(ii.Interpreter(ii))
    #num_blocks = int(ii.Interpreter(ii))
    block_size = 64
    num_blocks = 32
    global bdev
    bdev = RAMBlockDev(block_size, num_blocks)
    print("===Vfs===")
    os.VfsLfs2.mkfs(bdev)
    print("===mount===")
    os.mount(bdev, '/ramdisk')
    
def CmdRamDriveOriginalDump(ii):
    global bdev
    bdev.dump()

def isfolder(path):
    try:
        os.chdir(path)
        os.chdir("..")
        return True
    except:
        return False

def ListFolder(Path="", Level=0):
    List = uos.listdir(Path)
    for Item in List:
        if isfolder(Path + "/" + Item):
            print("F{} {}".format(" " * Level, Item))
            ListFolder(Path + "/" + Item, Level + 1)
        else:
            Type = "Folder" if isfolder(Item) else "Folder"
            print(" {} {}".format(" " * Level, Item))

# Lista plików
def CmdFileList(ii):
    try:
        Path = ii.Interpreter(ii)
    except:
        Path = ""
    if Path == None:
        Path = ""
    ListFolder(Path)

# Odczytanie pliku
def CmdFileRead(ii):
    File = str(ii.Interpreter(ii))
    try:
        with open(File) as f:
            Data = f.read()
            print(Data)
    except:
        print("Can't open")
        
# Zapis do pliku
def CmdFileWrite(ii):
    File = str(ii.Interpreter(ii))
    Data = str(ii.Interpreter(ii))
    print("Zapis {} w pliku {}".format(Data, File))
    try:
        F = open(File, "a")
        Len = F.write(Data)
        F.close()
        return Len
    except:
        print("Can't save")
    #try:
    #    with open(File, 'a') as f:
    #        f.write(Data)
    #except:
    #    print("Can't save")

# Zamontowanie karty SD
def CmdSDmount(ii):
    global SD
    SD = machine.SDCard(slot=2, width=1, freq=20000000)
    uos.mount(SD, "./sd")
    
# Odmontowanie karty SD
def CmdSDunmount(ii):
    global SD
    uos.umount("./sd")
    SD = None
    
# Uruchomienie skryptu z karty SD
def CmdSDrunScript(ii):
    import sd.script
    sd.script.main()

# RTC memory read
def CmdRtcMemRead(ii):
    return machine.RTC().memory()

# RTC memory write
def CmdRtcMemWrite(ii):
    Data = str(ii.Interpreter(ii))
    return machine.RTC().memory(Data)

# Download
def http_get(url):
    print(url)
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    
def InterruptPin(arg):
    print("interrupt: {}".format(arg))

def InterruptTimer(arg):
    print("timer: {}".format(arg))

def CmdExit(ii):
    quit()
    return 

def CmdAllCommands(ii):
    i = 0
    for Item in ii.Commands.keys():
        print("{}:\t{}".format(i, Item))
        i = i+1

def CmdVariables(ii):
    for Name, Value in ii.Variables.items():
        print("{}:\t{}".format(Name, Value))

def CmdSetVariable(ii):
    Name = str(ii.Args[0])
    
    ### Dodać sprawdzenie czy nazwa zmiennej nie koliduje z jakąś nazwą funkcji

    ii.Args = ii.Args[1:]
    Value = ii.Interpreter(ii)
    ii.Variables[Name] = Value
    return Value

def CmdConst(ii):
    return 123

def CmdEcho(ii):
    return ii.Interpreter(ii)

def CmdOperatorInc(ii):
    return ii.Interpreter(ii) + 1

def CmdOperatorDec(ii):
    return ii.Interpreter(ii) - 1

def CmdOperatorAdd(ii):
    return ii.Interpreter(ii) + ii.Interpreter(ii)

def CmdOperatorSub(ii):
    return ii.Interpreter(ii) - ii.Interpreter(ii)

def CmdOperatorMul(ii):
    return ii.Interpreter(ii) * ii.Interpreter(ii)

def CmdOperatorDiv(ii):
    return ii.Interpreter(ii) / ii.Interpreter(ii)

def CmdTestDodawaniaPolecen(ii):
    print("Polecenie dodane po konstruktorze")
    return None

def CmdLed(ii):
    p = Pin(2, Pin.OUT)
    Mode = ii.Interpreter(ii)
    if Mode == 1:
        p.value(1)
    elif Mode == 0:
        p.value(0)
    else:
        print("Bad arg")
    return None

def CmdPinRead(ii):
    numer = int(ii.Interpreter(ii))
    print("Pin {}".format(numer))
    p = Pin(numer, Pin.IN)
    print("stan = {}".format(p))
    return p.value()

def CmdPinReadAll(ii):
    for p in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33,34,35,36,37,38,39]:
        pin = Pin(p)
        v = pin.value()
        print("Pin {}\t{}".format(p, v))
    return None

def CmdPinInputAll(ii):
    for p in [0,2,4,5,9,10,12,13,14,15,18,19,21,22,23,25,26,27,32,33,34,35,36,37,38,39]:
        pin = Pin(p, Pin.IN)
        v = pin.value()
        print("Pin {}\t{}".format(p, v))
    return None

def CmdPinOutput(ii):
    numer = int(ii.Interpreter(ii))
    print("Pin {} = OUT".format(numer))
    p = Pin(numer, Pin.OUT)
    for i in range(3):
        print("Pin {} = 1".format(numer))
        p.value(1)
        time.sleep(1)
        print("Pin {} = 0".format(numer))
        p.value(0)
        time.sleep(1)
    

def CmdPWM(ii):
    value = int(ii.Interpreter(ii))
    if value >= 1024:
        print("Value of of range 0-1023")
        return None
    #pwm0 = PWM(Pin(2))
    #pwm0.freq(1000)
    #pwm0.duty(value)
    pwm2 = PWM(Pin(2), freq=10000, duty=value) # create and configure in one go
    return None

def CmdAdc(ii):
    pinnr = ii.Interpreter(ii)
    adc = ADC(Pin(pinnr))
    return adc.read()

def CmdTimer(ii):
    TimerNumber = ii.Interpreter(ii)
    PeriodTime = ii.Interpreter(ii)
    timer = machine.Timer(TimerNumber)
    timer.init(period=PeriodTime, mode=Timer.PERIODIC, callback=InterruptTimer)
    print("Timer {} set period to {}".format(TimerNumber, PeriodTime))
    return None

def CmdTimerDeinit(ii):
    TimerNumber = ii.Interpreter(ii)
    timer = machine.Timer(TimerNumber)
    timer.deinit()
    print("Timer {} deinit".format(TimerNumber))
    return None

def CmdWifiIP(ii):
    global Sta
    print("Active: {}".format(Sta.active()))
    print("IsConnected: {}".format(Sta.isconnected()))
    print(Sta.ifconfig())
 
def CmdWifiConnect(ii):
    global Sta
    Sta.active(True)
    Sta.connect("Extronic2.4", "LeonInstruments")
    while not Sta.isconnected():
        pass
    print("network config:", Sta.ifconfig())
    
def CmdWifiDisconnect(ii):
    global Sta
    Sta.disconnect()
    print("network config:", Sta.ifconfig())
    
def CmdStarWars(ii):
    addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
    print("addr_info={}".format(addr_info))
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)
    while True:
        data = s.recv(500)
        print(str(data, 'utf8'), end='')
    return None

def CmdGet(ii):
    #Address = ii.Interpreter(ii)
    #Address = "http://extronic.pl/robots.txt"
    Address = "http://micropython.org/ks/test.html"
    http_get(Address)
    return None

def CmdScan(ii):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    List = wlan.scan()             # scan for access points
    print("Wykryte sieci:")
    print("Num\tChannel\tRSSI\tauth\thidden\tbssid\t\tSSID")
    Num = 1
    for Item in List:
        
        # Number
        print(Num, end='\t')
        Num += 1
        
        # Channel
        print(Item[2], end='\t')
        
        # RSSI
        print(Item[3], end='\t')
        
        # Authmode
        print(Item[4], end='\t')
        
        # Hidden
        print(Item[5], end='\t')
        
        # bssid
        print(ubinascii.hexlify(Item[1]).decode('utf-8'), end='\t')
        
        # SSID
        print(Item[0].decode('utf-8'))




 

# Funkcja main
def main():
    
    gc.enable()
    
    # Informacja o pamięci
    fs_stat = uos.statvfs('/')
    print("Free flash:\t{}".format((fs_stat[0]*fs_stat[3])/1048576))
    print("Free RAM:\t{}".format(gc.mem_free()))
    
    # Przerwania
    p0 = machine.Pin(0, Pin.IN, Pin.PULL_UP)
    p0.irq(trigger=Pin.IRQ_FALLING, handler=InterruptPin)
    
    # Instancja interpretera
    Inter0 = InterpreterClass(Commands)
    
    #bdev2 = RAMBlockDev(16, 16)
    #os.VfsLfs2.mkfs(bdev2)
    #os.mount(bdev, '/ramdisk')
    
    while True:
        InputCommand = input("0> ")                                                          # Prompt
        Result = Inter0.InterpreterString(InputCommand, Inter0)
        print("Result0 = {}".format(Result))

if __name__ == "__main__":
    main()