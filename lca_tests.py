from utils import Node
import lca



def createTreeOne():
	rootNode = Node(aStrLength=0, aId="root")

	n1_l = Node(aId="inner",aStrLength=1,)
	n1_r = Node(aId="inner", aStrLength=1)

	rootNode.add_child(n1_l)
	rootNode.add_child(n1_r)


	n2_1_l = Node(aId=1, aStrLength=2)
	n2_1_r = Node(aId=2, aStrLength=2)

	n1_l.add_child(n2_1_l)
	n1_l.add_child(n2_1_r)

	n2_2_l = Node(aId=3, aStrLength=2)
	n2_2_r = Node(aId=4, aStrLength=2)

	n1_r.add_child(n2_2_l)
	n1_r.add_child(n2_2_r)

	return rootNode, [n2_1_l, n2_1_r, n2_2_l, n2_2_r]

def createTreeTwo():
	rootNode = Node(aStrLength=0, aId="root")
	inner1 = Node(aId="inner1")
	inner2 = Node(aId="inner2")
	rootNode.add_child(inner1)
	rootNode.add_child(inner2)


	nodes = []

	nodes.append(Node(aId=1))
	nodes.append(Node(aId=2))
	nodes.append(Node(aId=3))
	nodes.append(Node(aId=4))
	nodes.append(Node(aId=5))
	nodes.append(Node(aId=6))

	inner1.add_child(nodes[0])
	inner1.add_child(nodes[1])

	nodes.append(inner1)

	nodes.append(inner2)

	inner2_1 = Node(aId="inner2_1")

	inner2.add_child(nodes[2])
	inner2.add_child(nodes[3])
	inner2.add_child(inner2_1)



	nodes.append(inner2_1)



	inner2_1.add_child(nodes[4])
	inner2_1.add_child(nodes[5])

	return rootNode, nodes


def test1():
	tree, nodes = createTreeTwo()

	print(tree.fancyprint(S="121232", onlylengths=True))
	lca.preprocess(tree)
	print(tree.fancyprintLCA())
	print(nodes)
	lca.query(nodes[7], nodes[8])

	assert bin(lca.query(nodes[7], nodes[8]).PREORDER) == bin(5)
	assert bin(lca.query(nodes[0], nodes[1]).PREORDER) == bin(2)
	assert bin(lca.query(nodes[1], nodes[3]).PREORDER) == bin(1)
	assert bin(lca.query(nodes[1], nodes[4]).PREORDER) == bin(1)
	assert bin(lca.query(nodes[1], nodes[5]).PREORDER) == bin(1)
	assert bin(lca.query(nodes[0], nodes[5]).PREORDER) == bin(1)


	assert bin(lca.query(nodes[4], nodes[5]).PREORDER) == bin(8)

	print("well done")


def runTests():
	test1()


def main():
	runTests()

if __name__ == '__main__':
	main()