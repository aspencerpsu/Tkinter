import Tkinter
from Tkinter import *

import threading, sys

# Step 1. create an instance of Tk() to setup

mainframe = Frame()

# Step 2. Pack the main frame
mainframe.pack()

# You can now access the window in any order

Label(mainframe, text="Welcome To LifeForce!").pack(side="top")

# Step 3. Configure and Pack (Synchronously)

button = Button(mainframe, text="get system details", command=sys.stdout.write(str(threading.currentThread())))

button.config(bg="#259286", fg="#000000")

button.pack(side="left")

second_button = Button(mainframe, text="quit", command=mainframe.quit)
second_button.config(bg="#259286", fg="#000000")
second_button.pack(side="right")

mainframe.mainloop() #run the application with the following command
