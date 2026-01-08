import bluetooth
import ubinascii
import time
import micropython
from micropython import const

SCAN_TIME_S = const(10)

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE   = const(6)

# Słownik na urządzenia: {adres_mac: [lp, rssi, nazwa]}
devices = {}

def decode_name(payload):
    i = 0
    while i+1 < len(payload):
        length = payload[i]
        type = payload[i+1]
#         if type in (0x08, 0x09):
        if type == 0x08 or type == 0x09:
            try:
                return str(payload[i + 2 : i + length + 1], "utf-8")
            except:
                return "Błąd dekodowania"
        i += length + 1
    return None # Zwracamy None zamiast "Nieznane", by łatwiej było zarządzać logiką

# def print_line(data):
#     mac, rssi, name = data
#     print(f"{mac} | {rssi:4} dBm | {name}")

def ble_irq(event, data):    
    if event == _IRQ_SCAN_RESULT:
        addr_type, mac, adv_type, rssi, adv_data = data
        mac = ubinascii.hexlify(mac, ":").decode().upper()
        
        name = decode_name(adv_data)
        
        # Jeśli urządzenia nie ma jeszcze w słowniku
        if mac not in devices:
#             display_name = name if name else "Nieznane"
#             devices[mac] = [rssi, display_name]
            devices[mac] = [rssi, name]
            
            # Wypisz nowo znalezione urządzenie
#             micropython.schedule(print_line, (mac, rssi, display_name))
            print(f"{mac} | {rssi:3} dBm | {name}")
        
        # Jeśli urządzenie już było, ale nie miało nazwy, a teraz ją znaleźliśmy
#         elif name is not None and devices[mac][1] == "Nieznane":
        elif name is not None and devices[mac][1] == None:
            devices[mac][1] = name
#             lp = devices[mac][0]
            # Ponowne wypisanie tej samej linii z nową nazwą
#             micropython.schedule(print_line, (mac, rssi, f"{name} (zaktualizowano)"))
            print(f"{mac} | {rssi:3} dBm | {name} (nazwa z charakterystyki)")

    elif event == _IRQ_SCAN_DONE:
#         micropython.schedule(lambda _: print("-" * 85 + "\nSkanowanie zakończone."), None)
        print("------------------------------------------")
        print(f"Znaleziono {len(devices)} urządzeń")

ble = bluetooth.BLE()
ble.active(True)

devices.clear()

print("    Adres MAC     |   RSSI   | Nazwa")
print("------------------------------------------")

ble.irq(ble_irq)

# KLUCZOWA ZMIANA: active=True
# Interwał i okno ustawione na 30ms (ciągłe skanowanie)
ble.gap_scan(SCAN_TIME_S * 1000, 30000, 30000, True)

time.sleep(SCAN_TIME_S + 1)

#     end_time = time.ticks_add(time.ticks_ms(), duration_ms + 1000)
#     while time.ticks_diff(end_time, time.ticks_ms()) > 0:
#         time.sleep(0.1)

