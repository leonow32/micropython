import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image
from PIL import ImageTk
import serial.tools.list_ports as list_ports
import serial

_padx = 10
_pady = 5

class MainWindow(tk.Tk):

    def __init__(self):
        self.com_port_list = []
        self.com_port_opened = False
        
        super().__init__()
        self.title("Skaner portów COM")
        
        # Ramka Port COM
        self.port_frame = ttk.LabelFrame(self, text="Port COM")
        self.port_frame.grid(row=0, column=0, padx=_padx, pady=_pady, sticky="WE")
#         self.port_frame.grid_columnconfigure(0, weight=1)
#         self.port_frame.grid_columnconfigure(1, weight=2)
#         self.port_frame.grid_columnconfigure(2, weight=1)
#         self.port_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.X)
        
        self.scan_button = ttk.Button(self.port_frame, text="Skanuj", command=self.scan_button_cb)
        self.scan_button.grid(row=0, column=0, padx=_padx, pady=_pady, sticky="we")
#         self.scan_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.combo = ttk.Combobox(self.port_frame, values=self.com_port_list)
        self.combo.grid(row=0, column=1, padx=_padx, pady=_pady, sticky="we", columnspan=2)
#         self.combo.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.open_close_button = ttk.Button(self.port_frame, text="Otwórz", command=self.open_close_button_cb)
        self.open_close_button.grid(row=0, column=3, padx=_padx, pady=_pady, sticky="we")
#         self.open_close_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        # Ramka Terminal
        self.terminal_frame = ttk.LabelFrame(self, text="Terminal")
        self.terminal_frame.grid(row=1, column=0, padx=_padx, pady=_pady, sticky="we")
#         self.terminal_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.terminal_entry = ttk.Entry(self.terminal_frame)
        self.terminal_entry.grid(row=0, column=0, padx=_padx, pady=_pady, sticky="we")
#         self.terminal_entry.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.send_button = ttk.Button(self.terminal_frame, text="Wyślij", command=self.send_button_cb)
        self.send_button.grid(row=0, column=1, padx=_padx, pady=_pady, sticky="we")
#         self.send_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.read_button = ttk.Button(self.terminal_frame, text="Odbierz", command=self.read_button_cb)
        self.read_button.grid(row=0, column=2, padx=_padx, pady=_pady, sticky="we")
#         self.read_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.clear_button = ttk.Button(self.terminal_frame, text="Wyczyść", command=self.clear_button_cb)
        self.clear_button.grid(row=0, column=3, padx=_padx, pady=_pady, sticky="we")
#         self.clear_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.monitor = scrolledtext.ScrolledText(self.terminal_frame, height=8, font=("Lucida Console", 15))
        self.monitor.grid(row=1, column=0, columnspan=4, padx=_padx, pady=_pady, sticky="news")
#         self.monitor.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.make_buttons_inactive()
        
        # Ramka Obraz
        self.image_frame = ttk.LabelFrame(self, text="Obraz")
        self.image_frame.grid(row=2, column=0, padx=_padx, pady=_pady, sticky="we")
        
#         self.image_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.zoom_label = ttk.Label(self.image_frame, text="Zoom:")
        self.zoom_label.grid(row=0, column=0, padx=_padx, pady=_pady)
#         self.zoom_label.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.zoom_combo = ttk.Combobox(self.image_frame, values=["1x", "2x", "3x", "4x"])
        self.zoom_combo.bind("<<ComboboxSelected>>", self.zoom_combo_cb)
        self.zoom_combo.grid(row=0, column=1, padx=_padx, pady=_pady, sticky="news")
        
        self.download_button = ttk.Button(self.image_frame, text="Pobierz")
        self.download_button.grid(row=0, column=2, padx=_padx, pady=_pady)
        
        self.save_button = ttk.Button(self.image_frame, text="Zapisz")
        self.save_button.grid(row=0, column=3, padx=_padx, pady=_pady, sticky="e")
        
        self.scan_button_cb()
        
    def __del__(self):
        print("Destruktor")
        
    def scan_button_cb(self):
        print("scan_button_cb")
        self.com_port_list.clear()
        self.com_port_list = list(list_ports.comports())
        self.combo.configure(values=self.com_port_list)
        
        if len(self.com_port_list) > 0:
            self.combo.set(self.com_port_list[0])
        else:
            self.combo.set("")
        
    def open_close_button_cb(self):
        if self.com_port_opened == False:
            print("Port open")
            port_name  = self.combo.get()
            
            if port_name == "":
                messagebox.showerror("Błąd", "Nie wybrałeś żadnego portu")
            else:
                try:
                    port_name = port_name[0:port_name.find(" ")]
                    self.port = serial.Serial(port_name, 115200, timeout=0)
                
                    self.open_close_button.configure(text="Zamknij")
                    self.make_buttons_active()
                    self.com_port_opened = True
                except Exception as e:
                    messagebox.showerror("Błąd", f"{e}")
            
        else:
            print("Port close")
            self.port.close()
            self.open_close_button.configure(text="Otwórz")
            self.com_port_opened = False
            self.make_buttons_inactive()
        
    def send_button_cb(self):
        data = self.terminal_entry.get() + "\r\n"
        data = bytearray(data, "utf-8")
        self.port.write(data)
    
    def read_button_cb(self):
        while True:
            buf = self.port.read()
            if buf == b'':
                break
            buf = buf.decode("utf-8")
            
            self.monitor.insert(tk.END, buf)
            self.monitor.see(tk.END)
            print(buf, end="")
    
    def clear_button_cb(self):
        self.monitor.delete("1.0", tk.END)
        
    def zoom_combo_cb(self, arg):
        print(f"zoom_combo_cb({arg})")
        value = self.zoom_combo.get()
        print(f"{value}")
            
    def make_buttons_active(self):
        self.send_button.configure(state="!disabled")
        self.read_button.configure(state="!disabled")
        self.terminal_entry.configure(state="!disabled")
        self.monitor.configure(state="normal")
        
        self.scan_button.configure(state="disabled")
        self.combo.configure(state="disabled")
    
    def make_buttons_inactive(self):
        self.send_button.configure(state="disabled")
        self.read_button.configure(state="disabled")
        self.terminal_entry.configure(state="disabled")
        self.monitor.configure(state="disabled")
        
        self.scan_button.configure(state="!disabled")
        self.combo.configure(state="!disabled")

main_window = MainWindow()
main_window.mainloop()

# del main_window
print("Program closed")
