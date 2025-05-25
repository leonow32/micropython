import apds9960
import machine
import mem_used
import neopixel

def light_data_print(source):
    valid  = dut.light_sensor_valid_check()
    result = dut.light_sensor_read()
    print(f"C: {result[0]:5d}, R: {result[1]:5d}, G: {result[2]:5d}, B: {result[3]:5d}, Valid: {valid}")

def light_irq():
    value = dut.light_sensor_read()[0]
    low_threshold  = dut.light_sensor_irq_low_threshold_get()
    high_threshold = dut.light_sensor_irq_high_threshold_get()
    if value >= high_threshold:
        led[0] = (10, 0, 0)
    elif value <= low_threshold:
        led[0] = (0, 10, 0)
    else:
        led[0] = (0, 0, 10)
        
    led.write()
    
i2c = machine.I2C(0) # use default pinout and clock frequency
irq = machine.Pin(16)
dut = apds9960.APDS9960(i2c, irq)
led = neopixel.NeoPixel(machine.Pin(48, machine.Pin.OUT), 1)
tim = machine.Timer(0, mode=machine.Timer.PERIODIC, period=1000, callback=light_data_print)

print(dut)

dut.irq_clear_all_flags()
dut.light_sensor_gain_set(apds9960.AGAIN_64X)
dut.light_sensor_integration_time_set(100)
dut.light_sensor_irq_low_threshold_set(1000)
dut.light_sensor_irq_high_threshold_set(5000)
dut.light_sensor_irq_persistance_set(apds9960.APERS_3_CYCLE)
dut.light_sensor_irq_callback_set(light_irq)
dut.light_sensor_irq_enable()
dut.light_sensor_enable()

mem_used.print_ram_used()
