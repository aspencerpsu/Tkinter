from Tkinter import *
import threading, sys

win = Tk()
openboxes = {"on": []}

def document():
	global openboxes, win
	if openboxes["on"] != []:
		dialog = openboxes["on"][0] 
		#dialog.destroy()
		openboxes["on"].pop() #remove the widget window
		del dialog
	else:
		pass #continue
	""" Define the function's purpose """
	cursor = listbox.curselection()
	item = listbox.get(cursor[0])
	root = Tk()
	openboxes["on"].append(root)
	access = getattr(root, str(item))
	print "\n\n####\n\t %s \n\n####\n\t"%(access.__doc__)
	label = Label(root, text=access.__doc__.upper(), fg="#738A05", padx=30, pady=30).pack(side="top", expand="yes", fill="both")
	return

Label(win, text="A list of the following packages from Tkinter:\n").pack(side="top")

scrollbar = Scrollbar(win)
scrollbar.pack(side="right", fill="y")
types = len(dir(win)) #list of the different widgets accessible with Tkinter

button = Button(win, text="quit?", command=win.quit)

button.config(bg="#A57706", fg="#042029", relief="ridge", bd=3)

button.pack(side="top")

listbox = Listbox(win, yscrollcommand=scrollbar.set)
listbox.config(height = "400", width="30")

listbox.document = document  #Bind the function to listbox constructor

window_docs = {}

for wid in range(0, types):
	constructor = dir(win)[wid] #constructor method 
	listbox.insert(wid, constructor)

listbox.pack(side='top', fill="y")

trigger = Button(win, text="info", command=lambda listbox=listbox: listbox.document()) 
scrollbar.config(command=listbox.yview)
trigger.place(x=20, y=30, width=30, height=15)

win.mainloop()	
