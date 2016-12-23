from ortools.linear_solver import linear_solver_pb2 #linear problem solving tool
from ortools.linear_solver import pywraplp #problems to solve using pywrap advantage tools
import sys, Tkinter
from Tkinter import *

root = Tk()

def resetfunction():
	"""The resetfunction deletes all the String, Int, and Boolean Vars for 
	    linear package"""
	print "Working..."


def additionalConstraintCap(**kwargs):
	global guiapp, root
	if kwargs['state'].get(): #if the user wants an infinite guess
		try:
			guiapp.infCheckbuttonDir[kwargs['instance']]['label'].grid_forget()
			guiapp.infCheckbuttonDir[kwargs['instance']]['entry'].grid_forget()
			guiapp.infCheckbuttonDir[kwargs['instance']]['label'].destroy()
			guiapp.infCheckbuttonDir[kwargs['instance']]['entry'].destroy()
			del guiapp.infCheckbuttonDir[kwargs['instance']]['label']
			del guiapp.infCheckbuttonDir[kwargs['instance']]['entry']
		except KeyError:
			print guiapp.infCheckbuttonDir
			print root.grid_slaves()
	
	else:
		instancerow = int(guiapp.infCheckbuttonDir[kwargs['instance']]['self'].grid_info()['row'])
		guiapp.infCheckbuttonDir[kwargs['instance']]['label'] = Label(root, text="cap?")
		guiapp.infCheckbuttonDir[kwargs['instance']]['entry'] = Entry(root, textvariable=IntVar())

		#bind them A.K.A. hand the daughter's off to the groom for marriage

		guiapp.infCheckbuttonDir[kwargs['instance']]['label'].grid(row=instancerow, column=3)
		guiapp.infCheckbuttonDir[kwargs['instance']]['entry'].grid(row=instancerow, column=4)

		print guiapp.infCheckbuttonDir
		print root.grid_slaves()

def createVarLimit(check):
	if not check.InfVar: #if the user doesn't want a infinite spec. append row
		print "create a label for the widget"
	else:
		print "you're suppose to leave it"

class GUIAPPLICATION(Frame):

	def __init__(self, master):
		self.master = master # Master Widget
		self.InfVar = 1
		self.label = Label(master, width=int(.50*master.winfo_width()), height=int(.50*master.winfo_height()),text="Simplex Linear Solving Entry").grid(row=0,sticky=N+S+E+W,columnspan=3,padx=30)
		self.createLabel("delete all variables?")
		self.createReset()
		self.problemLabel()	
		self.infCheckbuttonDir = {'decisionvars':3} #house the decisions
		self.decisionvars()
		self.constraintloop = {} #add all the constraint objects so if one decision var is addded, loop and configure the row and push +1
		self.constraintbatch(self.infCheckbuttonDir['decisionvars'], "init")
		
	
	def createLabel(self, label):
		Label(self.master, text=label, width=int(.50*self.master.winfo_width()), height=int(.50*self.master.winfo_height())).grid(row=1, column=1, sticky=E)

	def createReset(self):
		Button(self.master, text='Reset?', command=resetfunction(), bg="#D11C24", padx=10, pady=10).grid(row=1, column=2, sticky=E)
	
	def problemLabel(self):
		ment = StringVar
		Label(self.master, text="Report Problem Statement", pady=20).grid(row=2, column=0)
		Entry(self.master, textvariable=ment).grid(row=2, column=1)
	
	def decisionvars(self,row=3):

		#Add the label and entry for the decision variable itself
		Label(self.master, text="Input a Variable").grid(row=row, column=0, sticky=W,padx=5)
		Entry(self.master, textvariable=StringVar()).grid(row=row, column=1)

		self.checkbox = Checkbutton(self.master, text="infinite variable?")
		self.infCheckbuttonDir[id(self.checkbox)] = {'var': IntVar(), 'self': self.checkbox}
		self.checkbox.grid(row=row, column=2)
		
		self.infCheckbuttonDir[id(self.checkbox)]['label'] = Label(self.master, text="cap?")

		self.infCheckbuttonDir[id(self.checkbox)]['entry'] = Entry(self.master, textvariable=IntVar())

		self.infCheckbuttonDir[id(self.checkbox)]['label'].grid(row=row, column=3)
		self.infCheckbuttonDir[id(self.checkbox)]['entry'].grid(row=row, column=4)
		self.infCheckbuttonDir[id(self.checkbox)]['self'].config(variable= self.infCheckbuttonDir[id(self.checkbox)]['var'], command=(lambda instance=id(self.checkbox), state=self.infCheckbuttonDir[id(self.checkbox)]['var']: additionalConstraintCap(instance=instance, state=state) ) )
		self.infCheckbuttonDir['decisionvars'] += 2 #remember the row for variables of user additions for later use...
		print self.infCheckbuttonDir
		Label(self.master, text="Add More Decisions?").grid(row=row+1, padx=15, column=0, ipadx=5)
		Button(self.master, text="Yes", bg="#738A05", fg="#ffffff", relief="raised", command=(lambda newrow=self.infCheckbuttonDir['decisionvars']: self.decisionvars(newrow))).grid(row=row+1, column=1, sticky=N+S+E+W, pady=25)

	def constraintbatch(self,row, constraint=None):
		if not self.constraintloop.has_key('title'):
			self.constrainttitle = Label(self.master, text="Constraints", font=('Arial', 24, 'underline'))
			self.constraintloop["title"] = self.constrainttitle
			self.constrainttitle.grid(row=self.infCheckbuttonDir['decisionvars']+1, column=0, columnspan=5, sticky=N+E+W+S)

		#Constraint label
		self.constraintlabel = Label(self.master, text="%s:"%(constraint))
		self.constraintloop[id(self.constraintlabel)] = self.constraintlabel
		self.constraintlabel.grid(row=row+2, column=0, pady=29, sticky=E)

		#constraint entry
		self.constraintentry = Entry(self.master, textvariable=StringVar())
		self.constraintloop[id(self.constraintentry)] = self.constraintentry
		self.constraintentry.grid(row=row+2, column=1, padx=5, sticky=E)

		#constraint operator

		self.constraintoperator = Entry(self.master, textvariable=StringVar(), width=5)
		self.constraintloop[id(self.constraintoperator)] = self.constraintoperator
		self.constraintoperator.grid(row=row+2, column=2, padx=30, sticky=W)

		
		self.constraintlabelop = Label(self.master, text="or symbol")
		self.constraintloop[id(self.constraintlabelop)] = self.constraintlabelop
		self.constraintlabelop.grid(row=row+2, column=2, ipady=4, sticky=N)

		#constraint boundary

		self.constraintboundary = Entry(self.master, textvariable=StringVar(), width=5)
		self.constraintloop[id(self.constraintboundary)] = self.constraintboundary
		self.constraintboundary.grid(row=row+2, column=3, padx=2, sticky=W)
		
		self.constraintlabelbo = Label(self.master, text="boundary alloc?")
		self.constraintloop[id(self.constraintlabelbo)] = self.constraintlabelbo
		self.constraintlabelbo.grid(row=row+2, column=3, ipady=4, sticky=N)

		#constraint addition:
		self.constraintlabelbu = Label(self.master, text="Add A Constraint? Constraint Name:")
		self.constraintloop[id(self.constraintlabelbu)] = self.constraintlabelbu
		self.constraintlabelbu.grid(row=row+3, column=0, columnspan=2, ipady=2, sticky=N)
		
		self.constraintaddentry = Entry(self.master, textvariable=StringVar())
		self.constraintloop[id(self.constraintaddentry)] = self.constraintaddentry
		getentry = id(self.constraintaddentry)
		self.constraintaddentry.grid(row=row+3, column=2, ipady=2, sticky=E)

		self.button = Button(self.master, text="yes", command=(lambda row=row+3, constraint=self.constraintloop[getentry].get(): self.constraintbatch(row, constraint)))
		self.constraintloop[id(self.button)] = self.button
		self.button.grid(row=row+3, column=3)


		



	
#root.geometry("450x600+20+10")

guiapp = GUIAPPLICATION(root)

mainloop()
