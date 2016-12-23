from ortools.linear_solver import linear_solver_pb2 #linear problem solving tool
from ortools.linear_solver import pywraplp #problems to solve using pywrap advantage tools
import sys, Tkinter
from Tkinter import *

root = Tk()

def resetfunction():
	"""The resetfunction deletes all the String, Int, and Boolean Vars for 
	    linear package"""
	print "Working..."


def additionalVarCap(**kwargs):
	global guiapp, root
	if kwargs['state'].get(): #if the user wants an infinite guess
		try:
			guiapp.infVarDir[kwargs['instance']]['label'].grid_forget()
			guiapp.infVarDir[kwargs['instance']]['entry'].grid_forget()
			guiapp.infVarDir[kwargs['instance']]['label'].destroy()
			guiapp.infVarDir[kwargs['instance']]['entry'].destroy()
			del guiapp.infVarDir[kwargs['instance']]['label']
			del guiapp.infVarDir[kwargs['instance']]['entry']
		except KeyError:
			print guiapp.infCheckbuttonDir
			print root.grid_slaves()
	
	else:
		instancerow = int(guiapp.infVarDir[kwargs['instance']]['self'].grid_info()['row'])
		guiapp.infVarDir[kwargs['instance']]['label'] = Label(root, text="cap?")
		guiapp.infVarDir[kwargs['instance']]['entry'] = Entry(root, textvariable=IntVar())

		#bind them A.K.A. hand the daughter's off to the groom for marriage

		guiapp.infVarDir[kwargs['instance']]['label'].grid(row=instancerow, column=3)
		guiapp.infVarDir[kwargs['instance']]['entry'].grid(row=instancerow, column=4)

		print guiapp.infVarDir
		print root.grid_slaves()

def additionalDecisionVar(**kwargs):
	global guiapp, root
	guiapp.decisionvars(kwargs['newrow'])
	guiapp.infVarDir[kwargs['id']]['buttonadd'].grid_remove()
	guiapp.infVarDir[kwargs['id']]['labeladd'].grid_remove()

class GUIAPPLICATION(Frame):

	def __init__(self, master):
		self.master = master # Master Widget
		self.label = Label(master, width=int(.50*master.winfo_width()), height=int(.50*master.winfo_height()),text="Simplex Linear Solving Entry").grid(row=0,sticky=N+S+E+W,columnspan=3,padx=30)
		self.createLabel("delete all variables?")
		self.createReset()
		self.problemLabel()	
		self.infVarDir = {'decisionvars':3} #house the decisions
		self.decisionvars()
		self.constraintloop = {} #add all the constraint objects so if one decision var is addded, loop and configure the row and push +1
		#self.constraintbatch(self.infVarDir['decisionvars'], "init")
		
	
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
		self.infVarDir[id(self.checkbox)] = {'var': IntVar(), 'self': self.checkbox}
		self.checkbox.grid(row=row, column=2)
		
		self.infVarDir[id(self.checkbox)]['label'] = Label(self.master, text="cap?")

		self.infVarDir[id(self.checkbox)]['entry'] = Entry(self.master, textvariable=IntVar())

		self.infVarDir[id(self.checkbox)]['label'].grid(row=row, column=3)
		self.infVarDir[id(self.checkbox)]['entry'].grid(row=row, column=4)
		self.infVarDir[id(self.checkbox)]['self'].config(variable= self.infVarDir[id(self.checkbox)]['var'], command=(lambda instance=id(self.checkbox), state=self.infVarDir[id(self.checkbox)]['var']: additionalVarCap(instance=instance, state=state) ) )
		self.infVarDir['decisionvars'] += 2 #remember the row for variables of user additions for later use...
		self.labeladd = Label(self.master, text="Add More Decisions?")		
		self.infVarDir[id(self.checkbox)]['labeladd'] = self.labeladd
		self.infVarDir[id(self.checkbox)]['labeladd'].grid(row=row+1, padx=15, column=0, ipadx=5)

		self.button = Button(self.master, text="Yes", bg="#738A05", fg="#ffffff", relief="raised", command=(lambda newrow=self.infVarDir['decisionvars'], id=id(self.checkbox): additionalDecisionVar(newrow=newrow, id=id)))
		self.infVarDir[id(self.checkbox)]['buttonadd'] = self.button
		self.infVarDir[id(self.checkbox)]['buttonadd'].grid(row=row+1, column=1, sticky=N+S+E+W, pady=25)

	def constraintbatch(self,row, constraint=None):
		# REMEMBER WIDGETS THAT ARE OF AN ENTRY ARE CONTAINED IN THE FIRST INDEX OF THE LIST
		# WITHIN THE SLAVE MAPS FOR INSTANCE
		if not self.constraintloop.has_key('title'):
			self.constrainttitle = Label(self.master, text="Constraints", font=('Arial', 24, 'underline'))
			self.constraintloop["title"] = self.constrainttitle
			self.constrainttitle.grid(row=self.infVarDir['decisionvars']+1, column=0, columnspan=5, sticky=N+E+W+S)

		#Constraint label
		self.constraintlabel = Label(self.master, text="%s:"%(constraint))
		self.constraintloop[id(self.constraintlabel)] = self.constraintlabel
		self.constraintlabel.grid(row=row+2, column=0, pady=29, sticky=E)

		#constraint entry
		self.constraintentry = Entry(self.master, textvariable=StringVar())
		self.constraintloop[id(self.constraintentry)] = self.constraintentry
		self.constraintentry.grid(row=row+2, column=1, padx=5, sticky=E)

		#constraint operator
		getoperator = StringVar()
		self.constraintoperator = Entry(self.master, textvariable=getoperator, width=5)
		self.constraintloop[id(self.constraintoperator)] = [self.constraintoperator, getoperator]
		self.constraintoperator.grid(row=row+2, column=2, padx=30, sticky=W)

		
		self.constraintlabelop = Label(self.master, text="or symbol")
		self.constraintloop[id(self.constraintlabelop)] = self.constraintlabelop
		self.constraintlabelop.grid(row=row+2, column=2, ipady=4, sticky=N)

		#constraint boundary
		getboundary = StringVar()
		self.constraintboundary = Entry(self.master, textvariable=getboundary, width=5)
		self.constraintloop[id(self.constraintboundary)] = [self.constraintboundary, getboundary]
		self.constraintboundary.grid(row=row+2, column=3, padx=2, sticky=W)
		
		self.constraintlabelbo = Label(self.master, text="boundary alloc?")
		self.constraintloop[id(self.constraintlabelbo)] = self.constraintlabelbo
		self.constraintlabelbo.grid(row=row+2, column=3, ipady=4, sticky=N)

		#constraint addition:
		self.constraintlabelbu = Label(self.master, text="Add A Constraint? Constraint Name:")
		self.constraintloop[id(self.constraintlabelbu)] = self.constraintlabelbu
		self.constraintlabelbu.grid(row=row+3, column=0, columnspan=2, ipady=2, sticky=N)
		
		getconstraint = StringVar()
		self.constraintaddentry = Entry(self.master, textvariable=getconstraint)
		self.constraintloop[id(self.constraintaddentry)] = [self.constraintaddentry, getconstraint]
		self.constraintaddentry.grid(row=row+3, column=2, ipady=2, sticky=E)

		self.button = Button(self.master, text="yes", command=(lambda row=row+3, constraint=getconstraint.get(): self.constraintbatch(row, constraint)))
		self.constraintloop[id(self.button)] = self.button
		self.button.grid(row=row+3, column=3)


		



	
#root.geometry("450x600+20+10")

guiapp = GUIAPPLICATION(root)

mainloop()
