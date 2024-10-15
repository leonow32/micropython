import machine
import uos

global SD

def SDmount():
    global SD
    SD = machine.SDCard(slot=3, width=1, freq=20000000)
    uos.mount(SD, "/sd")
    