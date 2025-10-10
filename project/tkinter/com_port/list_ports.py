import serial.tools.list_ports as list_ports

cnt = len(list(list_ports.comports()))
print(f"Found ports: {cnt}")

for p in list_ports.comports():
    print(p)
