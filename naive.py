from utils import Node, append_unique_char, str2int, lcp_string
import check_correctness

inputstr = 'banana'
inputstr = 'mississippi'


def construct_suffix_tree(inputstr, printstuff=False):
    S = append_unique_char(inputstr)
    n = len(S)

    root = Node(aId='root')
    fst_child = Node(aId=1, aStrLength=n)
    root.add_child(fst_child)
    root.leaflist = [fst_child]

    for i in range(1, n):
        suff = S[i:n]
        suff_id = i + 1
        suff_node = Node(aId=suff_id, aStrLength=n - i)

        remaining = suff
        parent = root
        searching = True

        child_to_merge = None
        lcp_with_child = ''

        while searching:
            continue_loop = False
            for c in parent.children:
                c_parentEdge = c.getParentEdge(S)
                curr_lcp = lcp_string(c_parentEdge, remaining)
                if curr_lcp:
                    if len(curr_lcp) == len(c_parentEdge):
                        # continue with c as parent
                        parent = c
                        remaining = remaining[len(curr_lcp):]
                        # loop; test children of new parent, c
                        continue_loop = True
                        break
                    else:
                        # found our parent, break out
                        child_to_merge = c
                        lcp_with_child = curr_lcp
                        searching = False
                        break
            if not continue_loop:
                # no children shared lcp; either it is to be appended to root
                # or to whatever parent was left from last iteration.
                # Either case will have the correct node saved in 'parent'
                searching = False
                break

        # TODO: sort children lexicographically?

        if child_to_merge:
            internal_strlength = parent.str_length + len(lcp_with_child)
            internal = Node(aId='inner', aStrLength=internal_strlength)
            parent.remove_child(child_to_merge)
            parent.add_child(internal)
            internal.add_child(suff_node)
            internal.add_child(child_to_merge)
        else:
            parent.add_child(suff_node)

        root.update_leaf_list()
    return root


def main():
    global inputstr
    inputstr = str2int(inputstr)
    suffix_tree = construct_suffix_tree(inputstr, False)

    print('final tree for input %s:' % inputstr)
    print(suffix_tree.fancyprint(inputstr))
    check_correctness.check_correctness(suffix_tree, inputstr)


if __name__ == '__main__':
    main()
