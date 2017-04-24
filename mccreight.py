from utils import Node, append_unique_char, str2int, lcp
import check_correctness

# inputstr = 'banana'
# inputstr = 'mississippi'
# inputstr = 'aabc'
inputstr = 'abc'


def construct_suffix_tree(inputstr, printstuff=False):
    S = append_unique_char(inputstr)
    n = len(S)

    root = Node(aId='root')
    fst_child = Node(aId=1, aStrLength=n)
    root.add_child(fst_child)
    root.leaflist = [fst_child]

    
    root.update_leaf_list()
    return root


def main():
    global inputstr
    inputstr = str2int(inputstr)
    suffix_tree = construct_suffix_tree(inputstr, False)

    print('final tree for input %s:' % inputstr)
    print(suffix_tree.fancyprint(inputstr))
    # check_correctness.check_correctness(suffix_tree, inputstr)


if __name__ == '__main__':
    main()
