# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import asyncio
from machine import Pin

async def led_task(gpio_num, period_ms):
    led = Pin(gpio_num, Pin.OUT)
    
    while True:
        led(not led())
        await asyncio.sleep_ms(period_ms)

async def main():
    asyncio.create_task(led_task(21, 1000))
    asyncio.create_task(led_task(47, 500))
    asyncio.create_task(led_task(48, 250))
    asyncio.create_task(led_task(45, 100))
    while True:
        print("main")
        await asyncio.sleep_ms(1000)
    
asyncio.run(main())
