import gc

import machine
import onewire
import time
#from time import sleep_ms
import ds18x20

ow = onewire.OneWire(machine.Pin(42))
list = ow.scan()

print(list)

ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print(roms)

ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))
    
total_ram = gc.mem_alloc() + gc.mem_free()
used_ram  = gc.mem_alloc()
print(f'RAM: {used_ram} / {total_ram}')
