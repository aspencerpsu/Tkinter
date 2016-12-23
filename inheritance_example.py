# This determines how the Tkinter packages and grids inherited widgets
# From the parent visual widget

import Tkinter
from Tkinter import *

#Main Frame

class Application(Frame):

	def __init__(self, master):
		Frame.__init__(self,master)
		self.grid()
		self.redFun()
		self.greenFun()
		self.widgets()
	def widgets(self):
		self.mylabel = Label(self, text="Hello World!")
		self.mylabel.grid()
	def redFun(self):
		self.redFrame = Frame(root, width=100, height=50, pady=5,bg="red")
		self.redFrame.grid()

	def greenFun(self):
		self.greenFrame = Frame(root, width=100, height=50, pady=5, bg='green')
		self.greenFrame.grid()

	
# Start #
root = Tk()
root.geometry("300x300")
app = Application(root)

root.mainloop()
