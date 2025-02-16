import micropython
import time

def test(arg):
    print(f"{__name__}")
    print(f"C {time.ticks_us()}, arg={arg}")
    
def main():
    print(f"{__name__}")
    print(f"A {time.ticks_us()}")
    print(f"B {time.ticks_us()}")
    micropython.schedule(test, None)
    print(f"D {time.ticks_us()}")
    print(f"E {time.ticks_us()}")

main()