from Tkinter import *

def result():
	print "The sum of 2+2 is %.2f"%(2+2)

win = Frame()

win.pack()

Button(win, text='Add', command=result()).pack(side="left")
Label(win, text="Click 'Add' to get the sum or 'Quit' to exit").pack(side="top")
Button(win, text='Quit', command=win.quit).pack(side="right")

win.mainloop()
