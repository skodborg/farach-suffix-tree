from utils import Node
import math


_height = None
_binaryDict = dict()
L = dict()
P = dict()

def preprocess(tree):
	global _height, _binaryDict, L, P

	currPREORDER = 1
	def preorder(node):
		nonlocal currPREORDER
		P[currPREORDER] =  node
		node.PREORDER = currPREORDER
		currPREORDER += 1
	tree.dfs(preorder)
	

	def createInlabels(node):
		if node.id != "root":
			if node.is_leaf():
				node.INLABEL = node.PREORDER

			parent = node.parent
			INLABEL = node.INLABEL

			if hasattr(parent, "INLABEL"):
				if leastSignificantBit(parent.INLABEL) > leastSignificantBit(INLABEL):
					INLABEL = parent.INLABEL

			if leastSignificantBit(parent.PREORDER) > leastSignificantBit(INLABEL):
				INLABEL = parent.PREORDER

			parent.INLABEL = INLABEL
		
		L[node.INLABEL] =  node

	dfs(tree, createInlabels)

	log2 = math.log(currPREORDER, 2)
	_height = math.ceil(log2) - 1

	binaryTree = createBinaryTree(_height)

	binaryNum = 1

	def binaryNumAlloc(node):
		nonlocal binaryNum
		node.numbering = binaryNum

		_binaryDict[binaryNum] = node

		if binaryNum in L:
			L[binaryNum].binaryNode = node
		binaryNum += 1

	fnOnBinaryTree(binaryTree, binaryNumAlloc)

	def createAncestor(node):
		
		if node.parent != None:
			node.bitList = node.parent.bitList
			node.bitList = shiftBitBasedOnHeight(node.bitList, L[node.INLABEL].binaryNode.bheight)

		for child in node.children:
			createAncestor(child)
		
	tree.bitList = shiftBitBasedOnHeight(0, L[tree.INLABEL].binaryNode.bheight)
	createAncestor(tree)



def findAncestorInBinaryTree(i,j):
	if i.dfsNumbering <= j.dfsNumbering and j.dfsNumbering < (i.dfsNumbering + i.ancestors):
		return i

	if j.dfsNumbering <= i.dfsNumbering and i.dfsNumbering < (j.dfsNumbering + j.ancestors):
		return j

	xor = i.numbering ^ j.numbering	
	msfBit = mostSignificantBitLeft(xor)

	curr = i.numbering >> (_height - msfBit)
	curr = curr | 1
	curr = curr << (_height - msfBit)
 
	return _binaryDict[curr]

def shiftBitBasedOnHeight(bit, height):
	# Shifting the i'th bit, where i = height, so that bit[i] = 1
	height = 2**height
	return bit | height


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
	currNum = 0

	def helper(node):
		nonlocal currNum
		node.dfsNumbering = currNum
		currNum += 1

	tree.dfs(helper)
	return tree


def dfs(tree, fn):
	for child in tree.children:
		dfs(child, fn)
	fn(tree)


def fnOnBinaryTree(tree, fn):
	if tree.children:
		fnOnBinaryTree(tree.children[0], fn)
		fn(tree)
		fnOnBinaryTree(tree.children[1], fn)
	else:
		fn(tree)

def mostSignificantBit(x):
	return ((x).bit_length() - 1)


def mostSignificantBitLeft(x):
	return _height - ((x).bit_length() - 1)


def leastSignificantBit(x):
	"""http://stackoverflow.com/questions/5520655/return-index-of-least-significant-bit-in-python
    Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
	return (x&-x).bit_length()-1




def query(x, y):

	i_x = L[x.INLABEL]
	i_y = L[y.INLABEL]
	#b_ancestor = findAncestorInBinaryTree(L[x.INLABEL].binaryNode,L[y.INLABEL].binaryNode)

	#j = b_ancestor.bheight
	# TODO: done preprocess a binary tree that you dont use, moron


	if i_x.INLABEL ^ i_y.INLABEL > 0:
		j_2 = math.floor(math.log(i_x.INLABEL ^ i_y.INLABEL, 2))
	else: 
		j_2 = 0
	
	j_3 = leastSignificantBit(i_x.INLABEL)

	j_4 = leastSignificantBit(i_y.INLABEL)
	j_2 = max(j_2, j_3)
	j_2 = max (j_2, j_4)
	j = j_2
	if j != j_2:

		print("%i, %i" % (j, j_2))

		# print(bin(i_x.INLABEL))
		# print(bin(i_y.INLABEL))
		i = L[x.INLABEL].binaryNode
		j2 = L[y.INLABEL].binaryNode
		if i.dfsNumbering <= j2.dfsNumbering and j2.dfsNumbering < (i.dfsNumbering + i.ancestors):
			#print ("is child of")
			pass

		elif j2.dfsNumbering <= i.dfsNumbering and i.dfsNumbering < (j2.dfsNumbering + j2.ancestors):
			#print("is child of")
			pass
		else:
			print("ERRROR!!!")




	x_temp_bitList = (x.bitList >> j) << j
	y_temp_bitList = (y.bitList >> j) << j

	total_list = y_temp_bitList & x_temp_bitList

	j = leastSignificantBit(total_list)
	
	# STEP 3:
	pos_l = leastSignificantBit(x.bitList)
	x_bar = None
	if pos_l == j:
		x_bar = x
	elif pos_l < j:
		temp_bitList = (x.bitList >> j) << j
		temp_bitList = temp_bitList ^ x.bitList
		pos_k = mostSignificantBit(temp_bitList)

		i_x_temp = i_x.INLABEL >> pos_k
		i_x_temp = i_x_temp | 1
		i_x_temp = i_x_temp << pos_k

		x_bar = L[P[i_x_temp].INLABEL].parent


	# STEP 3 AGAIN!:
	pos_l = leastSignificantBit(y.bitList)
	y_bar = None

	if pos_l == j:
		y_bar = y

	elif pos_l < j:
		temp_bitList = (y.bitList >> j ) << j 
		temp_bitList = temp_bitList ^ y.bitList
		pos_k = mostSignificantBit(temp_bitList)

		i_y_temp = i_y.INLABEL >> pos_k
		i_y_temp = i_y_temp | 1
		i_y_temp = i_y_temp << pos_k

		y_bar = L[P[i_y_temp].INLABEL].parent


	z = x_bar
	if y_bar.PREORDER < x_bar.PREORDER:
		z = y_bar
	return z