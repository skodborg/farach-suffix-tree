import farach
import naive
import mccreight
from utils import Node, str2int
import random
import string
import traceback
import time


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
    while True:
        S = ''.join(random.choice(string.digits) for _ in range(2000))
        print(S)
        S = str2int(S)

        # tree = naive.construct_suffix_tree(S)
        # correct_tree = check_correctness(tree, S)
        tree = naive.construct_suffix_tree(S)
        correct_tree = check_correctness(tree, S)
        # tree = farach.construct_suffix_tree(S)
        # correct_tree = check_correctness(tree, S)
            
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
