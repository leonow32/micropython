import time

# Task run modes
RUN = const(0)
CONSTRUCTOR = const(1)
DESTRUCTOR = const(2)
ID = const(3)

tasks = []
log_enable = True

def add(task_ptr, period):
    if log_enable:
        print(f"taskman.add(task_ptr={task_ptr}, period={period})")
        
    
        
def close(task_ptr):
    if log_enable:
        print(f"taskman.close(task_ptr={task_ptr})")
        
def scheduler():
    pass

if __name__ == "__main__":
    print("Begin")
    
    print("End")