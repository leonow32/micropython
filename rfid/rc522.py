from micropython import const
import mem_used

import rfid.reg2 as reg2

print(reg2.COMMAND)



mem_used.print_ram_used()