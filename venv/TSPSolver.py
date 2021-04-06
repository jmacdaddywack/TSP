#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import random



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def greedy( self,time_allowance=60.0 ):
		results = {}
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()

		while not foundTour and time.time() - start_time < time_allowance:
			cities = self._scenario.getCities().copy()
			currentCity = cities.pop(0)
			route = [currentCity]

			while len(cities) != 0:
				currentCity = self.findShortestPath(currentCity, cities)
				route.append(currentCity)
			bssf = TSPSolution(route)
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
			count += 1

		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results

	'''
	Searches through list of cities and pops and returns the cities that is nearest to  the current city
	'''
	def findShortestPath(self, current, cities):
		shortestPath = float("Inf")
		index = 0
		for i in range(len(cities)):
			cost = current.costTo(cities[i])
			if cost < shortestPath:
				shortestPath = cost
				index = i
		return cities.pop(index)
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	def branchAndBound( self, time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		max_repetitions = 10
		results = {}
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()

		best_cost = np.inf
		best_bssf = None
		num_solutions = 0
		cities = self._scenario.getCities().copy()

		while num_solutions < max_repetitions and time.time() - start_time < time_allowance:
			swap = random.randint(0, len(cities) - 1)
			temp = cities[0]
			cities[0] = cities[swap]
			cities[swap] = temp

			i = 0
			while i < len(cities) - 2:
				j = i + 2
				while j < len(cities) - 1:
					if cities[i].costTo(cities[i + 1]) > cities[i].costTo(cities[j]):
						temp = cities[i + 1]
						cities[i + 1] = cities[j]
						cities[j] = temp
					j += 1
				i += 1
			bssf = TSPSolution(cities)
			if bssf.cost < np.inf:
				foundTour = True
			count += 1

			if best_cost > bssf.cost:
				print ("Old cost: ", best_cost)
				print ("New cost: ", bssf.cost)
				best_cost = bssf.cost
				best_bssf = bssf

			num_solutions += 1
			if num_solutions >= max_repetitions:
				if not foundTour:        # If still hasn't found a solution by the time num_solutions reaches MAX_REPETITIONS
					max_repetitions += 1 # allow for one more run

		print("Number of Solutions: ", num_solutions)

		end_time = time.time()
		results['cost'] = best_cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = best_bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results
