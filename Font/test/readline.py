import mem_used
import gc
import time
start_time = time.ticks_us()

output = ""
with open("font/squared16B_unicode.py") as file:
    output = file.readlines()[10]

print(output)

gc.collect()
mem_used.print_ram_used()
end_time = time.ticks_us()
print(f"Work time: {end_time-start_time} us")