from itertools import count
import random as rnd
from collections import deque


class Tree:
    def traverse(self, fn):
        ''' also dfs '''
        self._traverse(self.root, fn)

    def _traverse(self, aNode, fn):
        if len(aNode.children) == 0:
            fn(aNode)
        else:
            fn(aNode)
            for child in aNode.children:
                self._traverse(child, fn)

    def dfs(self, fn):
        stack = [self.root]
        while stack:
            node = stack.pop()
            stack += reversed(node.children)
            fn(node)

    def reroot(self, newRoot):
        oldroot = self.root

        def find_path(newRoot):
            path = [newRoot]
            curr_parent = newRoot.parent
            while curr_parent != oldroot:
                path.append(curr_parent)
                curr_parent = curr_parent.parent
            return path

        # reverse all child-parent relations in the subtree from the root
        # containing the new root
        def reverse_relations(child):
            temp_parent = child.parent
            temp_parent.remove_child(child)
            child.add_child(temp_parent)

        def traverse_down(node):
            # cache before reverse_relations (mutates children list for node)
            cached_node_children = node.children

            # make node.parent a child of node, and change parent
            # of node.parent to node
            reverse_relations(node)

            for c in cached_node_children:
                traverse_down(c)

        path = list(reversed(find_path(newRoot)))
        for c in path:
            reverse_relations(c)

        self.root = newRoot

    def as_newick(self):
        return '%s;' % self.root.as_newick()

    def __init__(self, aInput=None):
        self.root = Node(aId='root')
        self.input = aInput

    def __str__(self):
        return self.root.fancyprint()


class Node:
    _ids = count(0)

    def add_child(self, new_child):
        self.children.append(new_child)
        new_child.parent = self

    def remove_child(self, old_child):
        self.children.remove(old_child)
        old_child.parent = None

    def is_leaf(self):
        return len(self.children) == 0

    def update_leaf_list(self):
        self.leaflist = []

        if self.is_leaf():
            return [self]

        for n in self.children:
            self.leaflist = n.update_leaf_list()
            #self.leaflist.extend(n.update_leaf_list())
        return self.leaflist

    def getParentEdge(self, S):
        if self.id == 'root':
            return ''

        if hasattr(self, 'edge'):
            return self.edge

        if self.is_leaf():
            leaf_id = self.id
        else:
            leaf_descendant = self.leaflist[0]
            leaf_id = leaf_descendant.id
        
        return S[leaf_id - 1 + self.parent.str_length : leaf_id - 1 + self.str_length]
    


    

    def printLCPTree(self):

        def helper(node):

            if hasattr(node, "suffix_link"):
                if hasattr(node.suffix_link, "suffix_link_children"):

                    node.suffix_link.suffix_link_children.append(node)
                else:
                    node.suffix_link.suffix_link_children = [node]
        self.bfs(helper)

        def helper(node):
            if hasattr(node, "lcp_depth"):
                print ("%s%s" % ((" " * node.lcp_depth * 2, str(node.id))))
            if hasattr(node, "suffix_link_children"):
                for child in node.suffix_link_children:
                    helper(child)

        helper(self)

                
    def fancyprintBinaryTree(self, level=0):
        self_id = "node : "

    
        self_id += str(self.numbering) + " dfs: " + str(self.dfsNumbering) + " bheight: " + str(self.bheight)

        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprintBinaryTree(level + 1)
        return result

    def fancyprintLCA(self, level=0):
        def ffs(x):
            """Returns the index, counting from 0, of the
            least significant set bit in `x`.
            """
            return (x&-x).bit_length()-1

        self_id = str(self.PREORDER)+":" if self.id else ''

        # TODO: utilize getParentEdge() ??
        if self.is_leaf():
            leaf_id = self.PREORDER

        edge = ""
        if(hasattr(self, "bitList")):
            edge = " bitList=" + str(bin(self.bitList)[2:])

        # printing odd/even nodes for which this node is the LCA
        # if hasattr(self, 'lca_odd') or hasattr(self, 'lca_even'):
        #     edge += ' ['
        #     if hasattr(self, 'lca_odd'):
        #         edge += 'o: %s' % self.lca_odd
        #         if hasattr(self, 'lca_even'):
        #             edge += ', '
        #     if hasattr(self, 'lca_even'):
        #         edge += 'e: %s' % self.lca_even
        #     edge += ']'

        self_id += str(edge)
        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprintLCA(level + 1)
        return result

    def fancyprint_mcc(self, S, level=0):
        self_id = str(self.id) + ':' if self.id else ''

        if self.id == 'root':
            edge = ''
        else:
            leafID = self.leaflist[0].id
            edge = S[leafID + self.parent.str_length:]
            edge += ' len: %i' % self.str_length
            if hasattr(self, 'start'):
                edge += '  (%i,%i)' % (self.start, self.stop)
            if hasattr(self, 'suffix_link'):
                edge += ' sl: %s' % self.suffix_link.str_length

        self_id += str(edge)
        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprint_mcc(S, level + 1)
        return result

    def fancyprint(self, S, level=0, onlylengths=False):


        self_id = str(self.id)+ ":" if self.id else ''

        # TODO: utilize getParentEdge() ??
        if self.is_leaf():
            leaf_id = self.id
        else:
            if not onlylengths:
                leaf_descendant = self.leaflist[0]
                leaf_id = leaf_descendant.id
        if self.id == "root":
            edge = ""
        else:
            if S:
                if not onlylengths:
                    edge =  str(S[leaf_id - 1 + self.parent.str_length : leaf_id - 1 + self.str_length])
                    edge += " len: " + str(self.str_length)
                #edge += ' p_str_ln: %i' % self.parent.str_length
                else:
                    edge = " len: " + str(self.str_length)
                
            else:
                edge = ''.join(map(str, self.parentEdge))

        # printing odd/even nodes for which this node is the LCA
        # if hasattr(self, 'lca_odd') or hasattr(self, 'lca_even'):
        #     edge += ' ['
        #     if hasattr(self, 'lca_odd'):
        #         edge += 'o: %s' % self.lca_odd
        #         if hasattr(self, 'lca_even'):
        #             edge += ', '
        #     if hasattr(self, 'lca_even'):
        #         edge += 'e: %s' % self.lca_even
        #     edge += ']'

        self_id += str(edge)
        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprint(S, level + 1, onlylengths)
        return result

    def as_newick(self):
        result = ''
        if self.children:
            # inner
            result += '('
            for c in self.children:
                result += c.as_newick() + ', '
            result = result[:-2] + ')'
        else:
            # leaf
            result += self.id
        if self.parentEdge:
            result += ':%f' % self.parentEdge

        return result

    def traverse(self, fn):
        self.dfs(fn)

    def dfs(self, fn):
        # depth-first search
        lifo = deque()
        lifo.append(self)
        while lifo:
            node = lifo.pop()
            lifo.extend(reversed(node.children))
            fn(node)

    def bfs(self, fn):
        # breadth-first search
        fifo = deque()
        fifo.append(self)
        while fifo:
            node = fifo.pop()
            fifo.extendleft(node.children)
            fn(node)

    def leaflist_slow(self):
        # TODO: leaflist should be saved on the node as the tree is constructed
        #       and not offered as a linear-time function on each node
        result = []
        self.traverse(lambda n: result.append(n) if n.is_leaf() else 'do nothing')
        return result
        # def rec_helper(aNode):
        #     temp = []
        #     if len(aNode.children) == 0:
        #         # base case
        #         # aNode has no children, return itself as it is a leaf
        #         return [aNode]
        #     else:
        #         # rec. case
        #         # aNode has children, return all their leaf descendants
        #         for c in aNode.children:
        #             recursive_leafnodes_list = c.leaflist()
        #             temp.append(recursive_leafnodes_list)
        #         # flatten before return
        #         # should not return list-of-lists, just a flat list
        #         flat_leaf_list = [i for sublist in temp for i in sublist]
        #         return flat_leaf_list
        # return rec_helper(self)

    def __init__(self, aStrLength=0, aId=None, aParentEdge='', aData=None):
        self.graphid = next(self._ids)
        self.id = aId
        self.parent = None
        self.parentEdge = aParentEdge
        self.data = aData
        self.str_length = aStrLength
        self.children = []

    def __repr__(self):
        self_id = 'no-id'
        if self.id:
            self_id = 'node'+str(self.id) if 'inner' not in str(self.id) else 'inner'
        return self_id


def generate_random_tree(n, forced_leaf_id=None):
    tree = Tree()
    root = tree.root
    nodes_list = [root]
    for i in range(n):
        newNode = Node(aId=str(i))
        rnd.choice(nodes_list).add_child(newNode)
        if not i == forced_leaf_id:
            nodes_list.append(newNode)
    return tree

'''
python3
from utils import get_lca_nodepairs

'''
def get_lca_nodepairs(nodelist):
    lca_nodepairs = []
    prev_node = None
    pairings = []
    for n in range(len(nodelist)):
        node = nodelist[n]
        if not prev_node and n > 0 and node % 2 != nodelist[n - 1] % 2:
            for pairingnode in pairings[:-1]:
                lca_nodepairs.append((pairingnode, node))
            prev_node = nodelist[n - 1]
            pairings = []
        if prev_node and node % 2 == prev_node % 2:
            for pairingnode in pairings:
                lca_nodepairs.append((prev_node, pairingnode))
            for pairingnode in pairings:
                lca_nodepairs.append((pairingnode, node))
            prev_node = node
            pairings = []
            continue
        pairings.append(node)
        # print(pairings)
        
        
    return lca_nodepairs


def str2int(string):
    ''' list append is O(1), string join() is O(n), totaling O(n) conversion
        time from string to string over int alphabet '''
    int_alph = {}
    new_str_list = []
    count = 1
    for c in string:
        if c not in int_alph:
            int_alph[c] = count
            count += 1
        new_str_list.append(int_alph[c])
    return new_str_list


def append_unique_char(string):
    # O(n) running time
    count = 0
    seen_chars = {}
    for c in string:
        if c not in seen_chars:
            count += 1
            seen_chars[c] = count
    string.append(count + 1)
    return string


def string_length(span):

    if(span == None or span[0] > span[1]):
        return 0
    return span[1] - span[0]

def lcp(string1, string2, S):

    string_1_len = string_length(string1)
    string_2_len = string_length(string2)
    shorter = min(string_1_len, string_2_len)

    lcp = 0
    for i in range(shorter):
        if S[string1[0] + i] == S[string2[0] + i]:
            lcp += 1
        else:
            break
    if lcp == 0:
        return None
    return (string1[0], string1[0] + lcp) #string1[:lcp]


def naive_lca(node1, node2, tree, id2node):
    ''' strategy:   from node1, test if node2 is in the subtree of node1
                        - if so, report node1 as LCA
                    if not, proceed to parent node and do:
                        - if parent node is node2, report parent node as LCA
                        - if parent node has node2 in its subtree, report
                          parent node as LCA
                        - if neither, recurse to parent's parent
        running time: awful!
    '''
    # Notice:   there may be a difference between the node1 and node2
    #           as they are given and the final state of node1 and node2,
    #           therefore id2node is necessary for now
    node1 = id2node[node1.id]
    node2 = id2node[node2.id]

    def node_is_descendant(node1, node2):
        descendants = []
        node1.traverse(lambda n: descendants.append(n)
                       if 'inner' not in str(n.id) else 'do nothing')
        is_descendant = True in [n.id == node2.id for n in descendants]
        return is_descendant

    curr_node = node1
    no_result = True

    while no_result:
        if curr_node.id == "root":
            no_result = False

        if node_is_descendant(curr_node, node2):
            no_result = False
            return curr_node
        else:
            curr_node = curr_node.parent

    return None
