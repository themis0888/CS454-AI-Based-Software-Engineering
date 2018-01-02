import numpy as np
from os import walk
import csv
import random



dna = [0.9220677485698374, 0.9100257295545071, 0.21715329849667672, 0.5165936339751951, 0.25892812834765755, 0.29698529393737183, 0.3717177257746823, 0.05909124657798681, 0.1727651822855801, 0.6021195722727968, 0.34806617929771266, 0.5922938448580425, 0.4349886231408373, 0.003479650085198358, 0.054627055633714866, 0.24014421203343794, 0.0416828796647368, 0.44699633239517284, 0.8655693555348235, 0.4538867741946022, 0.7732982501504061, 0.2841004461399209, 0.635358754404911, 0.9095028569332736, 0.7295709916619847, 0.05797134468626336, 0.38715471030331083, 0.11579503110831385, 0.33957627864757667, 0.5272627161971818, 0.10060619590812941, 0.5300256844546463, 0.7984876255678061, 0.07347857906501465, 0.7424586467653782, 0.5632005905961303, 0.4679265060739021, 0.20820410740561476, 0.09910217047065001, 0.3871943232355379, 0.7662787872443031]
LINE_SIZE = 42
DNA_SIZE = 41

f = [] 
for (a,b, filenames) in walk('fluccs_data/'):
	f.extend(filenames)

fitness_val = 0
err_num = 0
err_file = dict()

ranking_bar = 10
#random.shuffle(filenames)
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


	if err_file[name] not in top_list:
		fitness_val += 15
		

	f.close()

print(err_file)
