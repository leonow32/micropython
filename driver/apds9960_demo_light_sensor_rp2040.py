import apds9960
import machine
import mem_used
import neopixel

def light_data_print(source):
    valid  = dut.als.valid_check()
    saturation = dut.als.saturation_check()
    result = dut.als.read()
    print(f"C: {result[0]:5d}, R: {result[1]:5d}, G: {result[2]:5d}, B: {result[3]:5d}, Valid: {valid}, Saturation: {saturation}")

def light_saturation_irq():
    print("Light sensor saturation IRQ")

def light_irq():
    value = dut.als.read()[0]
    low_threshold  = dut.als.irq_low_threshold_get()
    high_threshold = dut.als.irq_high_threshold_get()
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
        
    if value >= high_threshold:
        led[0] = (10, 0, 0)
    elif value <= low_threshold:
        led[0] = (0, 10, 0)
    else:
        led[0] = (0, 0, 10)
        
    led.write()
    
i2c  = machine.I2C(0) # use default pinout and clock frequency
irq  = machine.Pin(16)
led  = neopixel.NeoPixel(machine.Pin(0, machine.Pin.OUT), 1)
ledr = machine.Pin(18, machine.Pin.OUT)
ledy = machine.Pin(19, machine.Pin.OUT)
ledg = machine.Pin(20, machine.Pin.OUT)
dut  = apds9960.APDS9960(i2c, irq)
tim  = machine.Timer(mode=machine.Timer.PERIODIC, period=1000, callback=light_data_print)

print(dut)

dut.everything_disable()
dut.irq_clear_all_flags()

dut.als.gain_set(apds9960.AGAIN_64X)
dut.als.integration_time_set(100)
dut.als.irq_low_threshold_set(1000)
dut.als.irq_high_threshold_set(5000)
dut.als.irq_persistance_set(apds9960.APERS_3_CYCLE)
dut.als.irq_saturation_callback_set(light_saturation_irq)
dut.als.irq_saturation_enable()
dut.als.irq_callback_set(light_irq)
dut.als.irq_enable()
dut.als.enable()

mem_used.print_ram_used()

