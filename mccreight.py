from utils import Node, append_unique_char, str2int, lcp, string_length
import check_correctness
from bisect import bisect_left

# inputstr = 'banana'
inputstr = 'mississippi'
# inputstr = 'aabc'
# inputstr = 'abaab'

# from book, p. 115, fig. 5.2



def binary_search(array, element):
    idx = bisect_left(array, element)
    result_idx = idx
    if not (idx < len(array) and array[idx] == element):
        result_idx = -1
    return result_idx


def slowscan(u, v, S):
    # searches for string v starting in node u
    # create a node for v if necessary and return it

    curr_node = u
    remaining = v

    for child in curr_node.children:
        leafID = child.leaflist[0].id - 1
        edge = (leafID + child.parent.str_length, leafID + child.str_length)
        curr_lcp = lcp(remaining, edge, S)
        if curr_lcp:

            if S[curr_lcp[0] : curr_lcp[1]] == S[edge[0] : edge[1]]:
                # remaining contains more than curr_lcp; we need to look
                # further down the tree
                return slowscan(child, (remaining[0]+string_length(curr_lcp), remaining[1]), S)
       
            # make new internal node
            internal = Node(aId='inner')
            # TODO: ADD LIST HERE
            # internal.str = curr_node.str + curr_lcp
            # internal.edge = curr_lcp
            internal.leaflist = child.leaflist
            internal.str_length = curr_node.str_length + string_length(curr_lcp) 

    
            curr_node.remove_child(child)
            curr_node.add_child(internal)
            # TODO: UPDATE LIST HERE
            internal.add_child(child)
            # TODO: UPDATE LIST HERE

            remaining = (remaining[0]+string_length(curr_lcp), remaining[1])

            return internal, remaining


    return curr_node, remaining


def fastscan(u, v, S):
    # Identify u_i, the child of u matching some prefix of v
    ui = u
    prev_idx = 0
    idx = 0
    searching = True
    while searching:
        if idx >= string_length(v):
            # we have covered more characters in the tree than is contained
            # in v; break the loop with ui being the node covering v plus some
            break
        found_child = False

        for child in ui.children:
            
            # TODO: UPDATE THIS LOOP TO UTILIZE BINARY SEARCH INSTEAD
            # in ui.children_char_list, look for entry v[idx]
            #   if -1 is returned, then no child was found
            #   if None is returned? no child was found
            #   if a child was found, do whatever is done already as below
            # THINK: is it necessary with binary search when list lookup at an
            #        an index is an O(1)-operation? because of the memory layout
            #        if so - why is McCreight then not plain O(n) running time?

            # compare the first character on edges to all children of u
            # if some edge matches current char in v, walk down this edge and
            # reloop to look further down from this new node ui
            leafID = child.leaflist[0].id - 1
            first_char_edge = S[leafID + child.parent.str_length]
           
            if first_char_edge == S[v[0]+idx]:
                prev_idx = idx
                idx += (child.str_length - child.parent.str_length)
                ui = child
                found_child = True
                break
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
    
    # slowscan for the exact location where the mismatch occurs
    

    if ui.id == "root":

        ui_edge = (0, 0)
    else:
        leafID = ui.leaflist[0].id - 1
        ui_edge = (leafID + ui.parent.str_length, leafID + ui.str_length)

    v_updated = (v[0] + prev_idx, v[1])

    lcp_ui_v = string_length(lcp(ui_edge, v_updated, S))

    return ui, (ui_edge[0] + lcp_ui_v, ui_edge[1])


def construct_suffix_tree(inputstr, printstuff=False):
    # TODO: should run in linear time; remove strings from edges n stuff

    S = append_unique_char(inputstr)
    
    alphabet = {}
    count = 1
    for c in S:
        if c not in alphabet:
            alphabet[c] = count
            count += 1

    print(alphabet)

    n = len(S)

    id2node = {}

    root = Node(aId='root')
    root.str = root.edge = []
    root.suffix_link = root
    root.children_char_list = [None] * (len(alphabet) + 1)
    fst_child = Node(aId=1, aStrLength=n)

    # fst_child.str = fst_child.edge = S
    fst_child.children_char_list = [None] * (len(alphabet) + 1)

    fst_child.str_length = n
    fst_child.leaflist = [fst_child]
   
    root.add_child(fst_child)
    # root.children_char_list[alphabet[fst_child.edge[0]]] = fst_child
    # print(root.children_char_list)
    root.leaflist = [fst_child]
    id2node[1] = fst_child

    head_i = root
    tail_i = (0, n)

    for i in range(1, n):

        if head_i == root:
            tail_i = (tail_i[0]+1, tail_i[1])

            head_i, remaining = slowscan(root, tail_i, S)

            # add i+1 and head(i+1) as node if necessary
            leaf_iplus1 = Node(aId=i + 1)
            # TODO: ADD LIST HERE
            # leaf_iplus1.str = S[i:]
            # leaf_iplus1.edge = remaining

            # head_i.add_child(leaf_iplus1)
            # TODO: UPDATE LIST HERE
            # tail_i = tail_i[len(head_i.str):]
            leaf_iplus1.str_length = n - i #TODO: correct index?
           
            head_i.add_child(leaf_iplus1)

            tail_i = (tail_i[0] + head_i.str_length, tail_i[1]) #tail_i[head_i.str_length:]
            leaf_iplus1.leaflist = [leaf_iplus1]

            continue

        u = head_i.parent
        leafID = head_i.leaflist[0].id - 1

        v = (leafID + head_i.parent.str_length, leafID + head_i.str_length)
        # v = head_i.edge

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

            # w.edge = leaf.edge[: len(leaf.edge) - len(remaining)]
            # w.str = parent.str + w.edge
            # TODO: ADD LIST HERE

            w.str_length = leaf.str_length - string_length(remaining)
          
            parent.add_child(w)
            parent.remove_child(leaf)
            # TODO: UPDATE LIST HERE
            w.add_child(leaf)
            # TODO: UPDATE LIST HERE
            w.leaflist = leaf.leaflist

        
            head_i.suffix_link = w
            head_i = w

            new_leaf = Node(aId=i + 1)

            # TODO: ADD LIST HERE
            # new_leaf.str = S[i:]
            # new_leaf.edge = new_leaf.str[len(w.str):]
            new_leaf.leaflist = [new_leaf]
            new_leaf.str_length = n - i #TODO: correct index?
            w.add_child(new_leaf)
            # TODO: UPDATE LIST HERE

        else:

            head_i.suffix_link = w
            head_i, remaining = slowscan(w, tail_i, S)
            leaf_iplus1 = Node(aId=i + 1)
            # TODO: ADD LIST HERE
            # leaf_iplus1.str = S[i:]
            # leaf_iplus1.edge = remaining

            # head_i.add_child(leaf_iplus1)
            # TODO: UPDATE LIST HERE
            # tail_i = S[i + len(head_i.str):]
            leaf_iplus1.str_length = n - i
            leaf_iplus1.leaflist = [leaf_iplus1]

            head_i.add_child(leaf_iplus1)
            tail_i = (i + head_i.str_length, n)

    root.update_leaf_list()

    return root


def main():
    global inputstr
    inputstr = str2int(inputstr)
    print('\033c')  # clear screen, no scrollback
    suffix_tree = construct_suffix_tree(inputstr, False)

    print('final tree for input %s:' % inputstr)
    #print(suffix_tree.fancyprint_mcc(inputstr))
    print(suffix_tree.fancyprint(inputstr))
    check_correctness.check_correctness(suffix_tree, inputstr)


if __name__ == '__main__':
    main()
