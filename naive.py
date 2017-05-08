from utils import Node, append_unique_char, str2int, lcp, string_length
import check_correctness
import random
import string

inputstr = 'banana'
inputstr = 'mississippi'


def construct_suffix_tree(inputstr, printstuff=False):
    S = append_unique_char(inputstr)
    n = len(S)

    root = Node(aId='root')
    root.charDict = dict()

    fst_child = Node(aId=1, aStrLength=n)
    fst_child.charDict = dict()
    fst_child.leaflist = [fst_child]
    root.charDict[S[0]] = fst_child
    root.add_child(fst_child)
    root.leaflist = [fst_child]



    for i in range(1, n):
        suff = (i, n) #S[i:n]
        suff_id = i + 1
        suff_node = Node(aId=suff_id, aStrLength=n - i)
        suff_node.charDict = dict()

        suff_node.leaflist = [suff_node]

        remaining = suff
        parent = root
        searching = True

        child_to_merge = None
        lcp_with_child = ''

        while searching:
            continue_loop = False
            if S[remaining[0]] in parent.charDict:
                c = parent.charDict[S[remaining[0]]]

                c_parentEdge = c.getParentEdge()
                curr_lcp = lcp(c_parentEdge, remaining, S)
                if string_length(curr_lcp) == string_length(c_parentEdge):
                    # continue with c as parent
                    parent = c
                    remaining = (remaining[0] + string_length(curr_lcp), remaining[1]) #remaining[len(curr_lcp):]
                    # loop; test children of new parent, c
                    continue_loop = True
                    #break
                else:
                    # found our parent, break out
                    child_to_merge = c
                    lcp_with_child = curr_lcp
                    searching = False
                    #break

            if not continue_loop:
                # no children shared lcp; either it is to be appended to root
                # or to whatever parent was left from last iteration.
                # Either case will have the correct node saved in 'parent'
                searching = False
                break

        # TODO: sort children lexicographically?

        if child_to_merge:
            internal_strlength = parent.str_length + string_length(lcp_with_child)
            internal = Node(aId='inner', aStrLength=internal_strlength)
            internal.charDict = dict()
            internal.leaflist = suff_node.leaflist

            childToMergeChar = S[child_to_merge.getParentEdge()[0]]
            del parent.charDict[childToMergeChar]
            parent.remove_child(child_to_merge)


            parent.add_child(internal)
            internalChar = S[internal.getParentEdge()[0]]
            parent.charDict[internalChar] = internal

            internal.add_child(suff_node)
            suff_nodeChar = S[suff_node.getParentEdge()[0]]
            internal.charDict[suff_nodeChar] = suff_node

            internal.add_child(child_to_merge)
            child_to_merge_Char = S[ child_to_merge.getParentEdge()[0]]
            internal.charDict[child_to_merge_Char] =  child_to_merge
        else:
            parent.add_child(suff_node)
            suff_nodeChar = S[ suff_node.getParentEdge()[0]]
            parent.charDict[suff_nodeChar] =  suff_node
    return root


def main():
    global inputstr
    inputstr = str2int(str2int(''.join(random.choice(string.digits) for _ in range(10000*1000))))
    suffix_tree = construct_suffix_tree(inputstr, False)

    print("done")
    #print('final tree for input %s:' % inputstr)
    #print(suffix_tree.fancyprint(inputstr))
    #check_correctness.check_correctness(suffix_tree, inputstr)


if __name__ == '__main__':
    main()
