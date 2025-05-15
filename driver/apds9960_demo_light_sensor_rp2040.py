import apds9960
import mem_used
import machine

def light_data_print(source):
    valid  = dut.light_sensor_valid_check()
    result = dut.light_sensor_read()
    print(f"C: {result[0]:5d}, R: {result[1]:5d}, G: {result[2]:5d}, B: {result[3]:5d}, Valid: {valid}")

def light_irq():
    value = dut.light_sensor_read()[0]
    low_threshold  = dut.light_sensor_irq_low_threshold_get()
    high_threshold = dut.light_sensor_irq_high_threshold_get()
    if value >= high_threshold:
        ledr(1)
        ledy(0)
        ledg(0)
    elif value <= low_threshold:
        ledr(0)
        ledy(0)
        ledg(1)
    else:
        ledr(0)
        ledy(1)
        ledg(0)
    
i2c  = machine.I2C(0) # use default pinout and clock frequency
irq  = machine.Pin(16)
ledr = machine.Pin(18, machine.Pin.OUT)
ledy = machine.Pin(19, machine.Pin.OUT)
ledg = machine.Pin(20, machine.Pin.OUT)
dut  = apds9960.APDS9960(i2c, irq)
tim  = machine.Timer(mode=machine.Timer.PERIODIC, period=1000, callback=light_data_print)

print(dut)

dut.everything_disable()
dut.irq_clear_all_flags()

dut.light_sensor_gain_set(apds9960.AGAIN_64X)
dut.light_sensor_integration_time_set(100)
dut.light_sensor_irq_low_threshold_set(1000)
dut.light_sensor_irq_high_threshold_set(5000)
dut.light_sensor_irq_persistance_set(apds9960.APERS_3_CYCLE)
dut.light_sensor_irq_callback_set(light_irq)
# dut.light_sensor_irq_enable()
dut.light_sensor_enable()

mem_used.print_ram_used()

