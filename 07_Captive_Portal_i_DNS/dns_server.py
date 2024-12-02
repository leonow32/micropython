import _thread

import gc
import network
import socket
import time

def ap_start(ssid, ip):
    #global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
        
    
    
    # IP address, netmask, gateway, DNS
    ap.ifconfig((ip, "255.255.255.0", ip, ip))
    ap.config(essid=ssid, authmode=network.AUTH_OPEN)
    
    while not ap.active():
        print(".", end="")
        sleep_ms(100)
    
    print(f"Access Point: {ssid} {ap.ifconfig()[0]}")

def decode_request(request):
    domain = ""
    head = 12
    length = request[head]
    
    while length != 0:
        label = head + 1
        # add the label to the requested domain and insert a dot after
        domain += request[label:label+length].decode("utf-8") + "."
        # check if there is another label after this one
        head += length + 1
        length = request[head]
        #print("_", end="")
    
    #print(f"domain: {domain} ", end="")
    
    packet = request[:2]
    # set response flags (assume RD=1 from request)
    packet += b"\x81\x80"
    # copy over QDCOUNT and set ANCOUNT equal
    packet += request[4:6] + request[4:6]
    # set NSCOUNT and ARCOUNT to 0
    packet += b"\x00\x00\x00\x00"

    # ** create the answer body **
    # respond with original domain name question
    packet += request[12:]
    # pointer back to domain name (at byte 12)
    packet += b"\xC0\x0C"
    # set TYPE and CLASS (A record and IN class)
    packet += b"\x00\x01\x00\x01"
    # set TTL to 60sec
    packet += b"\x00\x00\x00\x3C"
    # set response length to 4 bytes (to hold one IPv4 address)
    packet += b"\x00\x04"
    # now actually send the IP address as 4 bytes (without the "."s)
    global ip
    packet += bytes(map(int, ip.split(".")))
    
    return packet, domain

def task():
    print("DNS start")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("",53))
    #sock.listen(5)
    sock.setblocking(False)
    
    while True:
        try:
            print("1", end="")
            gc.collect()
            
            print("2", end="")
            data, addr = sock.recvfrom(1024)
            
            print("3", end="")
            response, domain = decode_request(data)
            
            print("4", end="")
            sock.sendto(response, addr)
            
            print("5", end="")
            print(f"DNS request from {addr[0]}, {domain} -> {ip}")
        except:
            time.sleep_ms(100)

def init():
    print("DNS init")
    _thread.start_new_thread(task, ())

if __name__ == "__main__":
    ap_start("TESTOWY", "192.168.4.1")
    init()
    

