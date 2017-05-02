import farach
from utils import Node
import random
import string
import traceback
import time
import mccreight

def runFarach(inputstr):
	S = farach.str2int(inputstr)
	tree = farach.construct_suffix_tree(S)


def main():

	for i in range(1, 100000, 1000):
		S = ''.join(random.choice(string.digits) for _ in range(i))
		start = time.time()
		tree = mccreight.construct_suffix_tree(farach.str2int(S))
		#correct_tree = runFarach(S)
		end = time.time()
		i += 1000
		print(i, ",", (end - start))

if __name__ == '__main__':
	main()

