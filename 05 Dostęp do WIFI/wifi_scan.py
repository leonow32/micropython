import network
station = network.WLAN(network.STA_IF)
station.active(True)
nets = station.scan()

counter = 0
authmodes = ["Open", "WEP", "WPA", "WPA2", "WPA/WPA2", "WPA2-Ent", "WPA3", "WPA2/WPA3", "WAPI", "OWE"]

print("Nr | Channel | RSSI | Security  | Hidden | SSID")
for net in nets:
    print(f"{counter:2d} | {net[2]:7d} | {net[3]:4d} | {authmodes[net[4]]:9s} | {net[5]:6d} | {net[0]:s}")
    counter = counter + 1
