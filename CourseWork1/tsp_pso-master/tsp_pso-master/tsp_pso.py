# encoding:utf-8

'''
	Solution for Travelling Salesman Problem using PSO (Particle Swarm Optimization)
	Discrete PSO for TSP

	References: 
		http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.258.7026&rep=rep1&type=pdf
		http://www.cs.mun.ca/~tinayu/Teaching_files/cs4752/Lecture19_new.pdf
		http://www.swarmintelligence.org/tutorials.php

	References are in the folder "references" of the repository.
'''

from operator import attrgetter
import random, sys, time, copy, math, csv, sys


# class that represents a graph
class Graph:

	def __init__(self, amount_vertices):
		self.edges = {} # dictionary of edges
		self.vertices = set() # set of vertices
		self.amount_vertices = amount_vertices # amount of vertices


	# adds a edge linking "src" in "dest" with a "cost"
	def addEdge(self, src, dest, cost = 0):
		# checks if the edge already exists
		if not self.existsEdge(src, dest):
			self.edges[(src, dest)] = cost
			self.vertices.add(src)
			self.vertices.add(dest)


	# checks if exists a edge linking "src" in "dest"
	def existsEdge(self, src, dest):
		return (True if (src, dest) in self.edges else False)


	# shows all the links of the graph
	def showGraph(self):
		print('Showing the graph:\n')
		for edge in self.edges:
			print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

	# returns total cost of the path
	def getCostPath(self, path):
		
		total_cost = 0
		for i in range(self.amount_vertices - 1):
			total_cost += self.edges[(path[i], path[i+1])]

		# add cost of the last edge
		total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
		return total_cost


	# gets random unique paths - returns a list of lists of paths
	def getRandomPaths(self, max_size):

		random_paths, list_vertices = [], list(self.vertices)

		initial_vertice = random.choice(list_vertices)
		if initial_vertice not in list_vertices:
			print('Error: initial vertice %d not exists!' % initial_vertice)
			sys.exit(1)

		list_vertices.remove(initial_vertice)
		list_vertices.insert(0, initial_vertice)

		for i in range(max_size):
			list_temp = list_vertices[1:]
			random.shuffle(list_temp)
			list_temp.insert(0, initial_vertice)

			if list_temp not in random_paths:
				random_paths.append(list_temp)

		return random_paths


# class that represents a complete graph
class CompleteGraph(Graph):

	# generates a complete graph
	def generates(self):
		for i in range(self.amount_vertices):
			for j in range(self.amount_vertices):
				if i != j:
					weight = random.randint(1, 10)
					self.addEdge(i, j, weight)


# class that represents a particle
class Particle:

	def __init__(self, solution, cost):

		# current solution
		self.solution = solution

		# best solution (fitness) it has achieved so far
		self.pbest = solution

		# set costs
		self.cost_current_solution = cost
		self.cost_pbest_solution = cost

		# velocity of a particle is a sequence of 4-tuple
		# (1, 2, 1, 'beta') means SO(1,2), prabability 1 and compares with "beta"
		self.velocity = []

	# set pbest
	def setPBest(self, new_pbest):
		self.pbest = new_pbest

	# returns the pbest
	def getPBest(self):
		return self.pbest

	# set the new velocity (sequence of swap operators)
	def setVelocity(self, new_velocity):
		self.velocity = new_velocity

	# returns the velocity (sequence of swap operators)
	def getVelocity(self):
		return self.velocity

	# set solution
	def setCurrentSolution(self, solution):
		self.solution = solution

	# gets solution
	def getCurrentSolution(self):
		return self.solution

	# set cost pbest solution
	def setCostPBest(self, cost):
		self.cost_pbest_solution = cost

	# gets cost pbest solution
	def getCostPBest(self):
		return self.cost_pbest_solution

	# set cost current solution
	def setCostCurrentSolution(self, cost):
		self.cost_current_solution = cost

	# gets cost current solution
	def getCostCurrentSolution(self):
		return self.cost_current_solution

	# removes all elements of the list velocity
	def clearVelocity(self):
		del self.velocity[:]


# PSO algorithm
class PSO:

	def __init__(self, graph, iterations, size_population, beta=1, alfa=1):
		self.graph = graph # the graph
		self.iterations = iterations # max of iterations
		self.size_population = size_population # size population
		self.particles = [] # list of particles
		self.beta = beta # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.alfa = alfa # the probability that all swap operators in swap sequence (pbest - x(t-1))

		# initialized with a group of random particles (solutions)
		solutions = self.graph.getRandomPaths(self.size_population)

		# checks if exists any solution
		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)

		# creates the particles and initialization of swap sequences in all the particles
		for solution in solutions:
			# creates a new particle
			particle = Particle(solution=solution, cost=graph.getCostPath(solution))
			# add the particle
			self.particles.append(particle)

		# updates "size_population"
		self.size_population = len(self.particles)


	# set gbest (best particle of the population)
	def setGBest(self, new_gbest):
		self.gbest = new_gbest

	# returns gbest (best particle of the population)
	def getGBest(self):
		return self.gbest


	# shows the info of the particles
	def showsParticles(self):

		print('Showing particles...\n')
		for particle in self.particles:
			print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent solution: %s\t|\tcost current solution: %d' \
				% (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
							particle.getCostCurrentSolution()))
		print('')


	def run(self):

		# for each time step (iteration)
		for t in range(self.iterations):

			# updates gbest (best particle of the population)
			self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

			# for each particle in the swarm
			for particle in self.particles:

				particle.clearVelocity() # cleans the speed of the particle
				temp_velocity = []
				solution_gbest = copy.copy(self.gbest.getPBest()) # gets solution of the gbest
				solution_pbest = particle.getPBest()[:] # copy of the pbest solution
				solution_particle = particle.getCurrentSolution()[:] # gets copy of the current solution of the particle

				# generates all swap operators to calculate (pbest - x(t-1))
				for i in range(self.graph.amount_vertices):
					if solution_particle[i] != solution_pbest[i]:
						# generates swap operator
						swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)

						# makes the swap
						aux = solution_pbest[swap_operator[0]]
						solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
						solution_pbest[swap_operator[1]] = aux

				# generates all swap operators to calculate (gbest - x(t-1))
				for i in range(self.graph.amount_vertices):
					if solution_particle[i] != solution_gbest[i]:
						# generates swap operator
						swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)

						# makes the swap
						aux = solution_gbest[swap_operator[0]]
						solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
						solution_gbest[swap_operator[1]] = aux

				
				# updates velocity
				particle.setVelocity(temp_velocity)

				# generates new solution for particle
				for swap_operator in temp_velocity:
					if random.random() <= swap_operator[2]:
						# makes the swap
						aux = solution_particle[swap_operator[0]]
						solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
						solution_particle[swap_operator[1]] = aux
				
				# updates the current solution
				particle.setCurrentSolution(solution_particle)
				# gets cost of the current solution
				cost_current_solution = self.graph.getCostPath(solution_particle)
				# updates the cost of the current solution
				particle.setCostCurrentSolution(cost_current_solution)

				# checks if current solution is pbest solution
				if cost_current_solution < particle.getCostPBest():
					particle.setPBest(solution_particle)
					particle.setCostPBest(cost_current_solution)


def ucl_dst(A, B):
	return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

def find_boundary(lst):
	x_max = lst[0].x
	x_min = lst[0].x	
	y_max = lst[0].y
	y_min = lst[0].y
	for i in range(len(lst)):
		if lst[i].x > x_max:
			x_max = lst[i].x
		if lst[i].x < x_min:
			x_min = lst[i].x
		if lst[i].y > y_max:
			y_max = lst[i].y
		if lst[i].y < y_min:
			y_min = lst[i].y


	return x_max, x_min, y_max, y_min

def devide(num,lst):
	new_lst = [[] for i in range(num)]
	x_max, x_min, y_max, y_min = find_boundary(lst)
	for k in range(len(lst)):
		for j in range(1,num):
			if (lst[k].y < (1-j/num)*y_min + (j/num)*y_max) & (lst[k].y >= (1-(j-1)/num)*y_min + ((j-1)/num)*y_max):
				new_lst[j].append(lst[k])


	return new_lst


class Node:
	def __init__(self, id, x_cord, y_cord):
		self.id = id
		self.x = x_cord
		self.y = y_cord
		self.x_id = None
		self.y_id = None

if __name__ == "__main__":
	
	f = open('rl11849.tsp', 'r')
	b_line = f.read().split()
	i = 0
	node_lst = []
	j = 1
	num = int(sys.argv[1])
	path = []
	length = 0


	while b_line[i] != 'EOF':
		if b_line[i] == str(j):
			node_lst.append(Node(b_line[i], float(b_line[i+1]), float(b_line[i+2])))
			j += 1
		i += 1

	A = devide(num,node_lst)

	for k in range(num):
	# creates the Graph instance

		size = len(A[k])
		if A[k] == []:
			continue
		print('{}: {}'.format(k,size))
		graph = Graph(amount_vertices=size)

		# This graph is in the folder "images" of the repository.
		for i in range(size):
			for j in range(size):
				if i != j:
					graph.addEdge(A[k][i].id, A[k][j].id, ucl_dst(A[k][i], A[k][j]))
		print('Resister over')

		# creates a PSO instance
		pso = PSO(graph, iterations=50, size_population=10, beta=1, alfa=0.9)
		pso.run() # runs the PSO algorithm
		pso.showsParticles()
		path += pso.getGBest().getPBest()
		length += pso.getGBest().getCostPBest()  # shows the particles

	# shows the global best particle
	print('gbest: %s | cost: %d\n' % (path, length))

	'''
	# random graph
	print('Random graph...')
	random_graph = CompleteGraph(amount_vertices=20)
	random_graph.generates()
	pso_random_graph = PSO(random_graph, iterations=10000, size_population=10, beta=1, alfa=1)
	pso_random_graph.run()
	print('gbest: %s | cost: %d\n' % (pso_random_graph.getGBest().getPBest(), 
					pso_random_graph.getGBest().getCostPBest()))
	'''