import time
import _thread

# Task run modes
RUN = const(0)
CONSTRUCTOR = const(1)
DESTRUCTOR = const(2)

tasks = {}
"""
key: task_ptr
val: [period_ms, next_run_time]
"""


log_enable = True

def log(message):
    if log:
        print(message)

def add(task_ptr, period_ms): 
    if task_ptr not in tasks:
        log(f"taskman.add(task_ptr={task_ptr}, period_ms={period_ms})")
        tasks[task_ptr] = [period_ms, time.ticks_add(time.ticks_ms(), period_ms)]
        task_ptr(CONSTRUCTOR)
    else:
        log(f"taskman.add(task_ptr={task_ptr}, period_ms={period_ms}) - already added")
        
def close(task_ptr):
    if task_ptr in tasks:
        log(f"taskman.close(task_ptr={task_ptr})")
        del tasks[task_ptr]
        task_ptr(DESTRUCTOR)
    else:
        log(f"taskman.close(task_ptr={task_ptr}) - not found")
        
def scheduler():
#     log(f"taskman.scheduler() - start")
    
    while(True):
        for task_ptr, details in tasks.items():
#             print(f"{time.ticks_ms()} {task_ptr} {details} {time.ticks_diff(time.ticks_ms(), details[1])}")
            if time.ticks_diff(details[1], time.ticks_ms()) <= 0:
                details[1] = time.ticks_add(details[0], details[1])
#                 print(details[1])
                task_ptr(RUN)
#             else:
#                 print(time.ticks_diff(details[1], time.ticks_ms()))
#         print(".")
        time.sleep_ms(1)

def init():
    _thread.start_new_thread(scheduler, ())

if __name__ == "__main__":  
    log("Begin")
    
    def test_task_a(run_mode):
        if run_mode == RUN:
            print(f"{time.ticks_ms()}\t test_task_a RUN")
#             pass
        elif run_mode == CONSTRUCTOR:
            print(f"{time.ticks_ms()}\t test_task_a CONSTRUCTOR")
        elif run_mode == DESTRUCTOR:
            print(f"{time.ticks_ms()}\t test_task_a DESTRUCTOR")
            
    def test_task_b(run_mode):
        if run_mode == RUN:
            print(f"{time.ticks_ms()}\t test_task_b RUN")
        elif run_mode == CONSTRUCTOR:
            print(f"{time.ticks_ms()}\t test_task_b CONSTRUCTOR")
        elif run_mode == DESTRUCTOR:
            print(f"{time.ticks_ms()}\t test_task_b DESTRUCTOR")
            
    add(test_task_a, 1000)
    add(test_task_b, 10000)
    
    init()
        
    
    log("End")