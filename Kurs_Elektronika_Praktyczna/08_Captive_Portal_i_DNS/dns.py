# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM
# Dekoder zapytań pochodzi z https://github.com/anson-vandoren/esp8266-captive-portal/blob/master/captive_dns.py

import _thread
import socket
import gc
import sys
import time
import wifi_ap

def decode_request(request):
    domain = ""
    head   = 12
    length = request[head]
    
    while length != 0:
        label = head + 1
        # add the label to the requested domain and insert a dot after
        domain += request[label:label+length].decode("utf-8") + "."
        # check if there is another label after this one
        head += length + 1
        length = request[head]
    
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
    local_ip = wifi_ap.get_ip()
    packet += bytes(map(int, local_ip.split(".")))
    
    return packet, domain

def task():
    #global local_ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 53))
    #sock.setblocking(False)
    
    while True:
        try:
            gc.collect()
            data, addr = sock.recvfrom(1024)
            response, domain = decode_request(data)
            sock.sendto(response, addr)
            print(f"DNS  - from {addr[0]} request {domain}, response is {wifi_ap.get_ip()}")
        except Exception as e:
            #sys.print_exception(e)
            time.sleep_ms(100)

def init():
    _thread.start_new_thread(task, ())

if __name__ == "__main__":
    init()
