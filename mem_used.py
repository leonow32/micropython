# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import os
import gc

def print_rom_used(path = ""):    
    stats = os.statvfs(path)
    block_size   = stats[0]
    total_blocks = stats[2]
    free_blocks  = stats[3]
    total_rom    = total_blocks * block_size
    used_rom     = (total_blocks - free_blocks) * block_size
    print(f"ROM: {used_rom} / {total_rom}")

def print_ram_used():
    gc.collect()
    total_ram = gc.mem_alloc() + gc.mem_free()
    used_ram  = gc.mem_alloc()
    print(f"RAM: {used_ram} / {total_ram}")
  
if __name__ == "__main__":
    print_rom_used()
    print_ram_used()
