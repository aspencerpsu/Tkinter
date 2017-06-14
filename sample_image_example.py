#! /usr/bin/python2.7
from Tkinter import *
from PIL import Image, ImageTk

class AFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        image = Image.open('lingo_scale.JPG')
        img = ImageTk.PhotoImage(image)
        self.label = Label(self.master, image=img)
        self.label.pack()

def main():

    a_root = Tk()
    lingo_image = AFrame(a_root)
    a_root.mainloop()

if __name__ == '__main__' and __package__==None:
    main()
