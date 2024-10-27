import network
import ntptime
import time

ssid = "Extronic2.4"
password = "LeonInstruments"

def wifi_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Łączenie z siecią", end="")
        station.connect(ssid, password)
        while not station.isconnected():
            print(".", end="")
            time.sleep_ms(250)
        print()    
    
    print(f"Adres IP: {station.ifconfig()[0]}")
    
def download_time():
    ntptime.settime()

def print_system_time():
    time_tuple = time.localtime()
    year    = time_tuple[0]
    month   = time_tuple[1]
    day     = time_tuple[2]
    hours   = time_tuple[3]
    minutes = time_tuple[4]
    seconds = time_tuple[5]
    weekday = time_tuple[6]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print(f"{year}.{month:02}.{day:02} {hours:02}:{minutes:02}:{seconds:02} {days[weekday]}")
        
if __name__ == "__main__":    
    print("Czas przed synchronizacją: ", end="")
    print_system_time()
    wifi_connect()
    download_time()
    print("Czas po synchronizacji:    ", end="")
    print_system_time()