import apds9960
import machine
import mem_used
import neopixel

def proximity_data_print(source):
    valid      = dut.prox.valid_check()
    saturation = dut.prox.saturation_check()
    result     = dut.prox.read()
    print(f"Proximity: {result:3d}, Valid: {valid}, Saturation: {saturation}")
    
def proximity_saturation_irq():
    print("Proximity sensor saturation IRQ")
    
def proximity_irq():
    value = dut.prox.read()
    low_threshold  = dut.prox.irq_low_threshold_get()
    high_threshold = dut.prox.irq_high_threshold_get()
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
    
    led[0] = (value, value, value)
    led.write()

i2c  = machine.I2C(0) # use default pinout and clock frequency
irq  = machine.Pin(16)
led  = neopixel.NeoPixel(machine.Pin(0, machine.Pin.OUT), 1)
ledr = machine.Pin(18, machine.Pin.OUT)
ledy = machine.Pin(19, machine.Pin.OUT)
ledg = machine.Pin(20, machine.Pin.OUT)
dut  = apds9960.APDS9960(i2c, irq)
tim  = machine.Timer(mode=machine.Timer.PERIODIC, period=1000, callback=proximity_data_print)

print(dut)

dut.everything_disable()
dut.irq_clear_all_flags()

dut.prox.gain_set(apds9960.PGAIN_8X)
dut.prox.led_drive_set(apds9960.LDRIVE__100_MA)
dut.prox.led_boost_set(apds9960.LED_BOOST_300_P)
dut.prox.irq_low_threshold_set(100)
dut.prox.irq_high_threshold_set(200)
dut.prox.irq_persistance_set(apds9960.PPERS_EVERYTIME)
dut.prox.irq_saturation_callback_set(proximity_saturation_irq)
dut.prox.irq_saturation_enable()
dut.prox.irq_callback_set(proximity_irq)
dut.prox.irq_enable()
dut.prox.enable()

mem_used.print_ram_used()
