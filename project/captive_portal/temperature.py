import machine
import sys

if sys.platform == "esp32":
    import esp32
elif sys.platform == "rp2":
    from machine import ADC
else:
    raise Exception("Microcontroller not supported")

def temperature_get():
    if "ESP32 " in sys.implementation._machine:
        return int((esp32.raw_temperature() - 32) / 1.8)
    elif "ESP32S3" in sys.implementation._machine:
        return esp32.mcu_temperature()
    elif "RP2040" in sys.implementation._machine:
        temp_sensor = ADC(4)
        adc_value = temp_sensor.read_u16()
        voltage = adc_value * (3.3 / 65535.0)
        temperature_celsius = 27 - (voltage - 0.706) / 0.001721
        return temperature_celsius
    else:
        raise Exception("Microcontroller not supported")


