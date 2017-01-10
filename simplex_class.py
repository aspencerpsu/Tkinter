#! /usr/bin/python2.7

from __future__ import print_function
from ortools.linear_solver import linear_solver_pb2
from ortools.linear_solver import pywraplp
from Tkinter import *
import tkFileDialog
import subprocess

def donothing():
    print("Nothing happening")

def file_save(text):

    f = tkFileDialog.asksaveasfile(mode="w", defaultextension=".txt")
    if f is None:
    	f = open("report.txt", "w+")
	text2save = str(text.get(1.0, END))
	f.write(text2save)
	f.close()
        return
    elif str(text.get(1.0, END)):
    	text2save = str(text.get(1.0, END))
    	f.write(text2save)
    	f.close()
    else:
    	print("You can't save this file")

class ProblemStatement(object):

	def __init__(self, **kwargs):
		print(" \n \n -------------Linear Programming Example---------------- W/ %s ----------" %"CLP")
		print("\n \n *Natural Language API* ")
		self.optimization_problem(0, kwargs['variables'], kwargs['constraints'], 
						kwargs['type'], kwargs['objective'])
	
	def optimization_problem(self, optimization_problem_type, variables,
                                constraints, type, objective):

		def blankcoefficients(expr):

			expr = expr.strip()
			if expr == '':
				return 1
			elif expr == '-':
				return -1
			else:
				return float(expr)
				
		solver = pywraplp.Solver("optimization_problem", optimization_problem_type)
		infinity = solver.infinity()
		vars = {}
		cons = {}
		for num in variables:
			if not num[1]:
				vars[str(num[0])] = solver.NumVar(0.0, infinity, str(num[0]))
			else:
				vars[str(num[0])] = solver.NumVar(0.0, int(num[1]), str(num[0]))

		if type == 'max':
			groupings = re.split('\+', objective)
			coefficients = map(blankcoefficients, map(lambda x: re.split('[a-zA-Z_]+[0-9]+',
				x)[0], groupings))
			solver.Maximize(coefficients, vars.values())
		else:
			groupings = re.split('\+', objective)
			coefficients = map(blankcoefficients, map(lambda x: re.split('[A-Za-z_]+[0-9]+',
				x)[0], groupings))
			solver.Minimize(coefficients, vars.values())

		for constraint in constraints:
			groupings = re.split('\+', constraint['entry'])
			
			label = constraint['label'][:-1]

			boundary = constraint['boundary']

			op = constraint['op'].strip() #remove whitespacing

			coefficients = map(blankcoefficients, map(lambda x: re.split('[a-zA-Z_]+[0-9]+',
				x)[0], groupings))
			variables = vars.values()
			if op == '<=':
				cons[str(label)] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) <= int(boundary), label)
			elif op == '>=':
				cons[str(label)] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) >= int(boundary), label)
			elif op == '<':
				cons[str(label)] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) < int(boundary), label) 
			elif  op== '>':
				cons[str(label)] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) > int(boundary), label) 
			elif op == '=':
				cons[str(label)] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) == int(boundary), label)
			else: raise SyntaxError("""Operator must be of type '=', \'>\', \'<', \'<=\', or \'>=\' symbols""")

		print (vars.values(), cons.values())
		self.SolveAndPrint(solver, vars.values(), cons.values())

	def SolveAndPrint(self, model, decisions, constraints):
		""" Solve the problem and print the solution"""
		self.root = Toplevel()
		menubar = Menu(self.root)
		text=Text(self.root)
		
		filemenu=Menu(menubar, tearoff=0)
		filemenu.add_command(label="Save As...", 
					command=(lambda text=text: file_save(text)), 
					accelerator="Ctrl+Shift+S")

		filemenu.add_command(label="Reload Module", command=(lambda: reload(simplex_class)), accelerator="Ctrl+T")

		filemenu.add_command(label="Close", 
					command=donothing, 
					accelerator="Ctrl+w") #come back to this
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.root.quit)

		menubar.add_cascade(label="File", menu=filemenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help", command=donothing) #come back to this
		text.insert(END, 
				"\nNumber of variables = %d\n"%(model.NumVariables()))

		print ("Number of variables = %d"%(model.NumVariables()))
		print ("Number of constraints = %d"%(model.NumConstraints()))

		text.insert(END, "\nNumber of constraints = %d\n"%(model.NumConstraints()))
		
		result_status = model.Solve()

		text.insert(END, "\nsolve output = %s"%(result_status))

		assert model.VerifySolution(1e-7, True), "model is not verifiable" # % equivalent to infeasibility

		assert result_status == pywraplp.Solver.OPTIMAL, "not an optimal solution present" #The problem has an optimal solution

		text.insert(END, "\nProblem solved in %f ms \n"%(model.wall_time()))

		print ("\nProblem solved in %f milliseconds \n" %(model.wall_time()))

		text.insert(END, "\nOptimal objective value = %f \n" %(model.Objective().Value())) #The objective value of the solution `no reduced costs`
		print ("\nOptimal objective value = %f\n" %(model.Objective().Value()))

		for variable in decisions:
			text.insert(END, "\n%s = %f\n"%(variable.name(), variable.solution_value()))
			print ("%s = %f" %(variable.name(), variable.solution_value()))

		text.insert(END, "\n \nAdvanced Usage: \n")
		print ("\n \nAdvanced Stats: \n")
		text.insert(END, "\n \nProblem Solved in %d iterations"%model.iterations())
		print ("\n \n Problem solved in %d iterations" %model.iterations())

		for variable in decisions:
			text.insert(END, "\n \n%s: reduced cost = %f" %(variable.name(), 
									variable.reduced_cost()))
			print ("%s: reduced cost = %f" %(variable.name(), variable.reduced_cost()))

		activities = model.ComputeConstraintActivities() #printout of RHS = `b` in AX = b

		for i, constraint in enumerate(constraints):
	
			print(dir(constraint))
			text.insert(END, 
				"\n\n constraint %s: dual value = %f\n activity=%f" %(constraint.name(), 
											constraint.dual_value(), 
											activities[constraint.index()]))

			print ("constraint %s: dual value = %f\nactivity=%f" %(constraint.name(), 
										constraint.dual_value(),
										activities[constraint.index()]))
			text.insert(END, 
					"\n \n constraint %s Lower to Upper Boundary:\n \t  %f < %.2d < %f" %(constraint.name(),
														constraint.Lb(),
														activities[constraint.index()],
														constraint.Ub()))

			print ("constraint %s Lower.....to.....Upper Boundary: %f < %.2d < %f" %(constraint.name(), 
												constraint.Lb(),
												activities[constraint.index()],
												constraint.Ub()))
		text.config(state=DISABLED)
		text.pack()
		self.root.config(menu=menubar)
