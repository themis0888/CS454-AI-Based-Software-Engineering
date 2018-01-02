import numpy as np
from os import walk
import csv


f = [] 
for (a,b, filenames) in walk('fluccs_data/'):
    f.extend(filenames)


err_line = []
for name in filenames:
    f = open('fluccs_data/' + name, 'r')
    lines = csv.reader(f)
    for line in lines:
        if line[42] == '1':
            err_line.append(line)

    f.close()