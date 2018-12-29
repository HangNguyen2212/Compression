import tkinter as tk
import tkinter,tkinter.filedialog
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import ImageTk, Image
from rle import main as RLEmain
import os
import ntpath
from pathlib import Path
global image_file 
root = tk.Tk()
root.title("IMAGE COMPRESSION")
root.geometry("840x960")
root.configure(background='white')

canvas = Canvas(root, width = 400, height = 200)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("ICON.png"))  
canvas.create_image(20, 20, anchor=NW, image=img)  

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail 
#---------------Choose file
name=StringVar()

def callback():
    global w
    root.filename = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    w.configure(text = root.filename)
    
    photo = Image.open(root.filename)
    photo.save('input_image.jpg')

    basewidth_1 = 300
    img_1 = Image.open(root.filename)
    width_before, height_before = img_1.size
    dimensions = "%dx%d" % (width_before, height_before)
    wpercent = (basewidth_1 / float(img_1.size[0]))
    hsize = int((float(img_1.size[1]) * float(wpercent)))
    img_1 = img_1.resize((basewidth_1, hsize), Image.ANTIALIAS)
    img_1.save('resized_image.jpg')
    #resize img to fit label
    before = Image.open('resized_image.jpg','r')
    bardejov = ImageTk.PhotoImage(before)
    label1 = Label(root,width= 300, heigh= 300, image=bardejov)
    label1.image = bardejov
    label1.place(x=20, y=380)

    
    T1 = Label(root, text= 'Before',font=("Helvetica", 15))
    T1.pack()
    T1.place(x=150, y=330)  
    T1_size = Label(root, text= dimensions,font=("Helvetica", 10))
    T1_size.pack()
    T1_size.place(x=150, y=350)     


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

image_file = 'input_image.jpg'
encode_file = 'img_encode.txt'
decode_file = 'img_decode.jpg'

#def

#COMPRESSBTN
def Compress():

    T2 = Label(root, text= "After",font=("Helvetica", 15))
    T2.pack()
    T2.place(x=620, y=330)   
    
     
    if v.get()== 0:
        RLEmain(image_file,encode_file,decode_file)
        
        basewidth_2 = 300
        img_2 = Image.open('img_decode.jpg','r')
        width_after, height_after = img_2.size
        dimensions_after = "%dx%d" % (width_after, height_after)
        wpercent = (basewidth_2 / float(img_2.size[0]))
        hsize = int((float(img_2.size[1]) * float(wpercent)))
        img_2 = img_2.resize((basewidth_2, hsize), Image.ANTIALIAS)
        img_2.save('resized_decode_image.jpg')
        #resize img to fit label
        after = Image.open('resized_decode_image.jpg','r')
        rotunda = ImageTk.PhotoImage(after)
        label2 = Label(root,width= 300, heigh= 300, image=rotunda)
        label2.image = rotunda
        label2.place(x=520, y=380)

        T1_size = Label(root, text= dimensions_after,font=("Helvetica", 10))
        T1_size.pack()
        T1_size.place(x=620, y=350) 
    elif v.get()== 1:
        pass
    else:
        pass

btn = Button(root, text="Compress", command=Compress)
btn.pack()

root.mainloop()