import json

data = {}

def read_json():
    try:
        with open("test.json") as file:
            global data
            data = json.load(file)
    except:
        print("File test.json doesn't exist")

def save_json():
    with open("test.json", "w") as file:
        json.dump(data, file, separators=(",\x0A", ":"))
        
if __name__ == "__main__":
    read_json()
    
    key = input("Type key: ")
    value = input("Type value: ")
    data[key] = value
    
    for key, value in data.items():
        print(f"{key}:\t\t{value}")
    
    save_json()
    
    