#! /usr/bin/python2.7

from __future__ import print_function
from ortools.linear_solver import linear_solver_pb2
from ortools.linear_solver import pywraplp
from Tkinter import *
import numpy

class ProblemStatement(object):

	def __init__(self, **kwargs):
		print(" \n \n -------------Linear Programming Example---------------- W/ %s ----------" %"CLP")
		print ("\n \n *Natural Language API* ")
		self.optimization_problem(0, kwargs['variables'], kwargs['constraints'], kwargs['type'], kwargs['objective'])
	
	def optimization_problem(self, optimization_problem_type, variables, constraints, type, objective):
		def blankcoefficients(expr):
			if expr.strip() == '':
				return 1
			else:
				return float(expr)
				
		solver = pywraplp.Solver("optimization_problem", optimization_problem_type)
		infinity = solver.infinity()
		vars = {}
		cons = {}
		for num in variables:
			if not num[1]:
				vars["%s"%(num[0])] = solver.NumVar(0.0, infinity, "%s"%(num[0]))
			else:
				vars["%s"%(num[0])] = solver.NumVar(0.0, int(num[1]), "%s"%(num[0]))

		if type == 'max':
			groupings = re.split('\+', objective)
			coefficients = map(blankcoefficients, map(lambda x: re.split('\-?[a-z|A-Z][0-9]*',x)[0], groupings))
			solver.Maximize(coefficients, vars.values())
		else:
			groupings = re.split('\+', objective)
			coefficients = map(blankcoefficients, map(lambda x: re.split('\-?[A-Z|a-z][0-9]*', x)[0], groupings))
			solver.Minimize(coefficients, vars.values())

		for constraint in constraints:
			groupings = re.split('\+', constraint['entry'])
			coefficients = map(blankcoefficients, map(lambda x: re.split('\-?[a-z|A-Z][0-9]*', x)[0], groupings))
			variables = vars.values()
			if constraint['op'] == '<=':
				cons["%s"%(constraint['label'][:-1])] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) <= int(constraint['boundary']))
			elif constraint['op'] == '>=':				
				cons["%s"%(constraint['label'][:-1])] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) >= int(constraint['boundary'])) 
			elif constraint['op'] == '<':
				cons["%s"%(constraint['label'][:-1])] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) < int(constraint['boundary'])) 
			elif constraint['op'] == '>':
				cons["%s"%(constraint['label'][:-1])] = solver.Add(sum([coefficients[x]*variables[x] for x in range(0,len(coefficients)-1)]) > int(constraint['boundary'])) 
			else:
				raise SyntaxError("Operator must be of type \'>\', \'<', \'<=\', or \'>=\' symbols")

		print (vars.values(), cons.values())
		self.SolveAndPrint(solver, vars.values(), cons.values())

	def SolveAndPrint(self, model, decisions, constraints):
		""" Solve the problem and print the solution"""
		self.root = Toplevel()

		self.label = Label(self.root, text="Number of variables = %d"%(model.NumVariables()))
		self.label.pack(pady=30)
		print ("Number of variables = %d"%(model.NumVariables()))
		print ("Number of constraints = %d"%(model.NumConstraints()))

		result_status = model.Solve()

		self.result = Label(self.root, text="%s"%(result_status))
		self.result.pack(pady=25)

		#Determine if the problem doesn't violate Simplex

		#Max Algorithms Rules #1-4

		try:

			assert model.VerifySolution(1e-7, True), "model is not verifiable" #The percentage of problem equivalent to infeasibility

		#The problem has an optimal solution

			assert result_status == pywraplp.Solver.OPTIMAL, "not an optimal solution present"
		except AssertionError:
			return "solution Not Optimal"

		self.label = Label(self.root, text="\n Problem solved in %f ms \n"%(model.wall_time()))
		self.label.pack(pady=30)

		print ("\n Problem solved in %f milliseconds \n" %(model.wall_time()))

		#The objective value of the solution `no reduced costs`
		self.label = Label(self.root, text="\n Optimal objective value = %f" %(model.Objective().Value()))
		self.label.pack(pady=30)
		print ("\n Optimal objective value = %f" %(model.Objective().Value()))

		#The value of each variable in the solution

		for variable in decisions:
			#self.label = Label(self.root, text="%s = %f"%(variable.name(), variable.solution_value()))
			#self.label.pack(pady=30)
			print ("%s = %f" %(variable.name(), variable.solution_value()))

		self.label = Label(self.root, text="\n \n Advanced Usage: \n")
		self.label.pack(pady=30)
		print ("\n \n Advanced Stats: \n")
		self.label.pack(pady=30)
		self.label = Label(self.root, text="\n \n Problem Solved in %d iterations"%model.iterations())
		print ("\n \n Problem solved in %d iterations" %model.iterations())
		self.label.pack(pady=30)

		for variable in decisions:
			#self.label = Label(self.root, text="\n \n %s: reduced cost = %f" %(variable.name(), variable.reduced_cost()))
			#self.label.pack(pady=30)
			print ("%s: reduced cost = %f" %(variable.name(), variable.reduced_cost()))

		activities = model.ComputeConstraintActivities() #printout of ERO's `b` in AX = b

		for i, constraint in enumerate(constraints):
			self.label = Label(self.root, text="\n\n constraint %d: dual value = %f\n activity=%f" %(i, constraint.dual_value(), activities[constraint.index()]))
			self.label.pack(pady=30)
			print ("constraint %d: dual value = %f\n activity=%f" %(i, constraint.dual_value(), activities[constraint.index()]))
