from gc import mem_free, mem_alloc
from os import statvfs

def disk_space():
  s = statvfs('//')
  print('ROM: {0} B'.format(s[0]*s[3]))

def ram_free():
  Free = mem_free()
  Used = mem_alloc()
  print('RAM: {0} / {1}'.format(Used, Free))
  
disk_space()
ram_free()
