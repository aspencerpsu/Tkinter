from ortools.linear_solver import linear_solver_pb2 #linear problem solving tool
from ortools.linear_solver import pywraplp #problems to solve using pywrap advantage tools
import sys, Tkinter
from Tkinter import *
import simplex_class

root = Tk()

def resetfunction():
	import simplex_class
	global guiapp, root
	"""The resetfunction deletes all the String, Int, and Boolean Vars for 
	    linear package"""
	print "Working..."
	root.destroy()
	del guiapp
	
	reload(simplex_class)
	root = Tk()
	guiapp = GUIAPPLICATION(root)
	guiapp.mainloop()


def additionalVarCap(**kwargs):

	global guiapp, root
	if kwargs['state'].get(): #if the user wants an infinite guess
		try:
			guiapp.infVarDir[kwargs['instance']]['label'].grid_forget()
			guiapp.infVarDir[kwargs['instance']]['cap'][0].grid_forget()
			guiapp.infVarDir[kwargs['instance']]['label'].destroy()
			guiapp.infVarDir[kwargs['instance']]['cap'][0].destroy()
			del guiapp.infVarDir[kwargs['instance']]['label']
		except KeyError:
			"Nothing to do" 
	
	else:
		instancerow = int(guiapp.infVarDir[kwargs['instance']]['self'].grid_info()['row'])
		guiapp.infVarDir[kwargs['instance']]['label'] = Label(guiapp.frame, text="cap?")
		guiapp.infVarDir[kwargs['instance']]['cap'][0] = Entry(guiapp.frame, textvariable=kwargs['capvar'])

		#bind them A.K.A. hand the daughter's off to the groom for marriage

		guiapp.infVarDir[kwargs['instance']]['label'].grid(row=instancerow, column=3)
		guiapp.infVarDir[kwargs['instance']]['cap'][0].grid(row=instancerow, column=4)

def additionalDecisionVar(**kwargs):

	global guiapp, root
	guiapp.decisionvars(kwargs['newrow'])
	guiapp.infVarDir[kwargs['id']]['buttonadd'].grid_remove()
	guiapp.infVarDir[kwargs['id']]['labeladd'].grid_remove()
	guiapp.infVarDir[kwargs['id']]['buttonno'].grid_remove()

	print guiapp.hscrollbar
	print guiapp.vscrollbar

	del guiapp.hscrollbar 
	del guiapp.vscrollbar #replace the horizontal scrollbar & vertical scrollbar
	guiapp.hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
	guiapp.vscrollbar = AutoScrollbar(root, orient=VERTICAL) 
		
	guiapp.hscrollbar.grid(row=1, column=0, sticky=E+W)
	guiapp.vscrollbar.grid(row=0, column=1, sticky=N+S)

	guiapp.canvas.create_window(1,1, anchor=NE, window=guiapp.frame)
	guiapp.frame.update_idletasks()
	guiapp.canvas.config(scrollregion=guiapp.canvas.bbox("all"))
	guiapp.canvas.update_idletasks()
	guiapp.hscrollbar.config(command=guiapp.canvas.xview)
	guiapp.vscrollbar.config(command=guiapp.canvas.yview)


def nodecisionvars(**kwargs):
	global guiapp, root
	guiapp.constraintbatch(kwargs['row'] +1, "init")
	guiapp.infVarDir[kwargs['id']]['buttonadd'].grid_remove()
	guiapp.infVarDir[kwargs['id']]['buttonno'].grid_remove()
	guiapp.infVarDir[kwargs['id']]['labeladd'].grid_remove()

	guiapp.canvas.create_window(1, 1, anchor=NE, window=guiapp.frame)
	guiapp.frame.update_idletasks()
	guiapp.canvas.config(scrollregion=guiapp.canvas.bbox("all"), xscrollcommand=guiapp.hscrollbar.set, yscrollcommand=guiapp.vscrollbar.set)
	guiapp.vscrollbar.config(command=guiapp.canvas.yview)
	guiapp.hscrollbar.config(command=guiapp.canvas.xview)
	guiapp.canvas.update_idletasks()

	guiapp.vscrollbar.update_idletasks()
	guiapp.hscrollbar.update_idletasks()

def addandremove(**kwargs):
	global guiapp, root
	input = kwargs['constraint'].get()
	guiapp.constraintbatch(kwargs['row']+1,input) #continue adding constraints per user demand
	guiapp.constraintloop[kwargs['id']]['entryadd'][0].grid_remove()
	guiapp.constraintloop[kwargs['id']]['labeladd'].grid_remove()
	guiapp.constraintloop[kwargs['id']]['buttonno'].grid_remove()
	guiapp.constraintloop[kwargs['id']]['buttonadd'].grid_remove()

	guiapp.canvas.create_window(1, 1, anchor=N, window=guiapp.frame)
	guiapp.frame.update_idletasks()
	guiapp.canvas.config(scrollregion=guiapp.canvas.bbox("all"), xscrollcommand=guiapp.hscrollbar.set, yscrollcommand=guiapp.vscrollbar.set)
	guiapp.vscrollbar.config(command=guiapp.canvas.yview)
	guiapp.hscrollbar.config(command=guiapp.canvas.xview)

	guiapp.vscrollbar.update_idletasks()
	guiapp.hscrollbar.update_idletasks()

def constraintend(**kwargs):

	global guiapp, root
	guiapp.constraintloop[kwargs['id']]['entryadd'][0].grid_remove()
	guiapp.constraintloop[kwargs['id']]['labeladd'].grid_remove()
	guiapp.constraintloop[kwargs['id']]['buttonno'].grid_remove()
	guiapp.constraintloop[kwargs['id']]['buttonadd'].grid_remove()
	guiapp.objectivefunction(kwargs['row']+1)

	guiapp.canvas.create_window(1, 1, anchor=N, window=guiapp.frame)
	guiapp.canvas.config(scrollregion=guiapp.canvas.bbox("all"), height=guiapp.frame.winfo_height())
	guiapp.frame.update_idletasks()
	guiapp.canvas.update_idletasks()

	guiapp.vscrollbar.update_idletasks()
	guiapp.hscrollbar.update_idletasks()

	
class GUIAPPLICATION(Frame):

	def __init__(self, master):
		self.master = master # Master Widget
		verticalscrollbar = AutoScrollbar(self.master, orient=VERTICAL)
		horizontalscrollbar = AutoScrollbar(self.master, orient=HORIZONTAL)
		canvas = Canvas(self.master, yscrollcommand=verticalscrollbar.set, xscrollcommand=horizontalscrollbar.set, width=400, height=3000)

		#### Frame ####
		self.frame = Frame(canvas, height=8000, width=400)

		self.frame.rowconfigure(1, weight=1)
		self.frame.columnconfigure(1, weight=1)
		
		canvas.grid(row=0, column=0, sticky=N+S+E+W)
		verticalscrollbar.grid(row=0, column=1, sticky=N+S)
		horizontalscrollbar.grid(row=1, column=0, sticky=E+W)

		self.vscrollbar = verticalscrollbar
		self.hscrollbar = horizontalscrollbar
		##########################################


		self.label = Label(self.frame, width=int(.50*master.winfo_width()), height=int(.50*master.winfo_height()),text="Simplex Linear Solving Entry",font=('Arial', 24, 'underline'),fg="#ffffff", bg='#0A2933').grid(row=1,sticky=N+S+E+W,columnspan=5,padx=30)
		self.createLabel("delete all variables?")
		self.createReset()
		self.problemdescription = {'label': ''}
		self.problemLabel()
		self.infVarDir = {'decisionvars':3} #house the decisions
		self.decisionvars()
		self.constraintloop = {} #add all the constraint objects so if one decision var is addded, loop and configure the row and push +1
		self.objectiveblock = {} #add the objective expression with labels

		self.frame.update_idletasks()

		canvas.create_window(1, 1, anchor=NE, window=self.frame)
		canvas.config(scrollregion=canvas.bbox("all"), height=self.frame.winfo_height())
		self.canvas = canvas
		self.master.config(width=800, height=2000)
		self.master.grid_rowconfigure(0, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
	
	def createLabel(self, label):
		Label(self.frame, text=label, width=int(.50*self.frame.winfo_width()), height=int(.50*self.frame.winfo_height())).grid(row=2, column=1, sticky=E)

	def createReset(self):
		Button(self.frame, text='Reset?', command=(lambda x=None: resetfunction()), bg="#D11C24", fg="#ffffff", padx=10, pady=10).grid(row=2, column=2, sticky=E)

	
	def problemLabel(self):
		Label(self.frame, text="Report Problem Statement", pady=20).grid(row=3, column=0)
		getentry = StringVar()
		Entry(self.frame, textvariable=getentry).grid(row=3, column=1)
		self.problemdescription['label'] = getentry.get()
	
	
	def decisionvars(self,row=4):
		getvar = StringVar()
		#Add the label and entry for the decision variable itself
		Label(self.frame, text="Input a Variable").grid(row=row, column=0, sticky=W,padx=5)
		Entry(self.frame, textvariable=getvar).grid(row=row, column=1)

		self.checkbox = Checkbutton(self.frame, text="infinite variable?")
		self.infVarDir[id(self.checkbox)] = {'var': IntVar(), 'self': self.checkbox, 'entry': getvar}
		self.checkbox.grid(row=row, column=2)
		
		self.infVarDir[id(self.checkbox)]['label'] = Label(self.frame, text="cap?")	
		getentry = IntVar()
		self.infVarDir[id(self.checkbox)]['cap'] = [Entry(self.frame, textvariable=getentry), getentry]

		self.infVarDir[id(self.checkbox)]['label'].grid(row=row, column=3)
		self.infVarDir[id(self.checkbox)]['cap'][0].grid(row=row, column=4)
		self.infVarDir[id(self.checkbox)]['self'].config(variable= self.infVarDir[id(self.checkbox)]['var'], command=(lambda instance=id(self.checkbox), state=self.infVarDir[id(self.checkbox)]['var']: additionalVarCap(instance=instance, state=state, capvar=getentry) ) )


		self.infVarDir['decisionvars'] += 2 #remember the row for variables of user additions for later use...

		self.labeladd = Label(self.frame, text="Add More Decisions?")		
		self.infVarDir[id(self.checkbox)]['labeladd'] = self.labeladd
		self.infVarDir[id(self.checkbox)]['labeladd'].grid(row=row+1, padx=15, column=0, ipadx=5)

		self.button = Button(self.frame, text="Yes", bg="#738A05", fg="#ffffff", relief="raised", command=(lambda newrow=self.infVarDir['decisionvars'], id=id(self.checkbox): additionalDecisionVar(newrow=newrow, id=id)))
		self.infVarDir[id(self.checkbox)]['buttonadd'] = self.button
		self.infVarDir[id(self.checkbox)]['buttonadd'].grid(row=row+1, column=1, sticky=N+S+E+W, pady=25)
		self.buttonno = Button(self.frame, text="No", bg="#D11C24", fg="#ffffff", relief="raised", command=(lambda row=self.infVarDir['decisionvars']+1, id=id(self.checkbox): nodecisionvars(row=row, id=id)))
		self.infVarDir[id(self.checkbox)]['buttonno'] = self.buttonno
		self.infVarDir[id(self.checkbox)]['buttonno'].grid(row=row+1, column=2, sticky=N+S+E+W, pady=25)


	def constraintbatch(self,row, constraint=None):
		# REMEMBER WIDGETS THAT ARE OF AN ENTRY ARE CONTAINED IN THE FIRST INDEX OF THE LIST
		# WITHIN THE SLAVE MAPS FOR INSTANCE


		if not self.constraintloop.has_key('title'):
			self.constrainttitle = Label(self.frame, text="Constraints", font=('Arial', 24, 'underline'))
			self.constraintloop["title"] = self.constrainttitle
			self.constrainttitle.grid(row=self.infVarDir['decisionvars'] + 1, column=0, columnspan=5, sticky=N+E+W+S)

		#constraint label
		self.constraintlabel = Label(self.frame, text="%s:"%(constraint))
		self.constraintloop[id(self.constraintlabel)] = {'label': self.constraintlabel}
		self.constraintlabel.grid(row=row+2, column=0, pady=29, sticky=E)

		#constraint entry
		getentry = StringVar()
		self.constraintentry = Entry(self.frame, textvariable=getentry)
		self.constraintloop[id(self.constraintlabel)]['entry'] = getentry
		self.constraintentry.grid(row=row+2, column=1, padx=5, sticky=E)

		#constraint operator
		getoperator = StringVar()
		self.constraintoperator = Entry(self.frame, textvariable=getoperator, width=5)
		self.constraintloop[id(self.constraintlabel)]['operator'] = [self.constraintoperator, getoperator]
		self.constraintoperator.grid(row=row+2, column=2, padx=30, sticky=W)

		
		self.constraintlabelop = Label(self.frame, text="or symbol")
		self.constraintloop[id(self.constraintlabel)]['labelop'] = self.constraintlabelop
		self.constraintlabelop.grid(row=row+2, column=2, ipady=4, sticky=N)

		#constraint boundary
		getboundary = StringVar()
		self.constraintboundary = Entry(self.frame, textvariable=getboundary, width=5)
		self.constraintloop[id(self.constraintlabel)]['constraintbound'] = [self.constraintboundary, getboundary]
		self.constraintboundary.grid(row=row+2, column=3, padx=2, sticky=W)
		
		self.constraintlabelbo = Label(self.frame, text="boundary alloc?")
		self.constraintloop[id(self.constraintlabel)]['labelbound'] = self.constraintlabelbo
		self.constraintlabelbo.grid(row=row+2, column=3, ipady=4, sticky=N)

		#constraint addition:
		self.constraintlabelbu = Label(self.frame, text="Add A Constraint? Constraint Name:")
		self.constraintloop[id(self.constraintlabel)]['labeladd'] = self.constraintlabelbu
		self.constraintlabelbu.grid(row=row+3, column=0, columnspan=2, ipady=2, sticky=N)
		
		getconstraint = StringVar()
		self.constraintaddentry = Entry(self.frame, textvariable=getconstraint)
		self.constraintloop[id(self.constraintlabel)]['entryadd'] = [self.constraintaddentry, getconstraint]
		self.constraintaddentry.grid(row=row+3, column=2, ipady=2, sticky=E)

		self.button = Button(self.frame, bg="#738A05", fg="#ffffff", text="yes", command=(lambda id=id(self.constraintlabel),instance=self.constraintloop[id(self.constraintlabel)], row=row+3, constraint=getconstraint: addandremove(instance=instance, row=row, id=id, constraint=constraint)))
		self.constraintloop[id(self.constraintlabel)]['buttonadd'] = self.button
		self.button.grid(row=row+3, column=3)

		self.buttonno = Button(self.frame, bg="#D11C24", fg="#ffffff", text="no", command=(lambda row=row+3, id=id(self.constraintlabel): constraintend(row=row,id=id)))
		self.constraintloop[id(self.constraintlabel)]['buttonno'] = self.buttonno
		self.buttonno.grid(row=row+3, column=4)

	def objectivefunction(self, row):
		if not self.objectiveblock.has_key('title'):
			self.objectivetitle = Label(self.frame, text="Objective Statement", font=('Arial', 24, 'underline'), )
			self.objectiveblock['title'] = self.objectivetitle
			self.objectivetitle.grid(row=row, columnspan=5, column=0, sticky=N+W+S+E)

		self.label = Label(self.frame, text="Objective Goal Algorithm:", font=('Arial', 14))
		self.objectiveblock[id(self.label)] = self.label
		self.label.grid(row=row+1, column=0, columnspan=2, sticky=E)
		
		getentry = StringVar()
		v = StringVar()
		self.entry = Entry(self.frame, textvariable=getentry)
		self.objectiveblock[id(self.entry)] = {'entry': [self.entry, getentry], 'type': v}
		self.objectiveblock[id(self.entry)]['entry'][0].grid(row=row+1, column=2, columnspan=3, sticky=W)

		Radiobutton(self.frame, text='Max', variable=v, value='max',anchor=N).grid(row=row+1, column=3, sticky=W)
		Radiobutton(self.frame, text='Min', variable=v, value='min',anchor=N).grid(row=row+1, column=4, sticky=W)


		self.submitbutton = Button(self.frame, text="Submit", fg="#ffffff", bg="#D11C24", command=(lambda row=row+4: self.solve(row)))
		self.submitbutton.grid(row=row+1, column=5, columnspan=2, sticky=E+W+S+N)

	def solve(self, row):	
		self.verticalscrollbar.config(command=self.canvas.yview)
		self.horizontalscrollbar.config(command=self.canvas.xview)

		def orsolver():
			varentries = [(self.infVarDir[x]['entry'].get(), self.infVarDir[x]['cap'][1].get()) for x in self.infVarDir if x != 'decisionvars']
			print varentries
			varconstraints = [{'label': self.constraintloop[x]['label'].cget('text'), 'boundary': self.constraintloop[x]['constraintbound'][1].get(), 'op': self.constraintloop[x]['operator'][1].get(), 'entry': self.constraintloop[x]['entry'].get()} for x in self.constraintloop if x != 'title']
			print varconstraints
			objective = self.objectiveblock.values()[1]
			print objective	
			createsimplex = simplex_class.ProblemStatement(constraints=varconstraints, objective=objective['entry'][1].get(), type=objective['type'].get(), variables=varentries)



		self.frame_2 = Frame(self.frame)
		self.button = Button(self.frame_2, font=('Arial', 14, 'underline'), text="Solve?", fg="#ffffff", bg="#0A2933", command=(lambda x=None: orsolver()))
		self.frame_2.config(bd=5)
		self.frame_2.grid(row=row, column=2, columnspan=5, rowspan=3, sticky=N+W+E+S)
		self.button.grid(row=0, column=0, sticky=N+W+E+S) 

root.geometry("600x600+20+10") #Make sure to add the window length and height of the object
guiapp = GUIAPPLICATION(root)
root.mainloop()
