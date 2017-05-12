import farach
import naive
import mccreight
from utils import Node, str2int
import random
import string
import traceback
import time

def sort_tree(tree, S):
    def sort_children_fn(S):
        def str_parentedge(node):
            start, stop = node.getParentEdge()
            return S[start:stop]
        return lambda n: n.children.sort(key=str_parentedge)

    tree.bfs(sort_children_fn(S))


def tree_equality(tree1, tree2, S):
    ''' assumes trees are lexicographically sorted w.r.t. edge labels '''
    tree1_nodes = []
    tree1.bfs(lambda n: tree1_nodes.append(n))

    tree2_nodes = []
    tree2.bfs(lambda n: tree2_nodes.append(n))

    # same total number of nodes in trees
    assert len(tree1_nodes) == len(tree2_nodes)

    for i in range(len(tree1_nodes)):
        node1 = tree1_nodes[i]
        node2 = tree2_nodes[i]

        # same no. of children
        assert len(node1.children) == len(node2.children)

        # same length of string represented
        assert node1.str_length == node2.str_length

        # same initial character on parent edges
        node1_edgechar = S[node1.getParentEdge()[0]]
        node2_edgechar = S[node2.getParentEdge()[0]]
        assert node1_edgechar == node2_edgechar

        # same leaf id
        if node1.is_leaf():
            assert node1.id == node2.id

    return True


def check_correctness(tree, inputstr):
    # TODO: find some definition of a suffix tree and refer it?
    #       below is from wikipedia with a dead reference to it, hmm..
    #       https://en.wikipedia.org/wiki/Suffix_tree#Definition

    # -------------------------------------------------------------
    # The suffix tree for the string S of length n is defined as a
    # tree such that:
    # -------------------------------------------------------------
    S = inputstr
    # S = farach.append_unique_char(S)
    n = len(S)
    # tree = farach.construct_suffix_tree(S)
    # print('check_correctness 2 final tree on inputstr = %s:' % S)
    # print(tree.fancyprint(S))

    # -------------------------------------------------------------
    # Check that each child has a parent pointer corresponding to
    # its position in some node's child list
    # -------------------------------------------------------------
    def helper(node):
        for child in node.children:
            assert child.parent == node
    tree.traverse(helper)

    # -------------------------------------------------------------
    # The tree has exactly n leaves numbered from 1 to n.
    # -------------------------------------------------------------
    leaflist = []
    def get_leafs(node):
        nonlocal leaflist
        if node.is_leaf():
            leaflist.append(node)
    tree.dfs(get_leafs)
    assert len(leaflist) == n

    # -------------------------------------------------------------
    # Except for the root, every internal node has at least two
    # children.
    # -------------------------------------------------------------
    def helper(node):
        if node.id == 'root':
            assert len(node.children) >= 1
        elif not node.is_leaf():
            assert len(node.children) >= 2
    tree.traverse(helper)

    # -------------------------------------------------------------
    # Each edge is labeled with a non-empty substring of S.
    # -------------------------------------------------------------
    def helper(node):
        if node.id != 'root':
            if not node.str_length - node.parent.str_length > 0:
                print('OUCH! %s %s %i' % (node, node.parent, node.str_length - node.parent.str_length))
                print(node.parent.fancyprint(S))
                print(inputstr)
            assert node.str_length - node.parent.str_length > 0
    tree.traverse(helper)

    # -------------------------------------------------------------
    # No two edges starting out of a node can have string-labels
    # beginning with the same character.
    # -------------------------------------------------------------
    def helper(node):
        if not node.is_leaf():
            seen_chars = set()
            for c in node.children:
                edge = c.getParentEdge()
                seen_chars.add(S[edge[0]])
            if len(seen_chars) != len(node.children):
                print('wtf ', seen_chars, node.children)
            assert len(seen_chars) == len(node.children)
    tree.traverse(helper)

    # -------------------------------------------------------------
    # The string obtained by concatenating all the string-labels
    # found on the path from the root to leaf i spells out suffix
    # S[i..n], for i from 1 to n.
    # -------------------------------------------------------------
    def helper(node, curr_str):
        if node.is_leaf():
            # check if curr_str + parentEdge equals i'th suffix
            # where i is node.id
            ith_suffix = S[node.id - 1:]
            str_curr_node = curr_str + S[node.getParentEdge()[0] : node.getParentEdge()[1]] 
            if ith_suffix != str_curr_node:
                print('OUCH! %s != %s' % (ith_suffix, str_curr_node))
            assert ith_suffix == str_curr_node
        else:
            # call recursively to all children with parentEdge appended
            # onto curr_str in the recursive call
            new_str = []
            if node.id != 'root':
                # need to make a copy of curr_str as otherwise all recursive
                # calls will have a pointer to the same list, thus extending
                # it far too much
                new_str = []
                new_str.extend(curr_str)
                new_str.extend(S[node.getParentEdge()[0] : node.getParentEdge()[1]])
            for n in node.children:
                helper(n, new_str)
    helper(tree, [])

    print('tree was verified and correct')
    return tree

    # print('tree for input \"%s\" is correct' % inputstr)

    # MANGELFULD:
    # det skal også være en compacted trie, så alle indre knuder skal være LCA
    # for mindst et par af leaf node descendants.
    # Hvis vi løber alle par af leaf nodes igennem, og markerer deres LCA, så
    # skal alle indre knuder være markeret mindst en gang
    # TODO: tænk lige igennem, passer det også? er det garanti nok??
    #       argumenter, noget med, at en indre knuder bliver konstrueret netop
    #       fordi prefixes af to suffixes er ens ned til det punkt, men så
    #       divergerer
    # VENT! ER DEN ALLIGEVEL INDEHOLDT I DEFINITIONEN PÅ WIKIPEDIA?
    #       for hvis der kun må være n leaf nodes, og alle inner nodes skal
    #       have to eller flere børn, så skal de alle dele et eller andet op
    #       og alle de n suffixes skal jo kunne staves i stien fra rodknuden
    #       bliver de så tvunget til at være lige præcis LCA for et par af leaf
    #       nodes på den måde?


def run_tests():
    inputstr = str2int("mississippi")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("121112212221")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("111222122121")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("12121212121")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("banana")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("mississippiisaniceplaceithink")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)
    inputstr = str2int("12121")
    tree = farach.construct_suffix_tree(inputstr)
    check_correctness(tree, inputstr)


def main():
    #run_tests()
    # while True:
    for _ in range(1000):
        S = ''.join(random.choice(string.digits) for _ in range(1000))
        S = str2int(S)

        tree1 = naive.construct_suffix_tree(S[:])
        tree2 = farach.construct_suffix_tree(S[:])
        tree3 = mccreight.construct_suffix_tree(S)

        sort_tree(tree1, S)
        sort_tree(tree3, S)
        assert tree_equality(tree1, tree2, S)
        assert tree_equality(tree1, tree3, S)
        # correct_tree = check_correctness(tree1, S)
        # correct_tree = check_correctness(tree2, S)
        # correct_tree = check_correctness(tree3, S)

        # print(tree1.fancyprint(S))
        # print(tree2.fancyprint(S))
        # print(tree3.fancyprint(S))
            
        # try:
        #     start = time.time()
        #     # tree = farach.construct_suffix_tree(S)
        #     tree = naive.construct_suffix_tree(S)
        #     end = time.time()
        #     correct_tree = check_correctness(tree, S)
        #     print('took %f' % (end - start))
        # except AssertionError:
        #     print('attempting string: %s' % S)
        #     print('assertion error!')
        #     traceback.print_exc()
        # except TypeError:
        #     print('attempting string: %s' % S)
        #     print('type error!')
        #     traceback.print_exc()
        # except:
        #     print('attempting string: %s' % S)
        #     print('some error!')
        #     traceback.print_exc()


if __name__ == '__main__':
    main()
