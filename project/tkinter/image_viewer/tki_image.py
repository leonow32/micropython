import tkinter as tk
import tkinter.messagebox as tkmb
from PIL import Image
from PIL import ImageTk


# Okna główne
Root = tk.Tk()
Root.title("Image viewer")
Root.iconbitmap("atom128.ico")

# Obrazek
MyImage = ImageTk.PhotoImage(Image.open("atom128.png"))
MyLabel = tk.Label(image=MyImage)
MyLabel.pack()

# Przycisk Exit
ButtonExit = tk.Button(Root, text="Exit", command=Root.quit)
ButtonExit.pack()



# Main loop    
Root.mainloop() 



