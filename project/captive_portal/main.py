# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import dns
import http
import led
import temperature
import wifi_ap

led.init()
wifi_ap.init("Captive Portal Hot Spot")
#dns.init()
http.init()
