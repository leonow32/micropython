_enabled = True

def debug(caption:str, data: bytes) -> None:
    if _enabled:
        if isinstance(data, int):
            print(f"{caption}: {data:02X}")
            
        elif isinstance(data, bytearray) or isinstance(data, bytes):           
            print(f"{caption}[{len(data)}]: ", end="")
            for byte in data:
                print(f"{byte:02X} ", end="")
            print()
            
        else:
            print(f"{caption}")

def debug_enable() -> None:
    global _enabled
    _enabled = True
    
def debug_disable() -> None:
    global _enabled
    _enabled = False
