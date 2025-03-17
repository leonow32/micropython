import machine
import esp32
import time

print("=== init ===")
wake_pin1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP, hold=True)
wake_pin2 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP, hold=True)
wake_pin3 = machine.Pin(0,  machine.Pin.IN, machine.Pin.PULL_UP, hold=True)
# esp32.wake_on_ext0(wake_pin1, esp32.WAKEUP_ALL_LOW)
esp32.wake_on_ext1((wake_pin1, wake_pin2), esp32.WAKEUP_ALL_LOW)

print("=== sleep ===")
time.sleep_ms(5)                         # wait for UART to finish transmission
machine.deepsleep(10_000)
# machine.lightsleep(10_000)
