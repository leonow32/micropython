import time
import sys
import _thread

# Task run modes
RUN         = const(0)
CONSTRUCTOR = const(1)
DESTRUCTOR  = const(2)

tasks = {}
"""
Contents of task dictionary
key: func
val: [period_ms, next_run_time]
"""

log_enable = True

def log(message):
    if log_enable:
        print(f"{time.ticks_ms()} {message}")

def add(func, period_ms): 
    if func not in tasks:
        log(f"taskman.add(func={func}, period_ms={period_ms})")
        tasks[func] = [period_ms, time.ticks_add(time.ticks_ms(), period_ms)]
        func(CONSTRUCTOR)
    else:
        log(f"taskman.add(func={func}, period_ms={period_ms}) - already added")
        
def close(func):
    if func in tasks:
        log(f"taskman.close(func={func})")
        del tasks[func]
        func(DESTRUCTOR)
    else:
        log(f"taskman.close(func={func}) - not found")
        
def scheduler():   
    while(True):
        time.sleep_ms(1)
        for func, details in tasks.items():
            if time.ticks_diff(details[1], time.ticks_ms()) <= 0:
                details[1] = time.ticks_add(details[0], details[1])
                func(RUN)

def init_loop():
    try:
        scheduler()
    except Exception as e:
#         sys.print_exception(e)
        log("--- Except ---")
        for task in tasks:
            print(task)
            close(task)

def init_thread():
    _thread.start_new_thread(scheduler, ())
    
def monitor():
    for func, details in tasks.items():
        print(f"{func} {details}")

if __name__ == "__main__":  
    log("Begin")
    
    def test_task_a(run_mode):
        if run_mode == RUN:
            global a
            a += 1
            log(f"a run {a}")
            if a == 5:
                close(test_task_b)
            if a == 10:
                add(test_task_b, 1000)
                add(test_task_d, 1000)
        elif run_mode == CONSTRUCTOR:
            log(f"a constructor")
            global a
            a = 0
        elif run_mode == DESTRUCTOR:
            log(f"a destructor")
            
    def test_task_b(run_mode):
        if run_mode == RUN:
            global b
            b += 1
            log(f"b run {b}")
        elif run_mode == CONSTRUCTOR:
            log(f"b constructor")
            global b
            b = 0
        elif run_mode == DESTRUCTOR:
            log(f"b destructor")
            
    def test_task_c(run_mode):
        if run_mode == RUN:
            global c
            c += 1
            log(f"c run {c}")
        elif run_mode == CONSTRUCTOR:
            log(f"c constructor")
            global c
            c = 0
        elif run_mode == DESTRUCTOR:
            log(f"c destructor")
            
    def test_task_d(run_mode):
        if run_mode == RUN:
            global d
            d += 1
            log(f"d run {d}")
        elif run_mode == CONSTRUCTOR:
            log(f"d constructor")
            global d
            d = 0
        elif run_mode == DESTRUCTOR:
            log(f"d destructor")
            
    add(test_task_a, 1000)
    add(test_task_b, 1000)
    add(test_task_c, 1000)
    
    monitor()
    init_loop()
    
    log("End")
    monitor()

