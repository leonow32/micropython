import json

data = {}

def read_json():
    try:
        with open("test.json") as file:
            global data
            data = json.load(file)
    except:
        print("Plik test.json nie istnieje")

def save_json():
    with open("test.json", "w") as file:
        json.dump(data, file, separators=(",\n", ":"))
        
if __name__ == "__main__":
    read_json()
   
    key   = input("Podaj nazwę nowego klucza: ")
    value = input("Podaj wartość nowego klucza: ")
    data[key] = value
    
    for key, value in data.items():
        print(f"{key}:\t\t{value}")
    
    save_json()
    
    