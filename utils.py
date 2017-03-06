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
            self.leaflist.extend(n.update_leaf_list())

        return self.leaflist

    def getParentEdge(self, S):
        if self.id == 'root':
            return ''

        if self.is_leaf():
            leaf_id = self.id
        else:
            leaf_descendant = self.leaflist[0]
            leaf_id = leaf_descendant.id
        
        return S[leaf_id - 1 + self.parent.str_length : leaf_id - 1 + self.str_length]
    
    def fancyprint(self, S, level=0):
        self_id = str(self.id)+":" if self.id else ''
        
        # TODO: utilize getParentEdge() ??
        if self.is_leaf():
            leaf_id = self.id
        else:
            leaf_descendant = self.leaflist[0]
            leaf_id = leaf_descendant.id
        if self.id == "root":
            edge = ""
        else:
            if S:
                edge =  str(S[leaf_id - 1 + self.parent.str_length : leaf_id - 1 + self.str_length]) #+ " len: " + str(self.str_length)
                
            else:
                edge = ''.join(map(str, self.parentEdge))
        self_id += str(edge)
        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprint(S, level + 1)
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
