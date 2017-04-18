import farach
from utils import Node
import random
import string
import traceback
import time


def runFarach(inputstr):
	S = farach.str2int(inputstr)
	tree = farach.construct_suffix_tree(S)


def main():
	for i in range(1, 100000, 1000):
		S = ''.join(random.choice(string.digits) for _ in range(i))
		start = time.time()
		correct_tree = runFarach(S)
		end = time.time()

		print("%i, %f" % (i, (end - start)))

if __name__ == '__main__':
	main()

