import sys
from Tkinter import *
import threading

widget = Button(None, text='Click Me', command=sys.exit)

widget.pack()

widget.mainloop()
