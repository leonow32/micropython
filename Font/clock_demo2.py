import machine
from font.galaxy16_digits import *
from font.galaxy24_digits import *
import ssd1309
import mem_used
import time
from machine import Timer, lightsleep, deepsleep

def draw():
    time_tuple = time.localtime()
    display.fill(0)
    display.print_text(galaxy24_digits, f"{time_tuple[3]}:{time_tuple[4]:02}", 127, 10, "C")
    display.print_text(galaxy16_digits, f"{time_tuple[2]}.{time_tuple[1]:02}.{time_tuple[0]}", 127, 38, "C")
    display.refresh()
    
def print_system_time():
    time_tuple = time.localtime()
    year    = time_tuple[0]
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    weekday = time_tuple[6]
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piatek", "Sobota", "Niedziela"]
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02} {days[weekday]}")

def timer_int(source):
    print("timer_int ", end="")
    print_system_time()
    draw()

i2c     = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2), freq=400000)
display = ssd1309.SSD1309(i2c)
timer   = Timer(0, mode=Timer.PERIODIC, period=5_000, callback=timer_int)
draw()
mem_used.print_ram_used()

#time.sleep(60)
#machine.lightsleep(60_000)

