import Tkinter

from Tkinter import *

root = Tk()

labelfont = ('times', 24, 'italic') #setting the family, size and style

widget = Label(root, text='Eat At Ak\'s')

widget.config(bg='black', fg='red')

widget.pack(expand="yes", fill="both")
root.mainloop()


