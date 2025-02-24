import time
import machine

def print_system_time():
    Y, M, D, h, m, s, w, _ = time.localtime()
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piatek", "Sobota", "Niedziela"]
    print(f"{Y}.{M:02}.{D:02} {h:02}:{m:02}:{s:02} {days[w]}")

def set_system_time(time_tuple):
    """
    time_tuple: (year, month, day, hours, minutes, seconds, 0, 0)
    """
    
    Y, M, D, h, m, s, _, _ = time_tuple
    new_time_tuple = (Y, M, D, 0, h, m, s, 0)
    rtc = machine.RTC()
    rtc.datetime(new_time_tuple)

print_system_time()
set_system_time((2025, 12, 24, 12, 34, 56, 0, 0))
print_system_time()
