
try:
    with open("/rtc/test1.txt", "w") as f:
        f.write("Some content to write")
except:
    print("Can't save")
