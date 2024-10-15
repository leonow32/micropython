from gc import mem_free, mem_alloc
print("WIFI Scanner")

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

networks = sta_if.scan()
count = 0

authmodes = ["Open", "WEP", "WPA-PSK", "WPA2-PSK4", "WPA/WPA2-PSK", "Unknown1", "Unknown2", "Unknown3"]

print("Nr | Channel | RSSI | Security     | Hidden | BSSID             | SSID")
for network in networks:
    print("{:2d} | " .format(count), end="")
    print("{:7d} | " .format(network[2]), end="")
    print("{:4d} | " .format(network[3]), end="")
    #print("{:12d} | ".format(network[4]), end="")
    print("{:12s} | ".format(authmodes[network[4]]), end="")
    print("{:6d} | " .format(network[5]), end="")
    for byte in network[1]:
        print("{:02X} ".format(byte), end="")
    print("| {:32s} ".format(network[0]), end="")
    print("")
    count = count + 1

print(f'RAM used: {mem_alloc()}')