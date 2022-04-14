from tkinter import *
from PIL import ImageTk, Image
from math import *

def funct(numimg):
    label.config(image=label.images[numimg])

root= Tk()
row_no = -1
buttons = []
num_of_cols = 3
root.resizable(0, 0)
numfiles = 2

for x in range(0, numfiles):
    if(x % num_of_cols is 0):
        row_no+=1

    buttons.append(Button(root, text = "Button "+str(x), bg = '#4098D3', width = 30,height = 13, command = lambda n=x: funct(n)))
    buttons[x].grid(row = row_no, column = x % num_of_cols)

label = Label(root)
label.grid(row = row_no+1, column = 0, columnspan = num_of_cols)

label.images=[]

for x in range(0, numfiles):
    label.images.append(PhotoImage(file="image"+str(x)+".png"))

gauge_img=PhotoImage(file="gauge.gif")

lowest=0
highest=originalAmt
val=0

start_x=128
start_y=145
leng=100

def read_amount_gauge():
    val=int(soapAmount)
    angle=pi*(val-lowest)/(highest-lowest)
    end_x=start_x-leng*cos(angle)
    end_y=start_y-leng*sin(angle)
    
    C.delete("all") #delete everything on canvas to redraw
    C.create_image(0,0,image=gauge_img,anchor=NW)
    C.create_line(start_x,start_y,end_x,end_y,fill="black",width=5)
    C.create_text(50,start_y+10,font="Arial 10",text=lowest)
    C.create_text(216,start_y+10,font="Arial 10",text=highest)
    C.create_text(start_x,start_y+50,font="Arial 20",text=val)
    top.after(500,read_amount_gauge) #schedule an update 500 ms later
    
C=Canvas(top,width=256,height=256)
C.pack()
top.after(0,read_amount_gauge) #schedule an update immediately
































root.mainloop()
