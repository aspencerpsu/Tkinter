from Tkinter import *
import threading, sys


def document():
	""" Define the function's purpose """
	cursor = listbox.curselection()
	item = listbox.get(cursor[0])
	root = Tk()
	access = getattr(root, str(item))
	print "\n\n####\n\t %s \n\n####\n\t"%(access.__doc__)
	root.destroy() #destroy the propagated window
	return

win = Tk()

Label(win, text="A list of the following packages from Tkinter:\n").pack(side="top")

scrollbar = Scrollbar(win)
types = len(dir(win)) #list of the different widgets accessible with Tkinter

button = Button(win, text="quit?", command=win.quit)

button.config(bg="#A57706", fg="#042029", relief="ridge", bd=3)

button.pack(side="top")

listbox = Listbox(win, yscrollcommand=scrollbar.set)
listbox.config(height = "400", width="30")

listbox.document = document  #Bind the function to listbox constructor

window_docs = {}

for wid in range(0, types-1):
	constructor = dir(win)[wid] #constructor method 
	listbox.insert(wid, constructor)

listbox.pack(side='top', fill="y")

trigger = Button(win, text="info", command=lambda listbox=listbox: listbox.document()) 

trigger.place(x=20, y=30, width=30, height=15)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")

while True:
	win.mainloop()	
