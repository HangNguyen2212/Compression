import tkinter as tk
import tkinter,tkinter.filedialog
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import ImageTk, Image
import os,ntpath
from pathlib import Path
from rle import main as RLEmain
from shannon import main as SHANNONmain
from lzw import main as LZWmain
from huffman import main as HUFFmain

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
    label1.place(x=20, y=390)
    label2 = Label(root,width= 300, heigh= 300)
    label2.place(x=520, y=390)
    
    T1 = Label(root, text= 'Before',font=("Helvetica", 15))
    T1.pack()
    T1.place(x=150, y=340)  
    T1_size = Label(root, text= dimensions,font=("Helvetica", 10))
    T1_size.pack()
    T1_size.place(x=150, y=360)     


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
    ("LZW"),
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
def getSize(filename):
    st = os.stat(filename)
    return st.st_size



compressed=0
#COMPRESSBTN
def Compress():
    global label2
    T2 = Label(root, text= "After",font=("Helvetica", 15))
    T2.pack()
    T2.place(x=620, y=340)   
    
     
    if v.get()== 0:
        RLEmain(image_file,encode_file,decode_file)
    elif v.get()== 1:
        SHANNONmain(image_file,encode_file,decode_file)
    elif v.get()== 2:
        HUFFmain(image_file,encode_file,decode_file)
    else:
        LZWmain(image_file,encode_file,decode_file)

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
    label2.place(x=520, y=390)
    T1_size = Label(root, text= dimensions_after,font=("Helvetica", 10))
    T1_size.pack()
    T1_size.place(x=620, y=360) 
    
    show_encode = tk.Button(root, text="img_encode.txt", command=lambda:OnClick())
    show_encode.pack()
    show_encode.place(x=360,y=600)

def OnClick():
    # window = tk.Toplevel(root)
    # window.geometry("300x500")
    # window.configure(background='white')
    # window.title ="img_encode"
    with open('img_encode.txt') as infp:
        txt = infp.read()
    # results= Label(window, text= data, bg="white", fg="black")
    # results.pack(fill=X,padx=10)
    top = tk.Toplevel()
    top.title("FILE ENCODE")
    about_message = (txt)
    top.lift()
    msg = tk.Text(top, width=50, font=('courier', 15, 'normal'))
    msg.grid(stick=tk.N, padx=(10,10), pady=(10,10))
    msg.insert("1.0", about_message)
    button = tk.Button(top, height=1, width=20, text="Dismiss", command=top.destroy, bg='gray97', relief=tk.GROOVE)
    button.grid(sticky=tk.S, pady=(0,10))
    s = tk.Scrollbar(top, width=20)
    s.grid(row=0, column=0, sticky=tk.E+tk.N+tk.S, padx=(0,10),pady=(10,10))
    s['command'] = msg.yview
    msg['yscrollcommand'] = s.set
    top.resizable(width=tk.FALSE, height=tk.FALSE) 

btn = Button(root, text="Compress", command=Compress)
btn.pack()


root.mainloop()