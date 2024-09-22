from json import dump, load

conf = dict()

def init():
    default_config = {
        "name": "Socket GEN4 HV2",
        "mode": "ap",
        "ssid": "",
        "password": "",
        "pin-sda": 18,
        "pin-scl": 19,
        "pin-relay": 10,
        "pin-button": 3,
        "pin-red": 0,
        "pin-grn": 0,
        "pin-tx": 4,
        "pin-rx": 5,
        "pin-ws2812": 7,
        "led-type": "ws2812",
        "led-inverted": False,
        "hlw-v": 9977,
        "hlw-i": 337915,
        "hlw-p": 102203,
    }
    
    global conf

    try:
        with open("app/config.json") as file:
            print("Config file present")
            conf = load(file)
            print("Config loading completed")
    except:
        print("Creating default config file")
        conf = default_config
        save()

def save():
    print("config.save()")
    with open("app/config.json", "w") as file:
        dump(conf, file, separators=(",\x0A", ":"))
        
def set(param, value):
    print(f"config.set({param}, {value})")
    conf[param] = value
    
def get(item):
    return conf[item]

if __name__ == "__main__":
    init()
