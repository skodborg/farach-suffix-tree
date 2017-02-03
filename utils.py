from itertools import count
import random as rnd


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

    def fancyprint(self, level=0):
        self_id = self.id if self.id else 'no-id'
        if self.parentEdge:
            self_id += ':%.2f' % self.parentEdge
        result = '\t' * level + self_id + '\n'
        for child in self.children:
            result += child.fancyprint(level + 1)
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

    def leaflist(self):
        def rec_helper(aNode):
            temp = []
            if len(aNode.children) == 0:
                # base case
                # aNode has no children, return itself as it is a leaf
                return [aNode]
            else:
                # rec. case
                # aNode has children, return all their leaf descendants
                for c in aNode.children:
                    recursive_leafnodes_list = c.leaflist()
                    temp.append(recursive_leafnodes_list)
                # flatten before return
                # should not return list-of-lists, just a flat list
                flat_leaf_list = [i for sublist in temp for i in sublist]
                return flat_leaf_list
        return rec_helper(self)

    def __init__(self, aParentEdge='', aId=None, aData=None):
        self.graphid = next(self._ids)
        self.id = aId
        self.parent = None
        self.parentEdge = aParentEdge
        self.data = aData
        self.children = []

    def __repr__(self):
        self_id = self.id if self.id else 'no-id'
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
