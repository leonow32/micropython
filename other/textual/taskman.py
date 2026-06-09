import time
import threading
import traceback

# Task run modes
RUN         = 0
CONSTRUCTOR = 1
DESTRUCTOR  = 2

# Task list items
FUNC     = 0
PERIOD   = 1
NEXT_RUN = 2

tasks = [[None, 0, 0], [None, 0, 0], [None, 0, 0], [None, 0, 0], [None, 0, 0]] # each task is [task, period, next_run_time]

log_enable = True

def log(message):
    if log_enable:
        print(f"{time.strftime('%Y.%m.%d %H:%M:%S')} {message}")

def get_used_slot(func):
    for slot, task in enumerate(tasks):
        if task[FUNC] == func:
            return slot
        
    return -1

def get_free_slot():
    for slot, task in enumerate(tasks):
        if task[FUNC] is None:
            return slot
    return -1

def is_running(task):
    return get_used_slot(task) >= 0

def add(task, period):
    slot = get_free_slot()
    if slot == -1:
        log(f"add {task} period {period} - no free slots")
        return
        
    if is_running(task):
        log(f"add {task} period {period} - already added")
        return
        
    log(f"add {task} period {period} - slot {slot}")
    tasks[slot][FUNC]     = task
    tasks[slot][PERIOD]   = period
    tasks[slot][NEXT_RUN] = period+time.monotonic()
    
    task(CONSTRUCTOR)
        
def close(task):
    slot = get_used_slot(task)
    
    if slot == -1:
        log(f"close {task} - not found")
        return
    
    log(f"close {task} - slot {slot}")
    tasks[slot][FUNC]     = None
    tasks[slot][PERIOD]   = 0
    tasks[slot][NEXT_RUN] = 0
    task(DESTRUCTOR)

def scheduler():
    try:
        while True:
            time.sleep(0.001)
            for task in tasks:
                if task[FUNC] and time.monotonic() >= task[NEXT_RUN]:
                    task[NEXT_RUN] += task[PERIOD]
                    task[FUNC](RUN)
    except:
        traceback.print_exc()
        
        for task in tasks:
            if task[FUNC]:
                close(task[FUNC])
        
def run_as_thread():
    threading.Thread(target=scheduler).start()

def monitor():
    print("Id\tPeriod\tNext\tFunction")
    for i, task in enumerate(tasks):
        print(f"{i}\t{task[PERIOD]}\t{task[NEXT_RUN]:.0f}\t{task[FUNC]}")

if __name__ == "__main__":
    
    def task_a(run_mode):
        if run_mode == RUN:
            global a
            log(f"task_a run {a}")
            a += 1
        elif run_mode == CONSTRUCTOR:
            log("task_a constructor")
            a = 0        
        elif run_mode == DESTRUCTOR:
            log("task_a destructor")
            del a

    def task_b(run_mode):
        if run_mode == RUN:
            global b
            log(f"task_b run {b}")
            b += 1
            
            if b == 5:
                close(task_c)
                
            if b == 10:
                add(task_c, 1)
                
        elif run_mode == CONSTRUCTOR:
            log("task_b constructor")
            b = 0        
        elif run_mode == DESTRUCTOR:
            log("task_b destructor")
            del b

    def task_c(run_mode):
        if run_mode == RUN:
            global c
            log(f"task_c run {c}")
            c += 1
        elif run_mode == CONSTRUCTOR:
            log("task_c constructor")
            c = 0        
        elif run_mode == DESTRUCTOR:
            log("task_c destructor")
            del c

    add(task_a, 1)
    add(task_b, 1)
    add(task_c, 1)
    monitor()
    
    scheduler()
#     run_as_thread()
    monitor()
