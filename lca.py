from utils import Node
import math

L = dict()
P = dict()

def preprocess(tree):
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

	def createAncestor(node):
		
		if node.parent != None:
			node.bitList = node.parent.bitList
			node.bitList = shiftBitBasedOnHeight(node.bitList, leastSignificantBit(node.INLABEL))

		for child in node.children:
			createAncestor(child)
		
	tree.bitList = shiftBitBasedOnHeight(0, leastSignificantBit(tree.INLABEL))
	createAncestor(tree)


def shiftBitBasedOnHeight(bit, height):
	# Shifting the i'th bit, where i = height, so that bit[i] = 1
	height = 2**height
	return bit | height

def dfs(tree, fn):
	for child in tree.children:
		dfs(child, fn)
	fn(tree)

def mostSignificantBit(x):
	if x == 0:
		return 0
	return math.floor(math.log(x, 2))

def leastSignificantBit(x):
	return mostSignificantBit(x&-x)

def query(x, y):

	i_x = L[x.INLABEL]
	i_y = L[y.INLABEL]

	j = mostSignificantBit(i_x.INLABEL ^ i_y.INLABEL)

	j = max(j, leastSignificantBit(i_x.INLABEL), leastSignificantBit(i_y.INLABEL))

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