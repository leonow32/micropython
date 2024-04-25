from machine import Pin, I2C
from time import sleep_ms

"""
power = Pin(14, Pin.OUT)
power(0)
sleep_ms(1000)
"""

#i2c = I2C(0, scl=Pin(19), sda=Pin(18), freq=100000)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
devices = i2c.scan()

library = {
    0x18: "LIS331   Accelerometer",
    0x20: "XL9535   GPIO Port",
    0x21: "SDP31    Air Pressure Sensor",
    0x32: "ZMOD4410 TVOC Sensor",
    0x38: "AHT20    Temperature & Humidity Sensor",
    0x39: "APDS9960 Gesture Sensor",
#   0x39: "VCNL4020 Light Sensor",
    0x43: "ENS210   Temperature & Humidity Sensor",
    0x52: "END160   TVOC Sensor",
    0x59: "SGP40    TVOC Sensor",
    0x60: "ATECC608 Crypto Processor",
    0x62: "SCD40    CO2 Sensor",
    0x63: "ICP10111 Barometer Sensor",
    0x69: "SPS30    Air Particle Sensor",
    0x76: "BME280   Temperature & Humidity Sensor",
}

print("Found devices:")
for item in devices:
    print(f"- {item:02X} {library.get(item, "unknown")}")
