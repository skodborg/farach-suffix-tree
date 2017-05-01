from utils import Node, append_unique_char, str2int, lcp
import check_correctness

# inputstr = 'banana'
# inputstr = 'mississippi'
# inputstr = 'aabc'
# inputstr = 'abaab'

# from book, p. 115, fig. 5.2
inputstr = 'abaababaabaab'


def slowscan(u, v):
    # searches for string v starting in node u
    # create a node for v if necessary and return it

    curr_node = u
    remaining = v

    for child in curr_node.children:
        curr_lcp = lcp(remaining, child.edge)

        if curr_lcp:
            if curr_lcp == child.edge:
                # remaining contains more than curr_lcp; we need to look
                # further down the tree
                return slowscan(child, remaining[len(curr_lcp):])

            # make new internal node
            internal = Node(aId='inner')
            internal.str = curr_node.str + curr_lcp
            internal.edge = curr_lcp

            curr_node.remove_child(child)
            curr_node.add_child(internal)
            internal.add_child(child)

            child.edge = child.edge[len(curr_lcp):]
            remaining = remaining[len(curr_lcp):]

            return internal, remaining

    return curr_node, remaining


def fastscan(u, v):
    # Identify u_i, the child of u matching some prefix of v
    ui = u
    prev_idx = 0
    idx = 0
    searching = True
    while searching:
        if idx >= len(v):
            # we have covered more characters in the tree than is contained
            # in v; break the loop with ui being the node covering v plus some
            break
        found_child = False
        for child in ui.children:
            # compare the first character on edges to all children of u
            # if some edge matches current char in v, walk down this edge and
            # reloop to look further down from this new node ui
            if child.edge[0] == v[idx]:
                prev_idx = idx
                idx += len(child.edge)
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
    lcp_ui_v = len(lcp(ui.edge, v[prev_idx:]))

    return ui, ui.edge[lcp_ui_v:]


def construct_suffix_tree(inputstr, printstuff=False):
    # TODO: should run in linear time; remove strings from edges n stuff

    S = append_unique_char(inputstr)
    n = len(S)

    id2node = {}

    root = Node(aId='root')
    root.str = root.edge = []
    root.suffix_link = root
    fst_child = Node(aId=1, aStrLength=n)
    fst_child.str = fst_child.edge = S
    root.add_child(fst_child)
    root.leaflist = [fst_child]
    id2node[1] = fst_child

    head_i = root
    tail_i = S

    for i in range(1, n):

        if head_i == root:
            tail_i = tail_i[1:]
            head_i, remaining = slowscan(root, tail_i)
            # add i+1 and head(i+1) as node if necessary
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str = S[i:]
            leaf_iplus1.edge = remaining

            head_i.add_child(leaf_iplus1)

            tail_i = tail_i[len(head_i.str):]
            continue

        u = head_i.parent
        v = head_i.edge

        if u != root:
            w, remaining = fastscan(u.suffix_link, v)
            if w is None:
                w = root
        else:
            w, remaining = fastscan(root, v[1:])
            if w is None:
                w = root

        if remaining:
            # "w is an edge"
            parent = w.parent
            leaf = w
            w = Node(aId='inner')
            w.edge = leaf.edge[: len(leaf.edge) - len(remaining)]
            w.str = parent.str + w.edge

            parent.add_child(w)
            parent.remove_child(leaf)
            w.add_child(leaf)

            leaf.edge = leaf.edge[len(w.edge):]

            head_i.suffix_link = w
            head_i = w

            new_leaf = Node(aId=i + 1)
            new_leaf.str = S[i:]
            new_leaf.edge = new_leaf.str[len(w.str):]
            w.add_child(new_leaf)

        else:
            head_i.suffix_link = w
            head_i, remaining = slowscan(w, tail_i)
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str = S[i:]
            leaf_iplus1.edge = remaining

            head_i.add_child(leaf_iplus1)
            tail_i = S[i + len(head_i.str):]

    root.update_leaf_list()

    def add_str_length(node):
        node.str_length = len(node.str)
    root.traverse(add_str_length)

    return root


def main():
    global inputstr
    inputstr = str2int(inputstr)
    print('\033c')  # clear screen, no scrollback
    suffix_tree = construct_suffix_tree(inputstr, False)

    print('final tree for input %s:' % inputstr)
    print(suffix_tree.fancyprint_mcc())
    check_correctness.check_correctness(suffix_tree, inputstr)


if __name__ == '__main__':
    main()
