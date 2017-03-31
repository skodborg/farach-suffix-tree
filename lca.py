from utils import Node
import math

_height = None
_binaryDict = dict()
L = dict()

def preprocess(tree):
	global _height, _binaryDict, L
	currPREORDER = 1


	def helper(node):
		nonlocal currPREORDER


		node.PREORDER = currPREORDER
		currPREORDER += 1


	tree.dfs(helper)
	

	def helper(node):

		if node.id != "root":
			if node.is_leaf():
				node.INLABEL = node.PREORDER
				L[node.INLABEL] =  node
				
			parent = node.parent

			INLABEL = node.INLABEL
			
			if hasattr(node, "INLABEL"):
				if leastSignificantBit(INLABEL) < leastSignificantBit(node.INLABEL):
					INLABEL = node.INLABEL

			node.INLABEL = INLABEL

			if hasattr(parent, "INLABEL"):
				if leastSignificantBit(parent.INLABEL) > leastSignificantBit(INLABEL):

					L[INLABEL] =  node
	
					INLABEL = parent.INLABEL

			if leastSignificantBit(parent.PREORDER) > leastSignificantBit(INLABEL):
				L[INLABEL] =  node
				INLABEL = parent.PREORDER

			parent.INLABEL = INLABEL

		else:
			L[node.INLABEL] =  node
	fnOnLeafs(tree, helper)

	log2 = math.log(currPREORDER, 2)
	_height = math.ceil(log2) - 1

	binaryTree = createBinaryTree(_height)


	binaryNum = 1

	Lbinary = dict()

	def binaryNumAlloc(node):
		nonlocal binaryNum
		node.numbering = binaryNum
		_binaryDict[binaryNum] = node

		if binaryNum in L:
			#TODO: WHICH OF THESE SHOULD WE USE?

			Lbinary[binaryNum] = node
			node.leader = L[binaryNum]
			L[binaryNum].binaryNode = node
		binaryNum += 1

	fnOnBinaryTree(binaryTree, binaryNumAlloc)

	def createAncestor(node):
		if node.is_leaf():
			# Reallocating enough zeros to cover all heights
			bitList = 2**_height
			node.bitList = bitList

			currList = shiftBitBasedOnHeight(bitList, L[node.INLABEL].binaryNode.height)
		else:
			currList = 0
			for child in node.children:
				bitList = createAncestor(child)

				# Merging the two bitlists, so that all bits that are 1 are one in the new list
				currList = currList | bitList

			node.bitList = currList
			

		
		return currList

	createAncestor(tree)



def findAncestorInBinaryTree(i,j):

	xor = i.numbering ^ j.numbering
	adjust = 0
	if i.numbering % 2 == 0:
		adjust = 1

	msfBit = mostSignificantBit(xor)
	curr = i.numbering >> (_height - msfBit)
	curr = curr | 1
	curr = curr << (_height - msfBit)
	return _binaryDict[curr]
	


def shiftBitBasedOnHeight(bit, height):
	# Shifting the i'th bit, where i = height, so that bit[i] = 1
	height = 2**height
	return bit | height

def isBitSat(bit, i):
	return bit & 2**(i-1) == 2**(i-1)


def createBinaryTree(total_height):
	tree = Node(aId=0)
	tree.height = 0
	def helper(tree, height):
		if height <= total_height:
			left = Node(aId=height)
			left.height= height
			right = Node(aId=height)
			right.height = height
			tree.add_child(left)
			tree.add_child(right)

			helper(left, height+1)
			helper(right, height+1)

	helper(tree, 1)	
	return tree



def fnOnLeafs(tree, fn):


	for child in tree.children:
		fnOnLeafs(child, fn)

	fn(tree)

def fnOnBinaryTree(tree, fn):
	if tree.children:
		fnOnBinaryTree(tree.children[0], fn)
		fn(tree)
		fnOnBinaryTree(tree.children[1], fn)
	else:
		fn(tree)


def mostSignificantBit(x):
	return _height - ((x).bit_length() - 1)


def leastSignificantBit(x):
	"""http://stackoverflow.com/questions/5520655/return-index-of-least-significant-bit-in-python
    Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
	return (x&-x).bit_length()-1

def query(x, y):
	print(L)
	i_x = L[x.INLABEL]
	i_y = L[y.INLABEL]

	b_ancestor = findAncestorInBinaryTree(L[x.INLABEL].binaryNode,L[y.INLABEL].binaryNode)

	j = b_ancestor.height

	x_list = x.bitList >> j
	y_list = y.bitList >> j

	total_list = x_list & y_list

	h_i_z = leastSignificantBit(total_list) + 1 + j



	# STEP 3:
	pos_l = leastSignificantBit(x.bitList)

	x_bar = None


	print(pos_l)
	print(h_i_z)
	if pos_l == j:
		x_bar = x
	elif pos_l < j:
		# TODO: 
		print("NOT IMPLEMENTED YET")
		print(bin(x.bitList))
		temp_bitList = (x.bitList >> j) << j

		temp_bitList = temp_bitList ^ x.bitList
		print(bin(temp_bitList))

		pos_k = mostSignificantBit(temp_bitList)
		print(pos_k)
		print("do shit")
		# bin((int('11100', 2) >> 3) << 3)
		# bin(test ^int('11000', 2))
		

		test = int('11100', 2)
		reset = (~test)
		reset = (~test >> 3) << 3
		test = (~test >> 3) << 3 & test

	# STEP 3 AGAIN!:

	pos_l = leastSignificantBit(y.bitList)

	y_bar = None


	print(pos_l)
	print(h_i_z)
	if pos_l == j:
		y_bar = y
		print("IM HERE")
	elif pos_l < j:
		# TODO: 
		print("NOT IMPLEMENTED YET")


	z = x_bar
	if y_bar.PREORDER < x_bar.PREORDER:
		z = y_bar

	print("Common ancestor is " + str(z)) 



def main():
    pass


if __name__ == '__main__':
    main()
