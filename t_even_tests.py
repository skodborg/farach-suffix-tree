import farach
import utils

def run_tests():
	test_even_tree_for_string_1()
	test_even_tree_for_string_2()
	print('tests succeeded!')


def test_even_tree_for_string_1():
	inputstr = utils.str2int("11112122")

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)

	root = utils.Node(aId="root")

	inner = utils.Node(1, "inner")

	root.add_child(inner)
	root.add_child(utils.Node(1, 8))

	inner.add_child(utils.Node(7, 2))

	inner2 = utils.Node(2, "inner")
	inner.add_child(inner2)

	inner2.add_child(utils.Node(5, 4))
	inner2.add_child(utils.Node(3, 6))

	root.update_leaf_list()
	
	assert t_even.fancyprint(inputstr) == root.fancyprint(inputstr)

def test_even_tree_for_string_2():
	# aaaaabbabb
	# 1111122122
	inputstr = farach.str2int('1111122122')

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)

	root = utils.Node(aId="root")

	inner = utils.Node(1, "inner")
	inner2 = utils.Node(2, "inner")
	inner.add_child(inner2)
	inner.add_child(utils.Node(3, 8))

	inner2.add_child(utils.Node(9, 2))
	inner2.add_child(utils.Node(7, 4))

	root.add_child(inner)

	root.add_child(utils.Node(5, 6))
	root.add_child(utils.Node(1, 10))

	root.update_leaf_list()
	
	# print("t_even:")
	# print(t_even.fancyprint(inputstr))

	# print("root:")
	# print(root.fancyprint(inputstr))

	assert(t_even.fancyprint(inputstr) == root.fancyprint(inputstr))


def main():
	run_tests()

if __name__ == '__main__':
	main()