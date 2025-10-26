import time

start_time = 0

def begin():
    global start_time
    start_time = time.ticks_us()
    
def end(message):
    elapsed_time = time.ticks_us() - start_time
    print(f"{message} {elapsed_time} us")
