import tkinter

class Root(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("800x600")
        
        self.hello_label = tkinter.Label(self, text="Hello world")
        self.hello_label.pack()
        
        self.demo_button1 = tkinter.Button(self, text="Click me 1", command=self.demo_button_cb)
        self.demo_button1.pack()
        
        self.demo_button2 = tkinter.Button(self, text="Click me 2", command=self.demo_button_cb, width=10, height=5)
        self.demo_button2.place(x=100, y=100)

        self.demo_button3 = tkinter.Button(self, text="Click me 3", command=self.demo_button_cb)
        self.demo_button3.place(x=600, y=100, width=100, height=50)
        
    def demo_button_cb(self):
        print("Hello!")
        

root = Root()
root.mainloop()

print("After main loop")
