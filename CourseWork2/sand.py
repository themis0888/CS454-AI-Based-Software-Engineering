import numpy as np
from os import walk
import csv
import random
import sys



def f1():
	return 1

def f2():
	return 2

def f3():
	return 3

f_list = [f1, f2, f3]

for i in range(3):
	print(f_list[i]())