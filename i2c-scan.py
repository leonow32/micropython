from machine import Pin, I2C
from time import sleep_ms

#i2c = I2C(0, scl=Pin(19), sda=Pin(18), freq=100000)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
devices = i2c.scan()

library = {
    0x18: "LIS331   Accelerometer / MCP9808 Temperature Sensor",
    0x20: "XL9535   GPIO Port",
    0x21: "SDP31    Air Pressure Sensor",
    0x32: "ZMOD4410 TVOC Sensor",
    0x38: "AHT20    Temperature & Humidity Sensor",
    0x39: "APDS9960 Gesture Sensor / VCNL4020 Light Sensor",
    0x3C: "SSD1309 / SH1106 OLED Display",
    0x43: "ENS210   Temperature & Humidity Sensor",
    0x4D: "MCP3x21  ADC",
    0x50: "AT24Cxxx EEPROM Memory",
    0x51: "PCF8563  Real Time Clock",
    0x52: "END160   TVOC Sensor",
    0x59: "SGP40    TVOC Sensor",
    0x5D: "GT911    Touch Panel",
    0x60: "ATECC608 Crypto Processor / MCP472x DAC",
    0x62: "SCD40    CO2 Sensor",
    0x63: "ICP10111 Barometer Sensor",
    0x68: "DS1307   Real Time Clock / MCP342x ADC"
    0x69: "SPS30    Air Particle Sensor",
    0x6F: "MCP7940  Real Time Clock",
    0x76: "BME280   Temperature & Humidity Sensor",
}

print("Found devices:")
for item in devices:
    print(f"- {item:02X} {library.get(item, "unknown")}")
