# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

def read_file_all():
    with open("plik.txt") as file:
        content = file.read()       # string
    print(content)

def read_file_lines():
    with open("plik.txt") as file:
        lines = file.readlines()    # list of strings
    
    for line in lines:
        print(line)
        
def save_file():
    with open("plik.txt", "a") as file:
        file.write("Pierwsza linia\n")
        file.write("Druga linia\n")
        file.write("Trzecia linia\n")
        
if __name__ == "__main__":
    save_file()
#   read_file_lines()
    read_file_all()