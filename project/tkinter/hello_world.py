import tkinter

def demo_button_cb():
    print("Hello!")

root = tkinter.Tk()
root.geometry("800x600")

hello_label = tkinter.Label(root, text="Hello world!")
hello_label.pack()

demo_button1 = tkinter.Button(root, text="Click me 1", command=demo_button_cb)
demo_button1.pack()

demo_button2 = tkinter.Button(root, text="Click me 2", command=demo_button_cb, width=10, height=5)
demo_button2.place(x=100, y=100)

demo_button3 = tkinter.Button(root, text="Click me 3", command=demo_button_cb)
demo_button3.place(x=600, y=100, width=100, height=50)

root.mainloop()

print("After main loop")