import math
import csv
import sys
import random


class Node:
	def __init__(self, id, x_cord, y_cord):
		self.id = id
		self.x = x_cord
		self.y = y_cord
		self.x_id = None
		self.y_id = None

"""
csvfile = open('data.csv', 'w')

for i in range(len(node_lst)):
	csvfile.write('{}, {}, {}\n'.format(node_lst[i].id, node_lst[i].x, node_lst[i].y))

csvfile.close()
"""

def ucl_dst(A, B):
	return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

def path_dst(lst):
	dist = 0
	pointer = lst[len(lst)-1]
	for i in lst:
		dist += ucl_dst(pointer, i)
		pointer = i
	return dist

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


def Greedy(lst):
	size = len(lst)
	bucket = set(lst)
	pointer = lst[0]
	ans = None
	path = []
	while len(bucket) > 1:
		path.append(pointer)
		key = float("inf")
		for i in bucket:
			if (ucl_dst(pointer,i) < key) & (pointer != i):
				ans = i
				temp_dist = ucl_dst(pointer,i)
		bucket.remove(pointer)
		pointer = ans
		#print('Progress:\t{}/{} left'.format(len(bucket),size))
	path.append(bucket.pop())

	return path


def devide_Greedy(num,lst):
	new_lst = [[] for i in range(num)]
	x_max, x_min, y_max, y_min = find_boundary(lst)
	for k in range(len(lst)):
		for j in range(1,num):
			if (lst[k].y < (1-j/num)*y_min + (j/num)*y_max) & (lst[k].y >= (1-(j-1)/num)*y_min + ((j-1)/num)*y_max):
				new_lst[j].append(lst[k])

	dist = 0
	entry = []
	for i in range(num):
		if new_lst[i] != []:
			temp = Greedy(list(new_lst[i]))
			dist += temp[1]
			entry += temp[0]
	return entry, dist, new_lst


def local_opt(lst):
	
	path = lst
	cur_dst = path_dst(path)

	sign = True
	size = len(lst)
	num_improve = 0

	while sign == True: 
		sign = False
		for i in range(size - 1):
			for k in range(i+1, size):
				new_lst = lst[:i]
				new_lst.extend(reversed(lst[i:k + 1]))
				new_lst.extend(lst[k+1:])

				new_dst = path_dst(new_lst)
				if new_dst < cur_dst:
					path = new_lst
					sign = True
					num_improve += 1
					cur_dst = new_dst
					break 
			if sign == True:
				break

	return path


def neighbor(lst):
	i = random.randrange(0,len(lst)-2)
	k = random.randrange(i+1,len(lst)-1)

	new_lst = lst[0:i]
	new_lst.extend(reversed(lst[i:k + 1]))
	new_lst.extend(lst[k+1:])
	return new_lst


def anneal(solution):
    old_cost = path_dst(solution)
    T = 1.0e+300
    T_min = 0.1
    alpha = 0.9
    while T > T_min:
        num_iter = 1
        while num_iter <= 1000:
            new_solution = neighbor(solution)
            new_cost = path_dst(new_solution)
            diff = (old_cost-new_cost)/T
            if diff > 700:
            	diff = 700
            ap = math.exp(diff)
            if diff > 0 or ap > random.random():
                solution = new_solution
                old_cost = new_cost
            num_iter += 1
        T = T * alpha
    return solution


#def main():
f_name = sys.argv[1]
f = open(f_name, 'r')
b_line = f.read().split()
i = 0
node_lst = []

j = 1

while b_line[i] != 'EOF':
	if b_line[i] == str(j):
		node_lst.append(Node(b_line[i], float(b_line[i+1]), float(b_line[i+2])))
		j += 1
	i += 1

simple = []
for i in range(100):
	simple.append(Node(i,random.randrange(0,200),random.randrange(0,200)))

if len(sys.argv) == 2:
	opt_lst = anneal(node_lst)
elif sys.argv[2] == 'greedy':
	opt_lst = Greedy(node_lst)
elif sys.argv[2] == 'local':
	opt_lst = local_opt(node_lst)
elif sys.argv[2] == 'anneal':
	opt_lst = anneal(node_lst)

# greedy_lst = Greedy(node_lst)
# local_lst = opt(greedy_lst)
# print(A)
opt_lst = anneal(node_lst)
print(path_dst(opt_lst))

csvfile = open('solution.csv', 'w')

for i in range(len(opt_lst)):
	csvfile.write(str(opt_lst[i].id) + '\n')

csvfile.close()
"""
if __name__ == '__main__':
	main()
"""