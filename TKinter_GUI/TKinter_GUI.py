from tkinter import *
from PIL import ImageTk, Image
from math import *

top= Tk()
top.title("Group F's TKinter GUI")
    
gauge_img=PhotoImage(file="gauge.gif")


# Reads value of originalAmt of bottle	
with open("../originalAmt.txt", "r") as f:
        originalAmt = f.read()

# Reads current value of soapAmount
with open("../soapAmount.txt", "r") as f:
        soapAmount = f.read()


lowest=0
highest=int(originalAmt)
val=0

start_x=128
start_y=145
leng=100


def read_amount_gauge():
    # Reads current value of soapAmount
    with open("../soapAmount.txt", "r") as f:
            soapAmount = f.read()

    val=int(soapAmount)
    angle=pi*(val-lowest)/(highest-lowest)
    end_x=start_x-leng*cos(angle)
    end_y=start_y-leng*sin(angle)
    
    C.delete("all") # delete everything on canvas to redraw
    C.create_image(0,0,image=gauge_img,anchor=NW)
    C.create_line(start_x,start_y,end_x,end_y,fill="black",width=5)
    C.create_text(50,start_y+10,font="Arial 10",text=lowest)
    C.create_text(216,start_y+10,font="Arial 10",text=highest)
    C.create_text(start_x,start_y+50,font="Arial 20",text=val)
    top.after(500,read_amount_gauge) #schedule an update 500 ms later
    
C=Canvas(top,width=256,height=256)
C.pack()
top.after(0,read_amount_gauge) #schedule an update immediately

###############################################################################

B=Canvas(top,bg="light blue",width=550,height=550)

# Reads current value of soapAmount
with open("../soapAmount.txt", "r") as f:
        soapAmount = f.read()

happy_filename = ImageTk.PhotoImage(Image.open ("face_happy.jpg"))
sad_filename = ImageTk.PhotoImage(Image.open ("face_sad.jpg"))

percentage = (int(soapAmount) / int(originalAmt)) * 100

    
if percentage < 50:
    I=B.create_image(40,40,anchor=NW,image=sad_filename)
    print("Percentage of remaining liquid less than 50%!")
        
else:
    I=B.create_image(40,40,anchor=NW,image=happy_filename)
    print("Percentage of remaining liquid is more than 50%")
    
        
B.pack()
top.mainloop()
