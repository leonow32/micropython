from font.squared16B_unicode import *
import mem_used
import gc
import time
start_time = time.ticks_us()

output = squared16B_unicode[40]
print(output)

gc.collect()
mem_used.print_ram_used()
end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")
