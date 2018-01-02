import numpy as np
from os import walk
import csv
import random


LINE_SIZE 	= 42
DNA_SIZE    = 41
POP_SIZE    = 20
GENERATIONS = 60
SEED_filter	= [0.9220677485698374, 0.9100257295545071, 0.21715329849667672, 0.5165936339751951, 0.25892812834765755, 0.29698529393737183, 0.3717177257746823, 0.05909124657798681, 0.1727651822855801, 0.6021195722727968, 0.34806617929771266, 0.5922938448580425, 0.4349886231408373, 0.003479650085198358, 0.054627055633714866, 0.24014421203343794, 0.0416828796647368, 0.44699633239517284, 0.8655693555348235, 0.4538867741946022, 0.7732982501504061, 0.2841004461399209, 0.635358754404911, 0.9095028569332736, 0.7295709916619847, 0.05797134468626336, 0.38715471030331083, 0.11579503110831385, 0.33957627864757667, 0.5272627161971818, 0.10060619590812941, 0.5300256844546463, 0.7984876255678061, 0.07347857906501465, 0.7424586467653782, 0.5632005905961303, 0.4679265060739021, 0.20820410740561476, 0.09910217047065001, 0.3871943232355379, 0.7662787872443031]
SEED_rank	= [0.8469174212932208, 0.24222500294242144, 0.959345303597786, 0.2372845394085067, 0.909029373498903, 0.5468491592401744, 0.935239026981628, 0.10569638869446088, 0.4848551178940422, 0.779515538495714, 0.8783187516925782, 0.40792671176405804, 0.9541825380863366, 0.9088943745544734, 0.31732909785448093, 0.9715704973905055, 0.7507622363205788, 0.01838378110440886, 0.8679241269676008, 0.9632211187187267, 0.7424285103493301, 0.5136942678817408, 0.7340009535293063, 0.47415535614366555, 0.9942224733194591, 0.6759063328804589, 0.6502191936678051, 0.9435719867799748, 0.9945844787025327, 0.9109631423920778, 0.9685178176146967, 0.923358978882266, 0.9375917937438328, 0.8824329148546302, 0.9720593794242726, 0.615597068323467, 0.9997572842674, 0.9551532335774668, 0.007285112920442871, 0.8983918335878014, 0.9968348142250842]
SEED 		= [0.8303922992623334, 0.9022180532513338, 0.27293181477397477, 0.5061013965273999, 0.3316238558194771, 0.34977298701772014, 0.4592754149922633, 0.06978592024551608, 0.1728543668536556, 0.6085801316755224, 0.4237489376872849, 0.553436215081015, 0.511297090109096, 0.12837978253220192, 0.9655999995343683, 0.30598315547863436, 0.2007604345359989, 0.36364021746164304, 0.8040338422956701, 0.5917827846775194, 0.81541795356198, 0.42286430339665915, 0.5763700080800743, 0.7644113344502876, 0.4311899392682048, 0.1303952835633016, 0.33440969832444556, 0.1344030042176904, 0.2906497204186368, 0.49150634204676297, 0.10655503545316436, 0.36357164433896183, 0.6441091858209844, 0.20744368481206862, 0.7661605058708474, 0.4746775805519456, 0.38218352488613605, 0.17365256814771998, 0.27205592883672014, 0.42243197274926175, 0.6932668708980132]
SEED_rand	= [random.random() for i in range(DNA_SIZE)] 
SEED_5	 	= [0.6421755170689676, 0.15519331216518795, 0.5286898357282412, 0.027599411721728726, 0.061421274195825444, 0.7180162810279758, 0.5356315113667476, 0.7098560523184523, 0.3237009196969203, 0.26069584620411285, 0.07164709883257146, 0.6508227979660364, 0.476726721015002, 0.19310655268035826, 0.15372854800827018, 0.051119401335774965, 0.19587239751816335, 0.03329514274209106, 0.4651030550809668, 0.8488065317918105, 0.2945686185798022, 0.6001324874348186, 0.5020543485280258, 0.4722453214492949, 0.01684054699233169, 0.2800898104540959, 0.11465380301145692, 0.2839876820798132, 0.08607911300719646, 0.6874666054144998, 0.5918305443926576, 0.24693624845389844, 0.40457293071233064, 0.03905730895282899, 0.18981287535527686, 0.5065999538667196, 0.4849787945199291, 0.3140063849535645, 0.40757214770718436, 0.6649113548515019, 0.0815221251348384]


fit_name 	= ['fitness_filter', 'fitness_1p', 'fitness_5', 'fitness']
f = [] 
for (a,b, filenames) in walk('fluccs_data/'):
	f.extend(filenames)



def weighted_choice(items):

	weight_total = sum((item[1] for item in items))
	n = random.uniform(0, weight_total)
	for item, weight in items:
		if n < weight:
			return item
		n = n - weight
	return item


def random_population(seed):

	pop = []
	for i in range(POP_SIZE):
		dna = [(seed[i] + 0.2 * random.uniform(-seed[i], 1-seed[i])) for i in range(DNA_SIZE)] 
		pop.append(dna)
	return pop


def fitness_filter(dna):

	err_num = 0
	err_line = []
	random.shuffle(filenames)
	for name in filenames[:int(0.2*len(filenames))]:
		f = open('fluccs_data/' + name, 'r')
		lines = csv.reader(f)
		for line in lines:
			try:
				val = float(line[1])
			except ValueError:
				continue

			line_f = list(map(float, line[1:]))
			estimate = 0
			estimate = np.dot(line_f[:DNA_SIZE], dna)

			if (estimate.any() < 20) and (line[42] == '1'):
				err_num += 10
			elif (estimate.any() >= 10) and (line[42] == '0'):
				err_num += 1

		f.close()

	return err_num


def fitness_5(dna):


	fitness_val = 0
	err_num = 0
	err_file = dict()
	ranking_bar = 5
	random.shuffle(filenames)
	for name in filenames[:int(0.4*len(filenames))]:
		f = open('fluccs_data/' + name, 'r')
		lines = csv.reader(f)
		index = 0
		rank_list = []

		for line in lines:
			if index == 0:
				index += 1
				continue
			if len(line) < LINE_SIZE:
				continue
			if line[LINE_SIZE] == '1':
				err_file[name] = index

			rank_list.append([index, list(map(float,line[1:]))])
			index += 1
		# np.dot(d[1][:DNA_SIZE], dna)
		rank_list = sorted(rank_list, key = lambda d: np.dot(d[1][:DNA_SIZE], dna), reverse = True)
		top_list = []
		if len(rank_list) < ranking_bar:
			continue
		for i in range(ranking_bar):
			top_list.append(rank_list[i][0])

		try:
			err_file[name]
		except KeyError:
			#print('no fault line')
			continue
		if err_file[name] not in top_list:
			fitness_val += 1
			

		f.close()
	
	return fitness_val 


def fitness(dna):

	total_rank = 0
	in_3rd = 0

	fitness_val = 0
	err_num = 0
	err_file = dict()

	ranking_bar = 10
	for name in filenames:

		f = open('fluccs_data/' + name, 'r')
		lines = csv.reader(f)
		index = 0
		rank_list = []
		err_file[name] = []

		for line in lines:
			if index == 0:
				index += 1
				continue
			if len(line) < LINE_SIZE:
				continue
			if float(line[LINE_SIZE]) != 0:												#####
				err_file[name].append([index, float(line[LINE_SIZE])]) 				#####

			rank_list.append([index, list(map(float,line[1:]))])
			index += 1
		
		err_file[name] = sorted(err_file[name], key = lambda d: d[1])				#####
		rank_list = sorted(rank_list, key = lambda d: np.dot(d[1][:DNA_SIZE], dna), reverse = True)
		top_list = []


		if len(rank_list) < ranking_bar:
			continue
		for i in range(ranking_bar):
			top_list.append(rank_list[i][0])
			if rank_list[i][0] == err_file[name][0][0]:
				fitness_val += i
				if i > 4:
					fitness_val += 2

		f.close()
	return fitness_val 


def fitness_1p(dna):

	fitness_val = 0
	err_num = 0
	err_file = dict()
	ranking_bar = 10
	random.shuffle(filenames)
	for name in filenames:
		f = open('fluccs_data/' + name, 'r')
		lines = csv.reader(f)
		index = 0
		rank_list = []

		for line in lines:
			if index == 0:
				index += 1
				continue
			if len(line) < LINE_SIZE:
				continue
			if line[LINE_SIZE] == '1':
				err_file[name] = index

			rank_list.append([index, list(map(float,line[1:]))])
			index += 1

		rank_list = sorted(rank_list, key = lambda d: np.dot(d[1][:DNA_SIZE], dna), reverse = True)
		top_list = []
		if len(rank_list) < ranking_bar:
			continue
		for i in range(int(0.01 * len(rank_list))):
			top_list.append(rank_list[i][0])

		try:
			err_file[name]
		except KeyError:
			print('no fault line')
			continue
		if err_file[name] not in top_list:
			fitness_val += 1			

		f.close()
	
	return fitness_val 





def mutate(dna):

	dna_out = []
	mutation_chance = 100
	for c in range(DNA_SIZE):
		if int(random.random()*mutation_chance) == 1:
			dna_out.append(random.random())
		else:
			dna_out.append(dna[c])
	return dna_out

# crossover : dna dna -> dna dna 
def crossover(dna1, dna2):

	pos = int(random.random()*DNA_SIZE)
	return (dna1[:pos]+dna2[pos:], dna2[:pos]+dna1[pos:])

# GA_process : dna integer -> population(set of dna)
def GA_process(seed, mode):
	population = random_population(seed)
	gen_elite = []

	for generation in range(GENERATIONS):
		print("Generation: {}\tFitness : {}".format(generation, fit_list[mode](population[0])))
		if generation % 5 == 0:
			print('Individuals : \n {} \n'.format(population[0]))
		
		weighted_population = []

		min_fit = 200
		ran1 = population[0]
		ran2 = population[1]
		for individual in population:
			fitness_val = fit_list[mode](individual)
			if min_fit > fitness_val:
				min_fit = fitness_val
				ran2 = ran1
				ran1 = individual


			if fitness_val == 0:
				pair = (individual, 1.0)
			else:
				pair = (individual, 1.0/fitness_val)

			weighted_population.append(pair)

		population = []

		for _ in range(int(POP_SIZE/2)-2):

			ind1 = weighted_choice(weighted_population)
			ind2 = weighted_choice(weighted_population)

			ind1, ind2 = crossover(ind1, ind2)

			population.append(mutate(ind1))
			population.append(mutate(ind2))
		population.append(ran1)
		population.append(ran2)
		gen_elite.append([generation, population[0]])

	return population


if __name__ == "__main__":

	fit_list 	= [fitness_filter, fitness_1p, fitness_5, fitness]
	seed = SEED
	for i in range(len(fit_list)):
		print('\nFor {}'.format(fit_name[i]))
		population = GA_process(seed, i)
		seed = population[0]

	fittest_string = population[0]
	minimum_fitness = fitness(population[0])

	for individual in population:
		ind_fitness = fitness(individual)
		if ind_fitness <= minimum_fitness:
			fittest_string = individual
			minimum_fitness = ind_fitness
	print("Minumum_fitness = {}".format(minimum_fitness))
	print('Final individual: \n {}'.format(population[0]))
	print("Fittest String: %s" % fittest_string)
	