from Tkinter import *

root = Tk()

def add_entry(master, text):
	frame = Frame(master)

	label = Label(frame, text=text)
	label.pack(side=LEFT)

	entry = Entry(frame)
	entry.pack(side=LEFT)

	frame.pack()

add_entry(root, "First")
add_entry(root, "Second")
add_entry(root, "Third")

mainloop()
