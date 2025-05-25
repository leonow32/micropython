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
    led[0] = (value, value, value)
    led.write()
    
i2c = machine.I2C(0) # use default pinout and clock frequency
irq = machine.Pin(16)
dut = apds9960.APDS9960(i2c, irq)
led = neopixel.NeoPixel(machine.Pin(48, machine.Pin.OUT), 1)
tim = machine.Timer(0, mode=machine.Timer.PERIODIC, period=1000, callback=proximity_data_print)

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
