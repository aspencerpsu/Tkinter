from Tkinter import *


root = Tk()

vscrollbar = AutoScrollbar(root)
vscrollbar.grid(row=0, column=1, sticky=N+S)
hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=E+W)

canvas = Canvas(root, yscrollcommand=vscrollbar.set,
		      xscrollcommand=hscrollbar.set)

canvas.grid(row=0, column=0, sticky=N+S+E+W)

vscrollbar.config(command=canvas.yview)

hscrollbar.config(command=canvas.xview)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = Frame(canvas)

frame.rowconfigure(1, weight=1)

frame.columnconfigure(1, weight=1)

rows = 5

for i in range(1,rows):
	for j in range(1,10):
		button = Button(frame, padx=7, pady=7, text="[%d, %d]" %(i,j))
		button.grid(row=i, column=j, sticky='news')


canvas.create_window(0, 0, anchor=NW, window=frame)

frame.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
