import farach
from utils import Node
import random
import string
import traceback
import time
import mccreight
import naive

def testRandomStringWithMultipleIterations(algorithm):
	iterations = 5
	for i in range(1, 100000, 1000):
		totalTime = 0

		for j in range(iterations):
			S = ''.join(random.choice(string.digits) for _ in range(i))
			inputstr = farach.str2int(S)
			start = time.time()
			tree = algorithm.construct_suffix_tree(inputstr)
			end = time.time()
			totalTime += (end - start)

		print(i, ",", (totalTime / iterations))

def main():
	testRandomStringWithMultipleIterations(naive)

if __name__ == '__main__':
	main()

