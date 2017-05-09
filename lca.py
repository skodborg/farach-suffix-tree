from utils import Node
import math



class LCA:

    def __init__(self):
        self.L = dict()
        self.P = dict()

    def preprocess(self, tree):
        def cleanup(node):
            if hasattr(node, 'INLABEL'):
                delattr(node, 'INLABEL')
            if hasattr(node, 'PREORDER'):
                delattr(node, 'PREORDER')
            if hasattr(node, 'ancestors'):
                delattr(node, 'ancestors')
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
                node.ancestors = node.parent.ancestors
                node.ancestors = self.shiftBitBasedOnHeight(node.ancestors, self.leastSignificantBit(node.INLABEL))

            for child in node.children:
                createAncestor(child)
            
        tree.ancestors = self.shiftBitBasedOnHeight(0, self.leastSignificantBit(tree.INLABEL))
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
        # Step 1
        j = self.mostSignificantBit(x.INLABEL ^ y.INLABEL)
        j = max(j, self.leastSignificantBit(x.INLABEL), self.leastSignificantBit(y.INLABEL))

        # Step 2
        x_temp_ancestors = (x.ancestors >> j) << j
        y_temp_ancestors = (y.ancestors >> j) << j

        total_list = y_temp_ancestors & x_temp_ancestors

        j = self.leastSignificantBit(total_list)
        
        # Step 3 & 4
        x_bar = self.findNodeClosestToRun(j, x)
        y_bar = self.findNodeClosestToRun(j, y)

        # Step 5
        z = x_bar
        if y_bar.PREORDER < x_bar.PREORDER:
            z = y_bar

        return z

    def findNodeClosestToRun(self, j, node):

        pos_l = self.leastSignificantBit(node.ancestors)
        node_bar = None
        # Step 3
        if pos_l == j:
            node_bar = node
        #Step 4
        elif pos_l < j:
            temp_ancestors = (node.ancestors >> j) << j
            temp_ancestors = temp_ancestors ^ node.ancestors

            pos_k = self.mostSignificantBit(temp_ancestors)

            node_temp = node.INLABEL >> pos_k
            node_temp = node_temp | 1
            node_temp = node_temp << pos_k

            node_bar = self.L[self.P[node_temp].INLABEL].parent

        return node_bar

        