
from time import sleep_ms
import app.button as button
import app.config as config
import app.control_task as control_task
import app.ens210 as ens210
import app.hlw8110 as hlw8110
import app.relay as relay
import app.server_http2 as server_http
import app.server_dns as server_dns
import app.wifi_ap as wifi_ap
import app.wifi_sta as wifi_sta
import app.ws2812 as led

config.init()

# If the button is pressed DO NOT start all the tasks
button.init()
if button.get() == 0:
    
    
    """
    if config.get("led-type") == "classic":
        import app.led as led
        led.init()
    if config.get("led-type") == "ws2812":
        import app.ws2812 as led
        led.init()
    """
    ens210.init()
    ens210.run_task()
    relay.init()
    hlw8110.init()
    hlw8110.run_task()
    control_task.init()
    control_task.run_task()
    wifi_ap.init()
    wifi_sta.init()
    server_dns.init()
    server_dns.run_task()
    server_http.init()
    server_http.run_task()
else:
    print("Startup interrupted")