import farach
from utils import Node
import random
import string
import traceback
import time
import mccreight
import naive
# commit e6d458690371c0e5839b7247167ae92c67f53739 for mccreight without dict
# remember to change line 143 and 35
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
	for i in range(1, 100000, 100):
		totalTime = 0
		#S = ''.join(random.choice(string.digits) for _ in range(i))
		S = [i for n in range(i)]
		#inputstr = farach.str2int(S)
		results = []
		for alg in algorithms:
			results.append(getAverageForString(S, alg))

		print(str(i)+", " + ", ".join(map(str, results)))

def main():
	testRandomStringWithMultipleIterations([farach])

if __name__ == '__main__':
	main()

