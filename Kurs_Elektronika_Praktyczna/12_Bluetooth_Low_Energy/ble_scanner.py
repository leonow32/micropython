import bluetooth
import ubinascii
import time
import micropython

# Stałe zdarzeń BLE
_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6

# Słownik na urządzenia: { adres_mac: [lp, rssi, nazwa] }
seen_devices = {}
device_counter = 0

def decode_name(payload):
    """Wyciąga nazwę urządzenia z danych rozgłoszeniowych."""
    i = 0
    while i + 1 < len(payload):
        length = payload[i]
        type = payload[i + 1]
        if type in (0x08, 0x09):
            try:
                return str(payload[i + 2 : i + length + 1], "utf-8")
            except:
                return "Błąd dekodowania"
        i += length + 1
    return None # Zwracamy None zamiast "Nieznane", by łatwiej było zarządzać logiką

def print_line(data):
    """Bezpieczne wypisanie linii w konsoli."""
    lp, mac, rssi, name = data
    print(f"{lp:<3} | {mac} | {rssi:4} dBm | {name}")

def ble_irq(event, data):
    global device_counter
    
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        mac_address = ubinascii.hexlify(addr, ":").decode().upper()
        
        name = decode_name(adv_data)
        
        # Jeśli urządzenia nie ma jeszcze w słowniku
        if mac_address not in seen_devices:
            device_counter += 1
            display_name = name if name else "Nieznane"
            seen_devices[mac_address] = [device_counter, rssi, display_name]
            
            # Wypisz nowo znalezione urządzenie
            micropython.schedule(print_line, (device_counter, mac_address, rssi, display_name))
        
        # Jeśli urządzenie już było, ale nie miało nazwy, a teraz ją znaleźliśmy
        elif name is not None and seen_devices[mac_address][2] == "Nieznane":
            seen_devices[mac_address][2] = name
            lp = seen_devices[mac_address][0]
            # Ponowne wypisanie tej samej linii z nową nazwą
            micropython.schedule(print_line, (lp, mac_address, rssi, f"{name} (zaktualizowano)"))

    elif event == _IRQ_SCAN_DONE:
        micropython.schedule(lambda _: print("-" * 85 + "\nSkanowanie zakończone."), None)

def start_scanning(duration_ms=15000):
    global device_counter
    ble = bluetooth.BLE()
    ble.active(True)
    
    seen_devices.clear()
    device_counter = 0
    
    print(f"Rozpoczynam AKTYWNE skanowanie...")
    print(f"{'LP':3} | {'ADRES MAC':17} | {'SYGNAŁ':10} | {'NAZWA URZĄDZENIA'}")
    print("-" * 85)
    
    ble.irq(ble_irq)
    
    # KLUCZOWA ZMIANA: active=True
    # Interwał i okno ustawione na 30ms (ciągłe skanowanie)
    ble.gap_scan(duration_ms, 30000, 30000, True)
    
    end_time = time.ticks_add(time.ticks_ms(), duration_ms + 1000)
    while time.ticks_diff(end_time, time.ticks_ms()) > 0:
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        start_scanning(30000)
    except KeyboardInterrupt:
        print("\nZatrzymano.")