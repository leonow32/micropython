# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

from machine import Pin, I2C

i2c = I2C(0)
# i2c = I2C(0, freq=100_000)
# i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
# i2c = I2C(0, scl=Pin(1),  sda=Pin(2),  freq=100000)
# i2c = I2C(0, scl=Pin(25), sda=Pin(26), freq=100000)
# i2c = I2C(0, scl=Pin(2),  sda=Pin(1),  freq=100000)      # TT v3.4

print(i2c)

devices = i2c.scan()

library = {
    0x08: "GreenPAK",
    0x14: "GT911",
    0x18: "LIS331 / MCP9800",
    0x20: "XL9535",
    0x21: "SDP31",
    0x32: "ZMOD4410",
    0x38: "AHT20 / FTxxxx / HY4613",
    0x39: "APDS9960 / VCNL4020",
    0x3C: "SSD1306 / SSD1309 / SSD1363 / SH1106",
    0x3D: "SSD1306 / SSD1309 / SSD1363 / SH1106",
    0x41: "ILI2130",
    0x43: "ENS210",
    0x4D: "MCP3x21",
    0x50: "24Cxxx",
    0x51: "PCF8563",
    0x52: "ENS160",
    0x55: "ST1XXX",
    0x59: "SGP40",
    0x5D: "GT911",
    0x60: "ATECC608 / MCP472x",
    0x62: "ILI2130 / SCD40",
    0x63: "ICP10111",
    0x68: "DS1307 / MCP342x",
    0x69: "SPS30",
    0x6F: "MCP7940",
    0x76: "BME280 / BMP280",
    0x77: "BMP280"
}

print("Found devices: ")
for device in devices:
    print(f" - {device:02X}: {library.get(device, "unknown")}")

