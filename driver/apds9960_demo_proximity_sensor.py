import apds9960
import mem_used
import machine

def proximity_data_print(source):
#     dut.irq_read()
    result = dut.proximity_sensor_read()
    print(f"Proximity: {result:3d}")
    
i2c = machine.I2C(0) # use default pinout and clock frequency
irq = machine.Pin(16)
dut = apds9960.APDS9960(i2c, irq)
tim = machine.Timer(0, mode=machine.Timer.PERIODIC, period=1000, callback=proximity_data_print)

print(dut)

print(f"Enable register: {dut.register_read(0x80)}")

dut.irq_clear_all_flags()

dut.proximity_sensor_gain_set(apds9960.PGAIN_8X)
dut.proximity_sensor_enable()

print(f"Enable register: {dut.register_read(0x80)}")

mem_used.print_ram_used()


