import farach
from utils import Node, str2int
import random
import string
import traceback
import time
import mccreight
import naive
import check_correctness

# commit e6d458690371c0e5839b7247167ae92c67f53739 for mccreight without dict
# remember to change line 143 and 35
def getAverageForString(S, algorithm):
	totalTime = 0
	iterations = 5
	tree = None
	minimum = float("inf")
	maximum = 0
	for j in range(iterations):
			start = time.time()
			tree = algorithm.construct_suffix_tree(S)
			end = time.time()
			totalTime += (end - start)
			minimum = min(minimum, (end-start))
			maximum = max(maximum, (end-start))
	totalTime = totalTime - minimum
	totalTime = totalTime - maximum
	return totalTime / (iterations-2), tree




def testRandomStringWithMultipleIterations(algorithms):
	for i in range(1, 100000, 100):
		totalTime = 0
		S = [i for n in range(i)]
		results = []
		for alg in algorithms:
			data = alg[1](i)
			if len(alg[1](i)) <= 1:
				continue
			ret = getAverageForString(data, alg[0])
			results.append(ret[0])

			if len(alg) == 3 and alg[2]:
				ret[1].update_leaf_list()
				check_correctness.check_correctness(ret[1], data)

			f = open("testData/" + alg[0].__name__ + "_" + alg[1].__name__, 'a')
			f.write(str(i)+", " + ", ".join(map(str, results)) + "\n")  # python will convert \n to os.linesep
			f.close()

	

def testNoise():
	i = 0
	while True:
		i += 1000*100
		for n in range(100):
			start = time.time()
			testArray = [None]*100
			for t in range(i):
				testArray[2] = t * 2 % 3
			end = time.time()
			f = open("testData/noise.txt", 'a')
			f.write(str(i)+"," + str((end - start)) + "\n")  # python will convert \n to os.linesep
			f.close()

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

def random_data(i):
	return str2int(''.join(random.choice(string.digits) for _ in range(i)))

def main():
	testNoise()
	#testRandomStringWithMultipleIterations([(farach, fibonacci)])

if __name__ == '__main__':
	main()

