import farach
from utils import Node
import random
import string

def check_correctness(inputstr):
    # TODO: i think it fails to identify trees that are not proper
    #       compacted tries; if an inner node only has a single inner
    #       node as child, it is not correct, but still reported as so
    # fixed in check_correctness2 though
    inputstrOld = inputstr
    inputstr = farach.str2int(inputstr)

    suffix_tree = farach.construct_suffix_tree(inputstr)

    add_str_length(suffix_tree, 0)
    farach.compute_lcp_tree(suffix_tree)
    make_inners_unique(suffix_tree)

    suffix_tree.traverse(check_suffix_link_length)

    check_string_length(suffix_tree)

    suffix_tree.traverse(check_descendants(inputstr))

    suffix_tree.traverse(children_different_first_char)

    print("tree for input : \"%s\" is correct" % inputstrOld)

    return suffix_tree


def children_different_first_char(node):
    # For each internal node x with children c1...ck
    # then each of substr xci begins with a different char
    current_chars = set()
    for n in node.children:
        assert n.parentEdge[0] not in current_chars
        current_chars.add(n.parentEdge[0])


def make_inners_unique(node):
    curr = 0

    def helper(n):
        nonlocal curr
        if n.id == "inner":
            n.id += str(curr)
            curr += 1
    node.bfs(helper)


def check_descendants(inputstr):
    # if y is a child of x, then sl(y) is a descendant of sl(x)
    # and x and y begin with the same char
    def check_descendants_helper(node):
        if hasattr(node, "suffix_link"):
            for n in node.children:
                if hasattr(n, "suffix_link"):
                    assert node_is_descendant(node.suffix_link, n.suffix_link)
                if n.is_leaf():
                    nth_suffix_firstchar = inputstr[n.id - 1]
                    current = n

                    while current.parent.id != "root":
                        current = current.parent

                    first_char_path_to_n = current.parentEdge[0]
                    assert nth_suffix_firstchar == first_char_path_to_n
    return check_descendants_helper


def node_is_descendant(node1, node2):
        descendants = []
        node1.traverse(lambda n: descendants.append(n))
        is_descendant = True in [n.id == node2.id for n in descendants]
        return is_descendant


def check_suffix_link_length(node):
    # For each node x,
    # |sl(x)| = |x| - 1

    if hasattr(node, "suffix_link"):
        assert node.str_length - 1 == node.suffix_link.str_length


def check_string_length(node):
    # If r is the root, then |r| = 0
    # If y is a child of x, then |y| > |x|

    if(node.id == "root"):
        assert node.str_length == 0

    else:
        for child in node.children:
            assert node.str_length < child.str_length
            check_string_length(child)


def add_str_length(node, prev_length):
        node.str_length = prev_length + len(node.parentEdge)
        for n in node.children:
            add_str_length(n, node.str_length)


def check_correctness2(inputstr):
    # TODO: find some definition of a suffix tree and refer it?
    #       below is from wikipedia with a dead reference to it, hmm..
    #       https://en.wikipedia.org/wiki/Suffix_tree#Definition

    # -------------------------------------------------------------
    # The suffix tree for the string S of length n is defined as a
    # tree such that:
    # -------------------------------------------------------------
    S = farach.str2int(inputstr)
    n = len(S)
    tree = farach.construct_suffix_tree(S)

    # -------------------------------------------------------------
    # The tree has exactly n leaves numbered from 1 to n.
    # -------------------------------------------------------------

    # the construction adds a unique char to the string to ensure deterministic
    # trees; therefore, the tree will contain a single leaf from root with this
    # unique char, hence the leaves will be n + 1, one per suffix plus an extra
    assert len(tree.leaflist) == n + 1

    # -------------------------------------------------------------
    # Except for the root, every internal node has at least two
    # children.
    # -------------------------------------------------------------
    def helper(node):
        if node.id == 'root':
            assert len(node.children) >= 1
        if not node.is_leaf():
            assert len(node.children) >= 2
    tree.traverse(helper)

    # -------------------------------------------------------------
    # Each edge is labeled with a non-empty substring of S.
    # -------------------------------------------------------------
    def helper(node):
        if node.id != 'root':
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
                seen_chars.add(c.getParentEdge(S)[0])
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
            str_curr_node = curr_str + node.getParentEdge(S)
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
                new_str.extend(node.getParentEdge(S))
            for n in node.children:
                helper(n, new_str)
    helper(tree, [])

    print('tree for input \"%s\" is correct' % inputstr)

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
    check_correctness2("mississippi")
    check_correctness2("121112212221")
    check_correctness2("111222122121")
    check_correctness2("12121212121")
    check_correctness2("banana")
    check_correctness2("mississippiisaniceplaceithink")
    check_correctness2("12121")


def main():
    #run_tests()

    check_correctness(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100)))

if __name__ == '__main__':
    main()
