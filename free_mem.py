from os import statvfs
from gc import mem_free, mem_alloc

def disk_space():    
    s = statvfs('/')
    block_size   = s[0]
    total_blocks = s[2]
    free_blocks  = s[3]
    total_rom    = total_blocks * block_size
    used_rom     = (total_blocks - free_blocks) * block_size
    print(f'ROM: {used_rom} / {total_rom}')

def ram_free():
    total_ram = mem_alloc() + mem_free()
    used_ram  = mem_alloc()
    print(f'RAM: {used_ram} / {total_ram}')
  
if __name__ == "__main__":
    disk_space()
    ram_free()
