# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import bluetooth
import binascii

DEVICE_NAME = "ESP32-S3"
conn_handle = None
tx_handle = None

# Simple
# SIMPLE_UUID = bluetooth.UUID(1)
# SIMPLE_CHAR = (bluetooth.UUID(2), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
# SIMPLE_SERVICE = (SIMPLE_UUID, (SIMPLE_CHAR,),)

# Heart rate
# HR_UUID = bluetooth.UUID(0x180D)
# HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
# HR_SERVICE = (HR_UUID, (HR_CHAR,),)

# Uart Nordic
# UART_UUID =  bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# UART_RX   = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE,)
# UART_TX   = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
# UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)

# Uart Microchip
MUART_UUID =  bluetooth.UUID("49535343-FE7D-4AE5-8FA9-9FAFD205E455")
MUART_RX   = (bluetooth.UUID("49535343-8841-43F4-A8D4-ECBE34729BB3"), bluetooth.FLAG_WRITE,)
MUART_TX   = (bluetooth.UUID("49535343-1E4D-4BD9-BA61-23C647249616"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
MUART_SERVICE = (MUART_UUID, (MUART_TX, MUART_RX,),)

# Uart test
# TUART_UUID =  bluetooth.UUID("00000001-0000-0000-0000-000000000000")
# TUART_RX   = (bluetooth.UUID("00000002-0000-0000-0000-000000000000"), bluetooth.FLAG_WRITE,)
# TUART_TX   = (bluetooth.UUID("00000003-0000-0000-0000-000000000000"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
# TUART_SERVICE = (TUART_UUID, (TUART_TX, TUART_RX,),)

# Services
#SERVICES = (SIMPLE_SERVICE,)
#SERVICES = (HR_SERVICE, UART_SERVICE, MUART_SERVICE)
#SERVICES = (HR_SERVICE, UART_SERVICE,)
#SERVICES = (HR_SERVICE,)
# SERVICES = (UART_SERVICE,)
SERVICES = (MUART_SERVICE,)
#SERVICES = (TUART_SERVICE,)

handles = ""
ble_msg = ""

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
        print(f"buffer: {buffer}")
        global ble_msg
        ble_msg = buffer.decode('UTF-8').strip()
        print(f"ble_msg: {ble_msg}")
        
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


