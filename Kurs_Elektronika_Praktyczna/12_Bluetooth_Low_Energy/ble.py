# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

import bluetooth

DEVICE_NAME = "ESP32-S3"

# Simple
SIMPLE_UUID = bluetooth.UUID(1)
SIMPLE_CHAR = (bluetooth.UUID(2), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
SIMPLE_SERVICE = (SIMPLE_UUID, (SIMPLE_CHAR,),)

# Heart rate
HR_UUID = bluetooth.UUID(0x180D)
HR_CHAR = (bluetooth.UUID(0x2A37), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
HR_SERVICE = (HR_UUID, (HR_CHAR,),)

# Uart Nordic
UART_UUID =  bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
UART_RX   = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE,)
UART_TX   = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)

# Uart Microchip
MUART_UUID =  bluetooth.UUID("49535343-FE7D-4AE5-8FA9-9FAFD205E455")
MUART_RX   = (bluetooth.UUID("49535343-8841-43F4-A8D4-ECBE34729BB3"), bluetooth.FLAG_WRITE,)
MUART_TX   = (bluetooth.UUID("49535343-1E4D-4BD9-BA61-23C647249616"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
MUART_SERVICE = (MUART_UUID, (MUART_TX, MUART_RX,),)

# Uart test
TUART_UUID =  bluetooth.UUID("00000001-0000-0000-0000-000000000000")
TUART_RX   = (bluetooth.UUID("00000002-0000-0000-0000-000000000000"), bluetooth.FLAG_WRITE,)
TUART_TX   = (bluetooth.UUID("00000003-0000-0000-0000-000000000000"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
TUART_SERVICE = (TUART_UUID, (TUART_TX, TUART_RX,),)

# Services
#SERVICES = (SIMPLE_SERVICE,)
#SERVICES = (HR_SERVICE, UART_SERVICE, MUART_SERVICE)
#SERVICES = (HR_SERVICE, UART_SERVICE,)
#SERVICES = (HR_SERVICE,)
SERVICES = (UART_SERVICE,)
#SERVICES = (MUART_SERVICE,)
#SERVICES = (TUART_SERVICE,)

handles = ""

ble_msg = ""

def bluetooth_interrupt(event, data):
    print(f"- bluetooth_interrupt(event={event}, data={data})")
    
    if event == 1:
        print("Event 1 - _IRQ_CENTRAL_CONNECT")

    elif event == 2:
        print("Event 2 - _IRQ_CENTRAL_DISCONNECT")
        #advertiser()
        #self.disconnected()
    
    # Phone writes some data to the characteristic
    elif event == 3: #_IRQ_GATTS_WRITE:
        print("Event 3 - _IRQ_GATTS_WRITE")
        buffer = ble.gatts_read(data[1])
        print(f"buffer: {buffer}")
        global ble_msg
        ble_msg = buffer.decode('UTF-8').strip()
        print(f"ble_msg: {ble_msg}")
        
    elif event == 4:
        print("Event 4 - _IRQ_GATTS_READ_REQUEST")
        
        
    elif event == 21: # _IRQ_MTU_EXCHANGED
        print("Event 21 - _IRQ_MTU_EXCHANGED")
        pass
    
    elif event == 27: # _IRQ_CONNECTION_UPDATE
        print("Event 27 - _IRQ_CONNECTION_UPDATE")
        pass
    
    else:
        print("other")
            
def register_services():
    print("register_services")
    global handles
    handles = ble.gatts_register_services(SERVICES)

def advertiser():
    print("advertiser()")
    name = bytes(DEVICE_NAME, 'UTF-8')
    adv_data = bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
    ble.gap_advertise(100, adv_data)
    print(adv_data)

def init():
    global ble
    ble = bluetooth.BLE()
    ble.active(True)
    ble.irq(bluetooth_interrupt)
    register_services()
    advertiser()
    
init()
print(handles)