from utils import Node
import math



class LCA:
    L = dict()
    P = dict()

    def __init__(self):
        L = dict()
        P = dict()

    def preprocess(self, tree):
        def cleanup(node):
            if hasattr(node, 'INLABEL'):
                delattr(node, 'INLABEL')
            if hasattr(node, 'PREORDER'):
                delattr(node, 'PREORDER')
            if hasattr(node, 'bitList'):
                delattr(node, 'bitList')
        tree.dfs(cleanup)


        currPREORDER = 1
        def preorder(node):
            nonlocal currPREORDER
            self.P[currPREORDER] =  node
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
                    if self.leastSignificantBit(parent.INLABEL) > self.leastSignificantBit(INLABEL):
                        INLABEL = parent.INLABEL

                if self.leastSignificantBit(parent.PREORDER) > self.leastSignificantBit(INLABEL):
                    INLABEL = parent.PREORDER

                parent.INLABEL = INLABEL
            
            self.L[node.INLABEL] =  node

        self.dfs(tree, createInlabels)

        def createAncestor(node):
            
            if node.parent != None:
                node.bitList = node.parent.bitList
                node.bitList = self.shiftBitBasedOnHeight(node.bitList, self.leastSignificantBit(node.INLABEL))

            for child in node.children:
                createAncestor(child)
            
        tree.bitList = self.shiftBitBasedOnHeight(0, self.leastSignificantBit(tree.INLABEL))
        createAncestor(tree)



    def shiftBitBasedOnHeight(self, bit, height):
        # Shifting the i'th bit, where i = height, so that bit[i] = 1
        height = 2**height
        return bit | height

    def dfs(self, tree, fn):
        for child in tree.children:
            self.dfs(child, fn)
        fn(tree)

    def mostSignificantBit(self, x):
        if x == 0:
            return 0
        return math.floor(math.log(x, 2))

    def leastSignificantBit(self, x):
        return self.mostSignificantBit(x&-x)

    def query(self, x, y):
        j = self.mostSignificantBit(x.INLABEL ^ y.INLABEL)

        j = max(j, self.leastSignificantBit(x.INLABEL), self.leastSignificantBit(y.INLABEL))

        x_temp_bitList = (x.bitList >> j) << j
        y_temp_bitList = (y.bitList >> j) << j

        total_list = y_temp_bitList & x_temp_bitList

        j = self.leastSignificantBit(total_list)
        
        # STEP 3:
        pos_l = self.leastSignificantBit(x.bitList)
        x_bar = None
        if pos_l == j:
            x_bar = x
        elif pos_l < j:
            temp_bitList = (x.bitList >> j) << j
            temp_bitList = temp_bitList ^ x.bitList
            pos_k = self.mostSignificantBit(temp_bitList)

            x_temp = x.INLABEL >> pos_k
            x_temp = x_temp | 1
            x_temp = x_temp << pos_k

            x_bar = self.L[self.P[x_temp].INLABEL].parent


        # STEP 3 AGAIN!:
        pos_l = self.leastSignificantBit(y.bitList)
        y_bar = None

        if pos_l == j:
            y_bar = y

        elif pos_l < j:
            temp_bitList = (y.bitList >> j ) << j 
            temp_bitList = temp_bitList ^ y.bitList
            pos_k = self.mostSignificantBit(temp_bitList)

            y_temp = y.INLABEL >> pos_k
            y_temp = y_temp | 1
            y_temp = y_temp << pos_k

            y_bar = self.L[self.P[y_temp].INLABEL].parent


        z = x_bar
        if y_bar.PREORDER < x_bar.PREORDER:
            z = y_bar

        return z