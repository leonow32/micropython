# MicroPython 1.27.0 ESP32-S3 Octal SPIRAM

import bluetooth
import binascii
from micropython import const

DEVICE_NAME = "ESP32-S3"

_IRQ_CENTRAL_CONNECT    = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE        = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_MTU_EXCHANGED      = const(21)
_IRQ_CONNECTION_UPDATE  = const(27)

events = {
    _IRQ_CENTRAL_CONNECT:    "Connect",
    _IRQ_CENTRAL_DISCONNECT: "Disconnect",
    _IRQ_GATTS_WRITE:        "Write",
    _IRQ_GATTS_READ_REQUEST: "Read",
    _IRQ_MTU_EXCHANGED:      "MTU Exchanged",
    _IRQ_CONNECTION_UPDATE:  "Connection update"
}

# Uart Microchip
UART_UUID =  bluetooth.UUID("49535343-FE7D-4AE5-8FA9-9FAFD205E455")

UART_TX   = (
    bluetooth.UUID("49535343-1E4D-4BD9-BA61-23C647249616"),
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)

UART_RX   = (
    bluetooth.UUID("49535343-8841-43F4-A8D4-ECBE34729BB3"),
    bluetooth.FLAG_WRITE,
)

UART_SERVICE = (
    UART_UUID,
    (UART_TX, UART_RX,),
)

# Services
SERVICES = (UART_SERVICE,)

conn_handle = None

def bluetooth_interrupt(event, data):
    print(f"- bluetooth_interrupt, event={events[event]}, data={data}")
    
    if event == _IRQ_CENTRAL_CONNECT:
        global conn_handle
        conn_handle = data[0]

    elif event == _IRQ_CENTRAL_DISCONNECT:
        global conn_handle
        conn_handle = None
        advertiser(DEVICE_NAME)
    
    elif event == _IRQ_GATTS_WRITE:
        buffer = ble.gatts_read(data[1])
        buffer = buffer.decode('UTF-8')
        buffer = buffer.strip()
        print(f"Received: {buffer}")

def advertiser(device_name):
    print(f"advertiser({device_name})")
    if isinstance(device_name, str):
        device_name = bytes(device_name, "utf-8")
    advertisement_data = bytearray(b'\x02\x01\x02') + bytearray((len(device_name) + 1, 0x09)) + device_name
    ble.gap_advertise(100, advertisement_data)

def get_my_mac():
    mac = ble.config("mac")
    mac = mac[1]
    mac = binascii.hexlify(mac, ":")
    mac = mac.decode()
    mac = mac.upper()
    return mac

def ble_send(text):
    if conn_handle is None:
        print("No connection")
        return

    if isinstance(text, str):
        text = text.encode("utf-8")

    ble.gatts_notify(conn_handle, tx_handle, text)
    print(f"Sent: {text}")
    
ble = bluetooth.BLE()
ble.active(True)
ble.irq(bluetooth_interrupt)
print(f"MAC Address: {get_my_mac()}")

handles = ble.gatts_register_services(SERVICES)
tx_handle = handles[0][0]
rx_handle = handles[0][1]

advertiser(DEVICE_NAME)
