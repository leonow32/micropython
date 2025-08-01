import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import serial.tools.list_ports as list_ports
import serial

_padx = 10
_pady = 5

class MainWindow(tk.Tk):

    def __init__(self):
        self.com_port_list = []
        
        super().__init__()
        self.title("Skaner portów COM")
        
        self.port_frame = ttk.LabelFrame(self, text="Port COM")
        self.port_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.X)
        
        self.scan_button = ttk.Button(self.port_frame, text="Skanuj", command=self.scan_button_cb)
        self.scan_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.listbox = ttk.Combobox(self.port_frame, values=self.com_port_list, width=50)
        self.listbox.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.open_close_button = ttk.Button(self.port_frame, text="Otwórz", command=self.open_close_button_cb)
        self.open_close_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.image_frame = ttk.LabelFrame(self, text="Obraz")
        self.image_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.send = ttk.Button(self.image_frame, text="Send", command=self.send_button_cb)
        self.send.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.read = ttk.Button(self.image_frame, text="Read", command=self.read_button_cb)
        self.read.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
    def scan_button_cb(self):
        print("scan_button_cb")
        self.com_port_list.clear()
        self.com_port_list = list(list_ports.comports())
        self.listbox.configure(values=self.com_port_list)
        
    def open_close_button_cb(self):
        print("open_close_button_cb")
        port  = self.listbox.get()
        if port == "":
            messagebox.showerror("Błąd", "Nie wybrałeś żadnego portu")
        else:
            messagebox.showinfo("Informacja", f"Wybrałeś port {port}")
            
        self.port = serial.Serial("COM1", 115200, timeout=0)
        
    def send_button_cb(self):
        self.port.write(b'print("Hello world")\r\n')
    
    def read_button_cb(self):
        while True:
            buf = self.port.read()
            if buf == b'':
                break
            buf = buf.decode("utf-8")
            print(buf, end="")

main_window = MainWindow()
main_window.mainloop()

print("Program closed")