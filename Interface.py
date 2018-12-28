import tkinter as tk
import tkinter,tkinter.filedialog
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import ImageTk, Image

import os

filePath=""

root = tk.Tk()
root.title("IMAGE COMPRESSION")
root.geometry("840x960")
root.configure(background='white')

canvas = Canvas(root, width = 400, height = 200)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("ICON.png"))  
canvas.create_image(20, 20, anchor=NW, image=img)  
#---------------Choose file

def callback():
    global w
    root.filename = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    w.configure(text = root.filename)
    filePath = root.filename
    
    before = Image.open(root.filename)
    bardejov = ImageTk.PhotoImage(before)
    label1 = Label(root,width= 300, heigh= 300, image=bardejov)
    label1.image = bardejov
    label1.place(x=20, y=380)

    T1 = Label(root, text= "Image",font=("Helvetica", 15))
    T1.pack()
    T1.place(x=150, y=340)
    # T2 = Label(root, text= "After",font=("Helvetica", 20))
    # T2.pack()
    # T2.place(x=650, y=340)

    # after = Image.open(root.filename)
    # rotunda = ImageTk.PhotoImage(after)
    # label2 = Label(root,width= 300, heigh= 300, image=rotunda)
    # label2.image = rotunda
    # label2.place(x=520, y=380)        


w = Label(root, text= "UNKNOWN FILE", bg="black", fg="white")
w.pack(fill=X,padx=10)


b = Button(root, text="Browse file", command=callback)
b.pack()

#------------checkbox
v = tk.IntVar()
v.set(0)  # initializing the choice, i.e. Python

languages = [
    ("RunLenght"),
    ("ShannonFano"),
    ("Huffman"),
]

def ShowChoice():
    print(v.get())


for val, language in enumerate(languages):
    Rad= tk.Radiobutton(root, 
                  text=language,
                  padx = 20, 
                  variable=v, 
                  command=ShowChoice,
                  value=val).pack(anchor=tk.W)

#inputFile = os.path(Text)



#COMPRESSBTN
def Compress():
    window = tk.Toplevel(root)
    if v.get()== 0:
        pass
    elif v.get()== 1:
        pass
    else:
        pass

btn = Button(root, text="Compress", command=Compress)
btn.pack()




# T1 = Label(root, text= "Before",font=("Helvetica", 28))
# T1.pack()
# T1.place(x=150, y=340)
# T2 = Label(root, text= "After",font=("Helvetica", 28))
# T2.pack()
# T2.place(x=650, y=340)

# before = Image.open(callback())
# bardejov = ImageTk.PhotoImage(before)
# label1 = Label(root,width= 300, heigh= 300, image=bardejov)
# label1.image = bardejov
# label1.place(x=20, y=380)


# after = Image.open(callback())
# rotunda = ImageTk.PhotoImage(after)
# label2 = Label(root,width= 300, heigh= 300, image=rotunda)
# label2.image = rotunda
# label2.place(x=520, y=380)        


root.mainloop()