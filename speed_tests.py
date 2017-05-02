import farach
from utils import Node
import random
import string
import traceback
import time
import mccreight
import naive

def getAverageForString(S, algorithm):
	totalTime = 0
	iterations = 5
	for j in range(iterations):
			start = time.time()
			tree = algorithm.construct_suffix_tree(S)
			end = time.time()
			totalTime += (end - start)
	return totalTime / iterations

def testRandomStringWithMultipleIterations(algorithms):
	iterations = 5
	for i in range(1, 100000, 1000):
		totalTime = 0
		S = ''.join(random.choice(string.digits) for _ in range(i))
		inputstr = farach.str2int(S)
		results = []
		for alg in algorithms:
			results.append(getAverageForString(inputstr, alg))

		print(str(i)+", " + ", ".join(map(str, results)))

def main():
	testRandomStringWithMultipleIterations([naive, mccreight, farach])

if __name__ == '__main__':
	main()

