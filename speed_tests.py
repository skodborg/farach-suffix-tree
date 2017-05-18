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
	iterations = 3
	# maxTime = 5*60  #sekunder

	timeTaken = dict()

	for i in range(10*1000, 34000000000*1000, 50*1000):

		for data_func in data_functions:
			# data = data_func(i)
			# rnd_data = data_func(a_size)

			for alg in algorithms:
			
				for i_pow in range(14, 18):
					for _ in range(iterations):
						data = data_func(2**i_pow)(i)
						uniq = len(set(data))

						start = time.time()

						tree = alg.construct_suffix_tree(data)
						end = time.time()
						t = end-start
						totalNodes = tree.totalNodes() - len(data)

						f = open("testData/compare_night_" + str(i_pow) + "_" + alg.__name__ + "_" + data_func.__name__, 'a')
						f.write(str(i)+", "  + str(t) + "," + str(totalNodes) +  "," + str(uniq) +  "\n") 
						f.close()
		print(i)

def test_varying_alphabet_size():
	iterations = 5
	start = time.time()
	naive.construct_suffix_tree(different_char(10000))
	end = time.time()

	print("base: " + str(end-start))
	for i in range(2, 50):
		a_size = 2**i

		rnd_data = random_data_varying_alphabet(a_size)

		for _ in range(iterations):
			start = time.time()
			S = rnd_data(100*1000)
			naive.construct_suffix_tree(S)
			end = time.time()
			print(len(S))

			t = end-start

			f = open("testData/naive_alphabet_size_varying_random_data", 'a')
			f.write(str(a_size)+", "  + str(t)  +  "\n") 
			f.close()


	

def testNoise():
	i = 1
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
	#return [n for n in range(i)]
	l = [n for n in range(i)]
	random.shuffle(l)
	return l
	#return str2int(''.join(random.choice([str(n) for n in range(i)]) for _ in range(i)))

def random_data(i):
	return str2int(''.join(random.choice(string.digits) for _ in range(i)))

def random_data_varying_alphabet(length):
		def helper(i):

			return str2int([str(random.randint(0,length)) for _ in range(i)])
		return helper
def random_data_fixed_alphabet(i):
	return str2int([str(random.randint(0,20*1000)) for _ in range(i)])
	
def same_char(length):
	return [0]*length





def main():
	#testMemoryTracking()
	#testNoise()
	
	# for i in range(10,24):

	# 	data_func = random_data_varying_alphabet(2**i)
	# 	S = data_func(10*1000)
	# 	chars = set()
	# 	for c in S:
	# 		chars.add(c)

	# 	start = time.time()
	# 	tree = naive.construct_suffix_tree(S)
	# 	print("-"*50)
	# 	print("num of children on averge: " + str(tree.averageLeafs()))
	# 	print("uniq len: " + str(len(chars)))
	# 	print("leafs from root: " + str(tree.leafs_from_root()))
	# 	totalN = tree.totalNodes()
	# 	print("total nodes: " + str(totalN))
	# 	print("inner node: " + str(totalN-len(S)))
	# 	print("time: " + str(time.time()-start))
	# 	print("depth: " + str(tree.depth()))
		# join(random.choice([str(n) for n in range(i)]) for _ in range(i))
	testProcedure([farach, mccreight], [random_data_varying_alphabet])
		# test_varying_alphabet_size()
		# testProcedure([farach], [random_data])


if __name__ == '__main__':
	main()

