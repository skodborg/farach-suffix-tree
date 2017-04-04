from utils import Node
import math

_height = None
_binaryDict = dict()
_numbToTreeNode = dict()
L = dict()
P = dict()

def preprocess(tree):
	global _height, _binaryDict, L, P
	currPREORDER = 1


	def helper(node):
		nonlocal currPREORDER

		P[currPREORDER] =  node
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
			
			# if hasattr(node, "INLABEL"):
			# 	# IS LEAF??
			# 	# TODO: CHANGE THIS???
			# 	if leastSignificantBit(INLABEL) < leastSignificantBit(node.INLABEL):
			# 		INLABEL = node.INLABEL

			# node.INLABEL = INLABEL

			if hasattr(parent, "INLABEL"):
				if leastSignificantBit(parent.INLABEL) > leastSignificantBit(INLABEL):
					L[INLABEL] =  node
	
					INLABEL = parent.INLABEL

			if leastSignificantBit(parent.PREORDER) > leastSignificantBit(INLABEL):
				L[INLABEL] =  node
				INLABEL = parent.PREORDER


			parent.INLABEL = INLABEL

			#DID THIS; REDO TOMORROW
			L[node.INLABEL] =  node

			print("INLABEL: " + str(INLABEL) + " node: " + str(node.id))


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
		
		if node.parent != None:
			node.bitList = node.parent.bitList
			node.bitList = shiftBitBasedOnHeight(node.bitList, L[node.INLABEL].binaryNode.bheight)

		for child in node.children:
			createAncestor(child)
			
		# if node.is_leaf():
		# 	# Reallocating enough zeros to cover all heights
		# 	bitList = 0
		# 	node.bitList = bitList

		# 	currList = shiftBitBasedOnHeight(bitList, L[node.INLABEL].binaryNode.height)
		# else:
		# 	currList = 0
		# 	for child in node.children:
		# 		bitList = createAncestor(child)

		# 		# Merging the two bitlists, so that all bits that are 1 are one in the new list
		# 		currList = currList | bitList

		# 	node.bitList = currList
			
	tree.bitList = shiftBitBasedOnHeight(0, L[tree.INLABEL].binaryNode.bheight)
	createAncestor(tree)
	print(binaryTree.fancyprintBinaryTree())



def findAncestorInBinaryTree(i,j):
	if i.dfsNumbering <= j.dfsNumbering and j.dfsNumbering < (i.dfsNumbering + i.ancestors):
		print("eh")
		return i

	if j.dfsNumbering <= i.dfsNumbering and i.dfsNumbering < (j.dfsNumbering + j.ancestors):
		return j


	xor = i.numbering ^ j.numbering
	
	msfBit = msf(xor)

	curr = i.numbering >> (_height - msfBit)
	curr = curr | 1
	curr = curr << (_height - msfBit)
 

	return _binaryDict[curr]
	
def msf(x):
	return _height - ((x).bit_length() - 1)


def shiftBitBasedOnHeight(bit, height):
	# Shifting the i'th bit, where i = height, so that bit[i] = 1
	

	height = 2**height
	return bit | height

def isBitSat(bit, i):
	return bit & 2**(i-1) == 2**(i-1)


def createBinaryTree(total_height):
	tree = Node(aId=0)
	tree.bheight = total_height

	
	def helper(c_tree, height):

		if height >= 0:
			left = Node(aId=height)
			left.bheight= height
			right = Node(aId=height)
			right.bheight = height
			c_tree.add_child(left)
			c_tree.add_child(right)

			c_tree.ancestors = 1
			c_tree.ancestors += helper(left, height-1)
			c_tree.ancestors += helper(right, height-1)


		else:
			c_tree.ancestors = 1
		return c_tree.ancestors



	helper(tree, total_height-1)	
	print("tree.height= " + str(tree.children[0].children[0].bheight))

	currNum = 0

	def helper(node):
		nonlocal currNum
		node.dfsNumbering = currNum
		currNum += 1

	tree.dfs(helper)

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
	if ((x).bit_length() == 0):
		return _height
	return _height - ((x).bit_length() - 1)

def mostSignificantBit2(x):
	return ((x).bit_length() - 1)


def leastSignificantBit(x):
	"""http://stackoverflow.com/questions/5520655/return-index-of-least-significant-bit-in-python
    Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
	return (x&-x).bit_length()-1

def query(x, y):
	print("x id: %s; : %s" % (str(x.id), bin(x.PREORDER)))
	print(bin(x.bitList))
	print("y %s : %s" % (str(y.id), bin(y.PREORDER)))
	print(bin(y.bitList))

	i_x = L[x.INLABEL]
	i_y = L[y.INLABEL]

	print(L)
	print("i: %i, j: %i" % (L[x.INLABEL].binaryNode.numbering,L[y.INLABEL].binaryNode.numbering))
	b_ancestor = findAncestorInBinaryTree(L[x.INLABEL].binaryNode,L[y.INLABEL].binaryNode)

	print("result: %i" % b_ancestor.numbering)


	j = b_ancestor.bheight

	print(b_ancestor)

	print("height of binary node:")
	print(j)



	print("-"*50)
	print(bin(x.bitList))
	print(bin(y.bitList))
	print("."*50)

	x_temp_bitList = (x.bitList >> j) << j

	y_temp_bitList = (y.bitList >> j) << j

	print(bin(x_temp_bitList))
	print(bin(y_temp_bitList))

	# x_list = x.bitList >> j
	# y_list = y.bitList >> j

	# total_list = x_list & y_list



	total_list = y_temp_bitList & x_temp_bitList

	print(bin(total_list))

	#j = (_height - leastSignificantBit(total_list)) + j


	# TODO: minimum?
	print("LSF: %i " % leastSignificantBit(total_list))
	print("J: %i" % j)
	j = leastSignificantBit(total_list)
	print("J: %i" % j)

	print(L)
	# STEP 3:
	pos_l = leastSignificantBit(x.bitList)
	print("j: %i"%j)
	print("l: %i"%pos_l)
	x_bar = None
	if pos_l == j:
		print("HERE TOO")
		x_bar = x
	elif pos_l < j:

		temp_bitList = (x.bitList >> j) << j
		temp_bitList = temp_bitList ^ x.bitList
		print("bitlist: " + bin(x.bitList))
		print("temp_bitList: " + bin(temp_bitList))
		pos_k = mostSignificantBit2(temp_bitList)
		print("POS_K: %i" % pos_k)
		i_x_temp = i_x.INLABEL >> pos_k
		i_x_temp = i_x_temp | 1
		i_x_temp = i_x_temp << pos_k
		print("i_x.INLABEL: " + bin(i_x.INLABEL))
		print("i_x_temp: " + bin(i_x_temp))
		print("PREORDER")
		print(L)
		print(pos_k)
		print(P[i_x_temp].INLABEL)
		x_bar = L[P[i_x_temp].INLABEL].parent
		print(P[i_x_temp].PREORDER)
		print(bin(x_bar.PREORDER))

	# STEP 3 AGAIN!:
	pos_l = leastSignificantBit(y.bitList)


	print("FIND Y")
	print(bin(y.bitList))
	y_bar = None

	if pos_l == j:
		print("IN HERE")
		y_bar = y
	elif pos_l < j:

		print(bin(y.bitList))
		temp_bitList = (y.bitList >> j ) << j 
		temp_bitList = temp_bitList ^ y.bitList
		print("y.bitList : " + bin(y.bitList))
		print("y temp list : " + bin(temp_bitList))
		pos_k = mostSignificantBit2(temp_bitList)

		i_y_temp = i_y.INLABEL >> pos_k
		i_y_temp = i_y_temp | 1
		i_y_temp = i_y_temp << pos_k

		print("i_y.INLABEL: " + bin(i_y.INLABEL))
		print("i_y_temp: " + bin(i_y_temp))

		print("preorder : " + str(P[i_y_temp].PREORDER))
		y_bar = L[P[i_y_temp].INLABEL].parent

		print("post_k: " + str(pos_k))
		print(bin(y_bar.PREORDER))


	z = x_bar
	print(bin(y_bar.PREORDER) +  " < " + bin(x_bar.PREORDER))
	if y_bar.PREORDER < x_bar.PREORDER:

		z = y_bar

	print("Common ancestor is " + bin(z.PREORDER)) 
	return z


def main():
    pass


if __name__ == '__main__':
    main()
