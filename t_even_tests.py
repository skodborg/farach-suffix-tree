import farach
import utils

def start_tests():
	#test_even_tree_for_string_1()
	test_even_tree_for_string_2()


def test_even_tree_for_string_1():
	inputstr = "11112122"

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)

	print("t_even")

	root = utils.Node(aId="root")

	inner = utils.Node("1", "inner")

	root.add_child(inner)
	root.add_child(utils.Node("2", 8))

	inner.add_child(utils.Node("112122", 2))

	inner2 = utils.Node("2", "inner2")
	inner.add_child(inner2)

	inner2.add_child(utils.Node("122", 4))
	inner2.add_child(utils.Node("2", 6))

	assert t_even.fancyprint() == root.fancyprint()

def test_even_tree_for_string_2():
	# aaaaabbabb
	# 1111122122
	inputstr = "1111122122"

	t_odd = farach.T_odd(inputstr)

	t_even = farach.T_even(t_odd, inputstr)


	root = utils.Node(aId="root")

	inner = utils.Node("1", "inner")
	inner2 = utils.Node("1", "inner")
	inner.add_child(inner2)
	inner.add_child(utils.Node("22", 8))

	

	inner2.add_child(utils.Node("1122122", 2))
	inner2.add_child(utils.Node("22122", 4))




	root.add_child(inner)

	root.add_child(utils.Node("22122", 6))
	root.add_child(utils.Node("2", 10))

	print("t_even:")
	print(t_even.fancyprint())

	print("root:")
	print(root.fancyprint())

	assert(t_even.fancyprint() == root.fancyprint())




def main():
	start_tests()

if __name__ == '__main__':
	main()