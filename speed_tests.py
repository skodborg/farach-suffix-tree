import farach
from utils import Node, str2int
import random
import string
import traceback
import mccreight
import naive
import check_correctness
import sys

import os
import psutil
import time
import memory_tracker

# commit e6d458690371c0e5839b7247167ae92c67f53739 for mccreight without dict
# remember to change line 143 and 35
sys.setrecursionlimit(30*1000)
def getAverageForString(S, algorithm):
	totalTime = 0
	iterations = 5
	tree = None
	minimum = float("inf")
	maximum = 0
	totalMemory = 0
	for j in range(iterations):
			start = time.time()

			memory_tracker.rebase()
			tree = algorithm.construct_suffix_tree(S)
			print("done")
			del tree
			totalMemory = memory_tracker.getPeak()
			end = time.time()
			totalTime += (end - start)
			minimum = min(minimum, (end-start))
			maximum = max(maximum, (end-start))
	totalTime = totalTime
	totalTime = totalTime
	return totalTime / iterations, None, (totalMemory / iterations)




def testProcedure(algorithms, data_functions):
	iterations = 5
	maxTime = 5*60  #sekunder

	timeTaken = dict()

	for i in range(10*1000, 340*1000, 10*1000):
		for data_func in data_functions:
			data = data_func(i)
			for alg in algorithms:
				
				for t in range(iterations):
					if alg.__name__ in timeTaken and timeTaken[alg.__name__] > maxTime:
						break
					start = time.time()
					memory_tracker.rebase()
					alg.construct_suffix_tree(data)
					end = time.time()

					memory = memory_tracker.getPeak()
					t = end-start

					timeTaken[alg.__name__] = t
					

					# if len(alg) == 3 and alg[2]:
					# 	ret[1].update_leaf_list()
					# 	print("testing")
					# 	check_correctness.check_correctness(ret[1], data)
					f = open("testData/" + alg.__name__ + "_" + data_func.__name__, 'a')
					proc = psutil.Process(os.getpid())
					f.write(str(i)+", "  + str(t) +  ", " + str(memory) + "\n") 
					f.close()

	

def testNoise():
	i = 0
	while True:
		i += 1000*10000
		for n in range(100):
			start = time.time()
			testArray = [None]*100
			for t in range(i):
				testArray[2] = t * 2 % 3
			end = time.time()
			f = open("testData/noise.txt", 'a')
			f.write(str(i)+"," + str((end - start)) + "\n")  # python will convert \n to os.linesep
			f.close()

def testMemoryTracking():
	i = 4000
	while i < 1000*40000000:
		i +=  10000*10

		current_process = psutil.Process(os.getpid())
		mem1 = psutil.virtual_memory().used >> 20
		# print(mem1)
		test = [n for n in range(i)]

		mem = psutil.virtual_memory().used >> 20
		
		f = open("testData/memoryTracking.txt", 'a')
		f.write(str(i)+"," + str(abs(mem1-mem)) + ", " + str(sys.getsizeof(test) >> 20) +", " + str(float(sys.getsizeof(test) >> 20)*4.7)  + "\n")  # python will convert \n to os.linesep
		f.close()
		del test

# DATA ALGORITHMS:
def fibonacci(n):
	a, b = 0, 1
	data = []
	for i in range(0, n):
		a, b = b, a + b
		data.append(a)
	return data


def only_ones(i):
	return [1 for n in range(i)]

def different_char(i):
	return [n for n in range(i)]

def random_data(i):
	return str2int(''.join(random.choice(string.digits) for _ in range(i)))

def random_data_varying_alphabet(length):
		def helper(i):
			return [random.randint(0,i) for _ in range(length)]
		return helper

def same_char(length):
	return [0]*length





def main():
	#testMemoryTracking()
	#testNoise()
	#testProcedure([farach, naive, mccreight], [random_data])

	# testProcedure([farach], [random_data])


if __name__ == '__main__':
	main()

