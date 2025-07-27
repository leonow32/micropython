import tkinter as tk
from tkinter import ttk 
from PIL import Image
from PIL import ImageTk

# Zmienne globalne
Root = tk.Tk()
ActualImageNumber = 0
ImageList = []
Text1 = tk.StringVar(Root)
StatusBarText = tk.StringVar(Root)
RadioButtonVar = tk.IntVar()
RadioButtonVar.set(0)

# Zmiana obrazka
def ChangeImage(NewImageNumber):
    print("ChangeImage(" + str(NewImageNumber) + ")")
    
    # Kontrola poprawności
    if NewImageNumber < 0:
        print("<0")
        return

    if NewImageNumber >= len(ImageList):
        print(">=len(ImageList)=" + str(len(ImageList)))
        return
    
    # Zmiana obrazka
    global ActualImageNumber
    global ImageLabel
    ImageLabel.grid_forget()
    ImageLabel = tk.Label(image=ImageList[NewImageNumber])
    ImageLabel.grid(row=0, column=0, columnspan=3)
    ActualImageNumber = NewImageNumber

    # Włączanie/wyłączanie przycisków przewijania
    if(ActualImageNumber == len(ImageList)-1):
        ButtonNext.config(state=tk.DISABLED)
        ButtonNextTTK.state(["disabled"])
    else:
        ButtonNext.config(state=tk.ACTIVE)
        ButtonNextTTK.state(["!disabled"])
    
    if(ActualImageNumber == 0):
        ButtonPrev.config(state=tk.DISABLED)
        ButtonPrevTTK.state(["disabled"])
    else:
        ButtonPrev.config(state=tk.ACTIVE)
        ButtonPrevTTK.state(["!disabled"])

    # Aktualizacja statusu
    global StatusBarText
    StatusBarText.set("Image {} / {}".format(ActualImageNumber+1, len(ImageList)))

    #Aktualizacja zmiennej dla radio buttonów
    RadioButtonVar.set(ActualImageNumber)

# Okna główne
Root.title("Image viewer")
Root.iconbitmap("atom128.ico")

# Obrazki
#Image0 = ImageTk.PhotoImage(Image.open("images/0.png"))
#Image1 = ImageTk.PhotoImage(Image.open("images/1.png"))
#Image2 = ImageTk.PhotoImage(Image.open("images/2.png"))
#Image3 = ImageTk.PhotoImage(Image.open("images/3.png"))
#Image4 = ImageTk.PhotoImage(Image.open("images/4.png"))

# Lista obrazków - wersja 1
#ImageList = [Image0, Image1, Image2, Image3, Image4]

# Lista obrazków - wersja 2
#ImageList.append(Image0)
#ImageList.append(Image1)
#ImageList.append(Image2)
#ImageList.append(Image3)
#ImageList.append(Image4)

# Lista obrazków - wersja 3
#ImageList += [Image0]
#ImageList += [Image1]
#ImageList += [Image2]
#ImageList += [Image3]
#ImageList += [Image4]

# Lista obrazów - wersja 4
for i in range(5):
    print(i)
    ImageList.append(ImageTk.PhotoImage(Image.open(str(i) + ".png")))

# Umieszczenie pierwszego obrazka
ImageLabel = tk.Label(image=ImageList[0])
ImageLabel.grid(row=0, column=0, columnspan=3)

# Tekst w pasku stanu
StatusBarText.set("Image 1 / " + str(len(ImageList)))

# Przyciski (tk)
ButtonExit = tk.Button(Root, text="Exit", command=Root.quit)
ButtonNext = tk.Button(Root, text=">", command=lambda: ChangeImage(ActualImageNumber+1))
ButtonPrev = tk.Button(Root, text="<", command=lambda: ChangeImage(ActualImageNumber-1), state=tk.DISABLED)
ButtonPrev.grid(row=1, column=0)
ButtonExit.grid(row=1, column=1)
ButtonNext.grid(row=1, column=2)

# Przyciski (ttk)
ButtonExitTTK = ttk.Button(Root, text="Exit", command=Root.quit)
ButtonNextTTK = ttk.Button(Root, text=">", command=lambda: ChangeImage(ActualImageNumber+1))
ButtonPrevTTK = ttk.Button(Root, text="<", command=lambda: ChangeImage(ActualImageNumber-1), state=["disabled"])
ButtonPrevTTK.grid(row=2, column=0)
ButtonExitTTK.grid(row=2, column=1)
ButtonNextTTK.grid(row=2, column=2)

# Status bar
StatusBar = tk.Label(Root, textvariable=StatusBarText, bd=1, relief=tk.SUNKEN, anchor=tk.E)
StatusBar.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E)

# Ramka 1 - radiobuttony dodawane pojedynczo
Frame1 = tk.LabelFrame(Root, text="Radio Buttony 1")
Frame1.grid(row=0, column=3, sticky=tk.N)

tk.Radiobutton(Frame1, text="Foto 1", value=0, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
tk.Radiobutton(Frame1, text="Foto 2", value=1, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
tk.Radiobutton(Frame1, text="Foto 3", value=2, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
tk.Radiobutton(Frame1, text="Foto 4", value=3, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
tk.Radiobutton(Frame1, text="Foto 5", value=4, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
TestLabel1 = tk.Label(Frame1, textvariable=RadioButtonVar).pack()

# Ramka 2 - radiobuttony dodawane poprzez listę
Frame2 = tk.LabelFrame(Root, text="Radio Buttony 2")
Frame2.grid(row=0, column=4, sticky=tk.N)
RadioButtonList = [
    ("Image 1", 0),
    ("Image 2", 1),
    ("Image 3", 2),
    ("Image 4", 3),
    ("Image 5", 4),
]
for (Txt, Val) in RadioButtonList:
    tk.Radiobutton(Frame2, text=Txt, value=Val, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)

TestLabel2 = tk.Label(Frame2, textvariable=RadioButtonVar).pack()

# Ramka 3 - radiobuttony z TTK dodawane pojedynczo
Frame3 = ttk.LabelFrame(Root, text="Radio Buttony TTK")
Frame3.grid(row=0, column=5, sticky=tk.N)

ttk.Radiobutton(Frame3, text="Foto 1", value=0, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
ttk.Radiobutton(Frame3, text="Foto 2", value=1, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
ttk.Radiobutton(Frame3, text="Foto 3", value=2, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
ttk.Radiobutton(Frame3, text="Foto 4", value=3, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)
ttk.Radiobutton(Frame3, text="Foto 5", value=4, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)

# Ramka 4 - radiobuttony z TTK dodawane przez listę
Frame4 = ttk.LabelFrame(Root, text="Radio Buttony TTK")
Frame4.grid(row=0, column=6, sticky=tk.N)

for (Txt, Val) in RadioButtonList:
    ttk.Radiobutton(Frame4, text=Txt, value=Val, variable=RadioButtonVar, command=lambda: ChangeImage(RadioButtonVar.get())).pack(anchor=tk.W)


# Main loop    
Root.mainloop() 


