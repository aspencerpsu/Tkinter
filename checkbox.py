from Tkinter import *
states = []
def check(i):
	states[i] = not states[i]

root = Tk()

for i in range(4):
	test = Checkbutton(root, text=str(i), command=(lambda i=i:check(i)))
	test.pack(side="top")
	states.append(0)

root.mainloop()
print states
