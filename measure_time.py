import time

start_time = 0

def begin():
    global start_time
    start_time = time.ticks_us()
    
def end(message):
    elapsed_time = time.ticks_us() - start_time
    millis = elapsed_time // 1000
    micros = elapsed_time % 1000
    print(f"{message} {millis}.{micros:03} ms")
