from micropython import const
import mem_used

import rfid.reg as reg

print(reg.COMMAND)



mem_used.print_ram_used()