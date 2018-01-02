import numpy as np
from os import walk
import csv
import random
import sys



#dna = [0.8303922992623334, 0.9022180532513338, 0.27293181477397477, 0.5061013965273999, 0.3316238558194771, 0.34977298701772014, 0.4592754149922633, 0.06978592024551608, 0.1728543668536556, 0.6085801316755224, 0.4237489376872849, 0.553436215081015, 0.511297090109096, 0.12837978253220192, 0.9655999995343683, 0.30598315547863436, 0.2007604345359989, 0.36364021746164304, 0.8040338422956701, 0.5917827846775194, 0.81541795356198, 0.42286430339665915, 0.5763700080800743, 0.7644113344502876, 0.4311899392682048, 0.1303952835633016, 0.33440969832444556, 0.1344030042176904, 0.2906497204186368, 0.49150634204676297, 0.10655503545316436, 0.36357164433896183, 0.6441091858209844, 0.20744368481206862, 0.7661605058708474, 0.4746775805519456, 0.38218352488613605, 0.17365256814771998, 0.27205592883672014, 0.42243197274926175, 0.6932668708980132]
dna = [0.8105761691189202, 0.8403866670679802, 0.25875856391156976, 0.466270484542888, 0.394625545129007, 0.43325192804399076, 0.5235703522845698, 0.11909428989144802, 0.26745695720229995, 0.6783802213583531, 0.35882604956336933, 0.5475290628134805, 0.5193667468291079, 0.1220042542353565, 0.948427541705796, 0.3632079524606084, 0.3506276322421571, 0.3962399256710268, 0.6930055202558214, 0.6676332260703831, 0.08191025642252248, 0.5127807725554739, 0.5858822345306869, 0.6634102248869527, 0.5804085176629754, 0.20620759961439233, 0.31636832927567704, 0.16680188146583452, 0.43124693410796344, 0.5713022579166503, 0.19928146467679725, 0.38689089500760937, 0.6816888810584526, 0.2747475788753686, 0.6737203577116613, 0.5382031183765028, 0.4249920545231617, 0.29070452931355345, 0.2178810436735465, 0.4085635439076995, 0.5799814843351907]

LINE_SIZE = 42
DNA_SIZE = 41

if len(sys.argv) == 1: 
	f = [] 
	for (a,b, filenames) in walk('fluccs_data/'):
		f.extend(filenames)
else:
	filenames = sys.argv[1:]

def full_fitness(dna):
	total_rank = 0
	in_3rd = 0

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
				print('File: {} \tRank: {}'.format(name, i))
				fitness_val += i
				if i < 4:
					in_3rd += 1
		"""
		if err_file[name] not in top_list:
			fitness_val += 15
		"""
			

		f.close()
	print('Total number of file : \t{}'.format(len(filenames)))
	print("Total rank sum : \t{}".format(fitness_val))
	print('Num of rank under 3: \t{}'.format(in_3rd))

	
full_fitness(dna)