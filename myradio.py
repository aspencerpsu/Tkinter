import Tkinter
from Tkinter import *

state = '' #initialization for the state

buttons = []

# State of buttons created for each button to select

def choose(i):
    global state
    state = i
    for btn in buttons:
    	btn.deselect()
    buttons[i].select()

# Create the program for the frame to be foundation
root = Tk()

for i in range(4):
	radio = Radiobutton(root, text=str(i), 
				value=str(i), command=(lambda i=i: choose(i))
				)
	radio.pack(side="top")
	buttons.append(radio)

root.mainloop()
print "You chose the following number: %s" %(state)


