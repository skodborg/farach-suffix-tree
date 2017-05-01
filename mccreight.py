from utils import Node, append_unique_char, str2int, lcp, string_length
import check_correctness

# inputstr = 'banana'
# inputstr = 'mississippi'
# inputstr = 'aabc'
# inputstr = 'abaab'

# from book, p. 115, fig. 5.2

inputstr = '1112112'


def slowscan(u, v, S):
    # searches for string v starting in node u
    # create a node for v if necessary and return it

    curr_node = u
    remaining = v

    for child in curr_node.children:
        leafID = child.leaflist[0].id - 1
        edge = (leafID + child.parent.str_length, leafID + child.str_length)
        #edge = S[leafID + child.parent.str_length: leafID + child.str_length]
        curr_lcp = lcp(remaining, edge, S)
        if curr_lcp:

            if S[curr_lcp[0] : curr_lcp[1]] == S[edge[0] : edge[1]]:
                # remaining contains more than curr_lcp; we need to look
                # further down the tree
                return slowscan(child, (remaining[0]+string_length(curr_lcp), remaining[1]), S)
                #return slowscan(child, remaining[len(curr_lcp):], S)

            # make new internal node
            internal = Node(aId='inner')
            internal.leaflist = child.leaflist
            internal.str_length = curr_node.str_length + string_length(curr_lcp) 

            # internal.str = curr_node.str + curr_lcp
            # internal.edge = curr_lcp

            curr_node.remove_child(child)
            curr_node.add_child(internal)
            internal.add_child(child)

            #child.edge = child.edge[len(curr_lcp):]
            #remaining = remaining[len(curr_lcp):]
            remaining = (remaining[0]+string_length(curr_lcp), remaining[1])

            return internal, remaining


    return curr_node, remaining


def fastscan(u, v):
    # Identify u_i, the child of u matching some prefix of v
    ui = None
    for child in u.children:
        if lcp(child.edge, v):
            ui = child
            break

    if not ui:
        # apparently it can be none, in which case the returned node is
        # expected to be root? Not available to grab here, so an ugly
        # test of None returned is performed where fastscan is called;
        # in case the None is returned, the root is used
        return None, ''
    
    lcp_ui_v = lcp(ui.edge, v)

    # 1) len(v) > len(ui):
    #       search recursively from ui for the remainder of v
    if len(v) > len(ui.edge):
        assert ui.edge == lcp_ui_v
        return fastscan(ui, v[len(ui.edge):])

    if len(v) <= len(ui.edge):
        # all of v was covered by some edge or node
        assert ui.edge[:len(v)] == v
        return ui, ui.edge[len(v):]


def construct_suffix_tree(inputstr, printstuff=False):
    # TODO: should run in linear time; remove strings from edges n stuff

    S = append_unique_char(inputstr)
    n = len(S)

    id2node = {}

    root = Node(aId='root')
    root.str = root.edge = []
    root.suffix_link = root
    fst_child = Node(aId=1, aStrLength=n)

    fst_child.str_length = n
    fst_child.leaflist = [fst_child]
    #fst_child.str = fst_child.edge = S
    root.add_child(fst_child)
    root.leaflist = [fst_child]
    id2node[1] = fst_child

    head_i = root
    tail_i = (0, n)

    for i in range(1, n):

        if head_i == root:
            #tail_i = tail_i[1:]
            tail_i = (tail_i[0]+1, tail_i[1])

            head_i, remaining = slowscan(root, tail_i, S)

            # add i+1 and head(i+1) as node if necessary
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str_length = n - i #TODO: correct index?
            #leaf_iplus1.str = S[i:]
            #leaf_iplus1.edge = remaining

            head_i.add_child(leaf_iplus1)

            tail_i = (tail_i[0] + head_i.str_length, tail_i[1]) #tail_i[head_i.str_length:]
            leaf_iplus1.leaflist = [leaf_iplus1]
            #tail_i = tail_i[len(head_i.str):]
            continue

        u = head_i.parent
        leafID = head_i.leaflist[0].id - 1

        v = (leafID + head_i.parent.str_length, leafID + head_i.str_length)
        # v = head_i.edge
       
        if u != root:
            w, remaining = slowscan(u.suffix_link, v, S) #fastscan(u.suffix_link, v)
            if w is None:
                w = root
        else:
            w, remaining = slowscan(root, (v[0]+1, v[1]), S) #fastscan(root, v[1:])
            if w is None:
                w = root

        if string_length(remaining) > 0:
            # "w is an edge"
            parent = w.parent
            leaf = w
            w = Node(aId='inner')
            w.str_length = n - string_length(remaining)

            # w.edge = leaf.edge[: len(leaf.edge) - len(remaining)]
            # w.str = parent.str + w.edge

            parent.add_child(w)
            parent.remove_child(leaf)
            w.add_child(leaf)
            w.leaflist = leaf.leaflist
            #leaf.edge = leaf.edge[len(w.edge):]

            head_i.suffix_link = w
            head_i = w

            new_leaf = Node(aId=i + 1)
            #new_leaf.str = S[i:]
            #new_leaf.edge = new_leaf.str[len(w.str):]
            new_leaf.leaflist = [new_leaf]
            new_leaf.str_length = n - i #TODO: correct index?
            w.add_child(new_leaf)

        else:
            head_i.suffix_link = w
            head_i, remaining = slowscan(w, tail_i, S)
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str_length = n - i
            leaf_iplus1.leaflist = [leaf_iplus1]
            # leaf_iplus1.str = S[i:]
            # leaf_iplus1.edge = remaining

            head_i.add_child(leaf_iplus1)
            tail_i = (i + head_i.str_length, n)
            #tail_i = S[i + head_i.str_length:]

    root.update_leaf_list()

    # def add_str_length(node):
    #     node.str_length = len(node.str)
    # root.traverse(add_str_length)

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
