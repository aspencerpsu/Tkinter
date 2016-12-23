import sys
from Tkinter import *
popupper = (len(sys.argv) > 1)

def dialog():
	win = Toplevel()
	Label(win, text="Do you always do what you are told? ").pack()
	Button(win, text="Now click this one", command = win.destroy).pack()
	Label(win, text="list of constructors for python: \n \n \t %s"%(dir(win))).pack()
	if popupper:
		win.focus_set()
		win.grab_set()
		win.wait_window()
	print ('You better obey me....')

root = Tk()

Button(root, text='Click Me Baby', command=dialog).pack()
root.mainloop()


