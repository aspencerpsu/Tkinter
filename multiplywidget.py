from Tkinter import *
import threading
import sys

def result():
	print "The sum of 2+2 is: %d"%(2+2)

win = Frame()
win.pack()

Label(win, text='Click Add to get the sum or Quit to Exit').pack(side="top")

Button(win, text='Add', command=result()).pack(side="left")

Button(win, text='Quit', command=win.quit).pack(side='right')

Label(win, text="threading info: %s"%(threading.currentThread())).pack(side="bottom")

win.mainloop()
