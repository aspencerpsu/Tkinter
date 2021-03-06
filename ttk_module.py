import ttk
from Tkinter import *
#from Tkinter.scrolledtext import ScrolledText

def demo():
    root = Tk()
    root.title("ttk.Notebook")

    nb = ttk.Notebook(root)

    # adding Frames as pages for the ttk.Notebook
    # first page, which would get widgets gridded into it

    page1 = ttk.Frame(nb)

    # Second page
    page2 = ttk.Frame(nb)
    text = Text(page2)
    text.insert(END, "love ultra")
    text.pack(expand=1, fill="both")

    nb.add(page1, text='One')
    nb.add(page2, text='Two')

    nb.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    demo()
