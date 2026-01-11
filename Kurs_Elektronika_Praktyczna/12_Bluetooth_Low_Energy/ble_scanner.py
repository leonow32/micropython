import bluetooth
import ubinascii
import time
from micropython import const

# Czas skanowania
SCAN_TIME_MS = const(30_000)

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE   = const(6)

# Słownik do zapisywania znalezionych urządzeń
# {mac: [rssi, name]}
devices = {}

def decode_name(payload):
    i = 0
    while i+1 < len(payload):
        length = payload[i]
        type = payload[i+1]
        if type == 0x08 or type == 0x09:
            try:
                return str(payload[i+2 : i+length+1], "utf-8")
            except:
                return "Błąd dekodowania"
        i += length + 1
    return None

def bluetooth_interrupt(event, data):    
    if event == _IRQ_SCAN_RESULT:
        addr_type, mac, adv_type, rssi, adv_data = data
        mac = ubinascii.hexlify(mac, ":").decode().upper()
        name = decode_name(adv_data)
        
        # Jeśli urządzenia nie ma jeszcze w słowniku
        if mac not in devices:
            devices[mac] = [rssi, name]
            print(f"{mac} | {rssi:4} dBm | {name}")
        
        # Jeśli urządzenie już było, ale nie miało nazwy, a teraz ją znaleźliśmy
        elif devices[mac][1] == None and name is not None:
            devices[mac][1] = name
            print(f"{mac} | {rssi:4} dBm | {name} (nazwa z charakterystyki)")

    elif event == _IRQ_SCAN_DONE:
        print("------------------------------------------")
        print(f"Znaleziono {len(devices)} urządzeń")

ble = bluetooth.BLE()
ble.active(True)
ble.irq(bluetooth_interrupt)
ble.gap_scan(SCAN_TIME_MS, 30000, 30000, True)

print("    Adres MAC     |   RSSI   | Nazwa")
print("------------------------------------------")

time.sleep_ms(SCAN_TIME_MS + 100)
