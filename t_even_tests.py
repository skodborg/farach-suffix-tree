import farach
import utils

def run_tests():
	test_even_tree_for_string_1()
	test_even_tree_for_string_2()
	print('tests succeeded!')


def test_even_tree_for_string_1():
	inputstr = farach.str2int("11112122")

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)

	root = utils.Node(aId="root")

	inner = utils.Node([1], "inner")

	root.add_child(inner)
	root.add_child(utils.Node([2], 8))

	inner.add_child(utils.Node([1,1,2,1,2,2], 2))

	inner2 = utils.Node([2], "inner2")
	inner.add_child(inner2)

	inner2.add_child(utils.Node([1,2,2], 4))
	inner2.add_child(utils.Node([2], 6))
	
	assert t_even.fancyprint() == root.fancyprint()

def test_even_tree_for_string_2():
	# aaaaabbabb
	# 1111122122
	inputstr = farach.str2int('1111122122')

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)

	root = utils.Node(aId="root")

	inner = utils.Node([1], "inner")
	inner2 = utils.Node([1], "inner")
	inner.add_child(inner2)
	inner.add_child(utils.Node([2,2], 8))

	inner2.add_child(utils.Node([1,1,2,2,1,2,2], 2))
	inner2.add_child(utils.Node([2,2,1,2,2], 4))

	root.add_child(inner)

	root.add_child(utils.Node([2,2,1,2,2], 6))
	root.add_child(utils.Node([2], 10))

	# print("t_even:")
	# print(t_even.fancyprint())

	# print("root:")
	# print(root.fancyprint())

	assert(t_even.fancyprint() == root.fancyprint())


def main():
	run_tests()

if __name__ == '__main__':
	main()