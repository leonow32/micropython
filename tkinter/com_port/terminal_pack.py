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
        self.port_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.X)
        
        self.scan_button = ttk.Button(self.port_frame, text="Skanuj", command=self.scan_button_cb)
        self.scan_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.combo = ttk.Combobox(self.port_frame, values=self.com_port_list, width=50)
        self.combo.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.open_close_button = ttk.Button(self.port_frame, text="Otwórz", command=self.open_close_button_cb)
        self.open_close_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        # Ramka Terminal
        self.terminal_frame = ttk.LabelFrame(self, text="Terminal")
        self.terminal_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        # Ramka Terminal 1
        self.terminal_frame_row1 = ttk.Frame(self.terminal_frame)
        self.terminal_frame_row1.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.terminal_entry = ttk.Entry(self.terminal_frame_row1)
        self.terminal_entry.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.send_button = ttk.Button(self.terminal_frame_row1, text="Wyślij", command=self.send_button_cb)
        self.send_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.read_button = ttk.Button(self.terminal_frame_row1, text="Odbierz", command=self.read_button_cb)
        self.read_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.clear_button = ttk.Button(self.terminal_frame_row1, text="Wyczyść", command=self.clear_button_cb)
        self.clear_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        # Ramka Terminal 2
        self.terminal_frame_row2 = ttk.Frame(self.terminal_frame)
        self.terminal_frame_row2.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.monitor = scrolledtext.ScrolledText(self.terminal_frame_row2, height=8, font=("Lucida Console", 15))
        self.monitor.pack(side=tk.LEFT, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.make_buttons_inactive()
        
        # Ramka Obraz
        self.image_frame = ttk.LabelFrame(self, text="Obraz")
        self.image_frame.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.X, expand=True)
        
        self.image_frame_row1 = ttk.Frame(self.image_frame)
        self.image_frame_row1.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
        self.zoom_label = ttk.Label(self.image_frame_row1, text="Zoom:")
        self.zoom_label.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.zoom_combo = ttk.Combobox(self.image_frame_row1, values=["1x", "2x", "3x", "4x"])
        self.zoom_combo.bind("<<ComboboxSelected>>", self.zoom_combo_cb)
        self.zoom_combo.set("1x")
        self.zoom_combo.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.download_button = ttk.Button(self.image_frame_row1, text="Pobierz")
        self.download_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.save_button = ttk.Button(self.image_frame_row1, text="Zapisz")
        self.save_button.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
        self.image_frame_row2 = ttk.Frame(self.image_frame)
        self.image_frame_row2.pack(side=tk.TOP, padx=_padx, pady=_pady, fill=tk.BOTH, expand=True)
        
#         self.my_image = ImageTk.PhotoImage(Image.open("yellow.png"))
        self.image_obj = Image.open("yellow.png")
        self.image_obj[0] = 0
        print(self.image_obj)
        self.my_image = ImageTk.PhotoImage(self.image_obj)
        self.image_label = tk.Label(self.image_frame_row2, image=self.my_image)
        self.image_label.pack(side=tk.LEFT, padx=_padx, pady=_pady)
        
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