# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import bluetooth
import binascii

DEVICE_NAME = "ESP32-S3"

# Uart Microchip
UART_UUID =  bluetooth.UUID("49535343-FE7D-4AE5-8FA9-9FAFD205E455")

UART_RX   = (
    bluetooth.UUID("49535343-8841-43F4-A8D4-ECBE34729BB3"),
    bluetooth.FLAG_WRITE,
)

UART_TX   = (
    bluetooth.UUID("49535343-1E4D-4BD9-BA61-23C647249616"),
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)

UART_SERVICE = (
    UART_UUID,
    (UART_TX, UART_RX,),
)

# Services
SERVICES = (UART_SERVICE,)

conn_handle = None
tx_handle   = None
handles = ""

events = {
    1: "Connect",
    2: "Disconnect",
    3: "Write",
    4: "Read",
    21: "MTU Exchanged",
    27: "Connection update"
}

def bluetooth_interrupt(event, data):
    print(f"- bluetooth_interrupt, event={events[event]}, data={data}")
    
    # _IRQ_CENTRAL_CONNECT
    if event == 1:
        global conn_handle
        conn_handle = data[0]

    # _IRQ_CENTRAL_DISCONNECT
    elif event == 2:
        global conn_handle
        conn_handle = None
        advertiser(DEVICE_NAME)
    
    # _IRQ_GATTS_WRITE
    elif event == 3: #_IRQ_GATTS_WRITE:
        buffer = ble.gatts_read(data[1])
        buffer = buffer.decode('UTF-8').strip()
        print(f"Received: {buffer}")
        
    # _IRQ_GATTS_READ_REQUEST
    elif event == 4:
        pass
        
    # _IRQ_MTU_EXCHANGED
    elif event == 21:
        pass
    
    # _IRQ_CONNECTION_UPDATE
    elif event == 27:
        pass
    
    else:
        print("other")

def advertiser(device_name):
    print(f"advertiser({device_name})")
    if isinstance(device_name, str):
        device_name = bytes(device_name, "utf-8")
    advertisement_data = bytearray(b'\x02\x01\x02') + bytearray((len(device_name) + 1, 0x09)) + device_name
    ble.gap_advertise(100, advertisement_data)
    print(advertisement_data)

def get_my_mac():
    mac = ble.config("mac")
    mac = mac[1]
    mac = binascii.hexlify(mac, ":")
    mac = mac.decode()
    mac = mac.upper()
    return mac

def ble_send(text):
    if conn_handle is None:
        print("Brak połączenia BLE")
        return

    if isinstance(text, str):
        text = text.encode("utf-8")

    ble.gatts_notify(conn_handle, tx_handle, text)
    print(f"Wysłano BLE: {text}")
    
ble = bluetooth.BLE()
ble.active(True)
ble.irq(bluetooth_interrupt)
print(f"Mój adres MAC: {get_my_mac()}")

# register_services()
handles = ble.gatts_register_services(SERVICES)
# handles = ((tx_handle, rx_handle),)
tx_handle = handles[0][0]

advertiser(DEVICE_NAME)

print(handles)

