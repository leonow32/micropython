import apds9960
import mem_used
import machine
    
i2c  = machine.I2C(0) # use default pinout and clock frequency
irq  = machine.Pin(16)
dut  = apds9960.APDS9960(i2c, irq)

print(dut)

dut.irq_clear_all_flags()
print(dut.proximity_sensor_enabled_check())
dut.proximity_sensor_enable()
print(dut.proximity_sensor_enabled_check())

print(f"Proximity data: {dut.proximity_sensor_read()}")

mem_used.print_ram_used()


