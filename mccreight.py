from utils import Node, append_unique_char, str2int, lcp, string_length
import check_correctness
from bisect import bisect_left

import argparse
import os.path


timers = dict()
timers["fastscan"] = 0

def binary_search(array, element):
    idx = bisect_left(array, element)
    result_idx = idx
    if not (idx < len(array) and array[idx] == element):
        result_idx = -1
    return result_idx

jump = 0
def slowscan(u, v, S):
    global jump
    # searches for string v starting in node u
    # create a node for v if necessary and return it
    curr_node = u
    remaining = v
    if S[remaining[0]] in curr_node.charDict:
        child = curr_node.charDict[S[remaining[0]]]
        leafID = child.leaflist[0].id - 1
        edge = (leafID + child.parent.str_length, leafID + child.str_length)
        curr_lcp = lcp(remaining, edge, S)
        if curr_lcp:
            if string_length(curr_lcp) == string_length(edge):
                # remaining contains more than curr_lcp; we need to look
                # further down the tree
                return slowscan(child, (remaining[0]+string_length(curr_lcp), remaining[1]), S)
       
            # make new internal node
            internal = Node(aId='inner')
            internal.charDict = dict()
            # internal.str = curr_node.str + curr_lcp
            # internal.edge = curr_lcp
            internal.leaflist = child.leaflist
            internal.str_length = curr_node.str_length + string_length(curr_lcp) 


            # Remove child
            childLeafId = child.leaflist[0].id-1
            childChar = S[childLeafId + child.parent.str_length]
            del curr_node.charDict[childChar]
            curr_node.remove_child(child)

            # Add internal node
            curr_node.add_child(internal)
            internalLeafId = internal.leaflist[0].id-1
            internalChar = S[internalLeafId + internal.parent.str_length]
            curr_node.charDict[internalChar] = internal
            

            curr_node.charDict
            # Add child
            internal.add_child(child)
            childChar = S[childLeafId + child.parent.str_length]
            internal.charDict[childChar] = child
    

            remaining = (remaining[0]+string_length(curr_lcp), remaining[1])

            return internal, remaining


    return curr_node, remaining


def fastscan(u, v, S):
    global jump
    # Identify u_i, the child of u matching some prefix of v
    ui = u
    prev_idx = 0
    idx = 0

    searching = True
    while searching:
        jump += 1
        if idx >= string_length(v):
            # we have covered more characters in the tree than is contained
            # in v; break the loop with ui being the node covering v plus some
            break
        found_child = False

        if S[v[0]+idx] in ui.charDict:
            child = ui.charDict[S[v[0]+idx]]
            prev_idx = idx
            idx += (child.str_length - child.parent.str_length)
            ui = child
            found_child = True
        # for child in ui.children:
            
        #     # TODO: UPDATE THIS LOOP TO UTILIZE BINARY SEARCH INSTEAD
        #     # in ui.children_char_list, look for entry v[idx]
        #     #   if -1 is returned, then no child was found
        #     #   if None is returned? no child was found
        #     #   if a child was found, do whatever is done already as below
        #     # THINK: is it necessary with binary search when list lookup at an
        #     #        an index is an O(1)-operation? because of the memory layout
        #     #        if so - why is McCreight then not plain O(n) running time?

        #     # compare the first character on edges to all children of u
        #     # if some edge matches current char in v, walk down this edge and
        #     # reloop to look further down from this new node ui
        #     leafID = child.leaflist[0].id - 1
        #     first_char_edge = S[leafID + child.parent.str_length]
           
        #     if first_char_edge == S[v[0]+idx]:
        #         prev_idx = idx
        #         idx += (child.str_length - child.parent.str_length)
        #         ui = child
        #         found_child = True
        #         break
        if not found_child:
            # looped through all children of current node ui, and none of them
            # shared paths with v; break out with ui being the node with the
            # longest path shared with v
            searching = False
            break


    if not ui:
        # apparently it can be none, in which case the returned node is
        # expected to be root? Not available to grab here, so an ugly
        # test of None returned is performed where fastscan is called;
        # in case the None is returned, the root is used
        return None, ''
    

    if ui.id == "root":

        ui_edge = (0, 0)
    else:
        leafID = ui.leaflist[0].id - 1
        ui_edge = (leafID + ui.parent.str_length, leafID + ui.str_length)

    v_updated = (v[0] + prev_idx, v[1])

    lcp_ui_v = min(string_length(ui_edge), string_length(v_updated))

    return ui, (ui_edge[0] + lcp_ui_v, ui_edge[1])


def construct_suffix_tree(inputstr, printstuff=False):
    timers["fastscan"] = 0
    S = append_unique_char(inputstr)
    
    alphabet = {}
    count = 1
    for c in S:
        if c not in alphabet:
            alphabet[c] = count
            count += 1


    n = len(S)

    id2node = {}

    root = Node(aId='root')
    root.charDict = dict()
    root.str = root.edge = []
    root.suffix_link = root

    fst_child = Node(aId=1, aStrLength=n)
    fst_child.charDict = dict()


    fst_child.str_length = n
    fst_child.leaflist = [fst_child]

    root.charDict[S[0]] = fst_child
    root.add_child(fst_child)

    root.leaflist = [fst_child]
    id2node[1] = fst_child

    head_i = root
    tail_i = (0, n)

    for i in range(1, n):
        if head_i == root:
            tail_i = (tail_i[0]+1, tail_i[1])

            head_i, remaining = slowscan(root, tail_i, S)

            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.charDict = dict()

            leaf_iplus1.str_length = n - i
           

            leaf_iplus1.leaflist = [leaf_iplus1]

            head_i.add_child(leaf_iplus1)

            leaf_iplusLeafID = i
            leaf_iplusChar = S[i + leaf_iplus1.parent.str_length]
            head_i.charDict[leaf_iplusChar] = leaf_iplus1

            tail_i = (tail_i[0] + head_i.str_length, tail_i[1]) 
            
            continue

        u = head_i.parent
        leafID = head_i.leaflist[0].id - 1

        v = (leafID + head_i.parent.str_length, leafID + head_i.str_length)
        if u != root:
            w, remaining = fastscan(u.suffix_link, v, S)
            if w is None:
                w = root
        else:
            w, remaining = fastscan(root, (v[0]+1, v[1]), S)
            if w is None:
                w = root

        if string_length(remaining) > 0:
            # "w is an edge"
            parent = w.parent
            leaf = w
            w = Node(aId='inner')
            w.charDict = dict()

            w.str_length = leaf.str_length - string_length(remaining)
          

            leafID  = leaf.leaflist[0].id - 1
            leafChar = S[leaf.parent.str_length + leafID]
            del parent.charDict[leafChar]
            parent.remove_child(leaf)


            w.leaflist = leaf.leaflist

            parent.add_child(w)
            wID = w.leaflist[0].id - 1
            wChar = S[w.parent.str_length + wID]
            parent.charDict[wChar] = w

            w.add_child(leaf)
            leafID = leaf.leaflist[0].id - 1
            leafChar = S[leaf.parent.str_length + leafID]
            w.charDict[leafChar] = leaf
        
            head_i.suffix_link = w
            head_i = w

            new_leaf = Node(aId=i + 1)
            new_leaf.charDict = dict()


            new_leaf.leaflist = [new_leaf]
            new_leaf.str_length = n - i
            w.add_child(new_leaf)
            new_leafID = new_leaf.leaflist[0].id - 1
            new_leafChar = S[new_leaf.parent.str_length + new_leafID]
            w.charDict[new_leafChar] = new_leaf

        else:

            head_i.suffix_link = w
            head_i, remaining = slowscan(w, tail_i, S)
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.charDict = dict()

            leaf_iplus1.str_length = n - i
            leaf_iplus1.leaflist = [leaf_iplus1]

            head_i.add_child(leaf_iplus1)

            leaf_iplus1ID = leaf_iplus1.leaflist[0].id - 1
            leaf_iplus1Char = S[leaf_iplus1.parent.str_length + leaf_iplus1ID]
            head_i.charDict[leaf_iplus1Char] = leaf_iplus1

            tail_i = (i + head_i.str_length, n)
    return root


def main():
    parser = argparse.ArgumentParser()
    input_helptxt = "File or string to construct a suffix tree over."
    f_helptxt = "If sat, the input argument will be handled as a text file"
    s_helptxt = "File to save suffix tree to, if not sat the tree will be printed in the console"
    parser.add_argument("input", help=input_helptxt)
    parser.add_argument("--f", help=f_helptxt, dest="filename", action="store_const", const=True, default=False)

    parser.add_argument("--s", help=s_helptxt, dest="filename_save")

    args = parser.parse_args()
    if args.filename_save:
        if os.path.isfile(args.filename_save):
            print("Cannot overwrite file %s" % args.filename_save)
            return
    inputstr = ""
    if args.filename:
        
        with open(args.input, 'r') as myfile:
            inputstr=myfile.read()
    else:
        inputstr = args.input


    inputstr = str2int(inputstr)
    
    suffixtree = construct_suffix_tree(inputstr)
    if args.filename_save:
        if not os.path.isfile(args.filename_save):
            f = open(args.filename_save, 'w+')
            f.write(suffixtree.fancyprint(inputstr))

    else:
        print(suffixtree.fancyprint(inputstr))

if __name__ == '__main__':
    main()
