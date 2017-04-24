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
	total = []
	i = 999
	# for i in range(1, 100000, 1000):
	while True:
		S = ''.join(random.choice(string.digits) for _ in range(i))
		start = time.time()
		correct_tree = runFarach(S)
		end = time.time()
		total.append((i, (end-start)))
		i += 1000
		# print("Total:")
		# for n, t in total:
		# 	if n == 1:
		# 		continue
		# 	print("%i, %f" % (n, t))

if __name__ == '__main__':
	main()

