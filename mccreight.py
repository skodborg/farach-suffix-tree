from utils import Node, append_unique_char, str2int, lcp
import check_correctness

# inputstr = 'banana'
# inputstr = 'mississippi'
# inputstr = 'aabc'
# inputstr = 'abaab'

# from book, p. 115, fig. 5.2
# inputstr = 'abaababaabaab'
inputstr = '5355590107'
inputstr = '55955979110599394087'


def slowscan(u, v):
    # searches for string v starting in node u
    # create a node for v if necessary and return it

    curr_node = u
    remaining = v

    for child in curr_node.children:
        curr_lcp = lcp(remaining, child.edge)

        if curr_lcp:
            # print('curr_lcp: ', curr_lcp, ' with child ', child)
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
    # string uv is a prefix of S; locate exact position in S. Two cases can apply:

    # Identify u_i, the child of u matching some prefix of v
    ui = None
    for child in u.children:
        if lcp(child.edge, v):
            ui = child
            break

    # assert ui  # should always exist
    if not ui:
        # apparently it can be none, in which case the returned node is expected
        # to be root?
        return None, ''
    
    lcp_ui_v = lcp(ui.edge, v)

    # 1) len(v) > len(ui):
    #       search recursively from ui for the remainder of v
    if len(v) > len(ui.edge):
        assert ui.edge == lcp_ui_v
        return fastscan(ui, v[len(ui.edge):])

    if len(v) <= len(ui.edge):
        assert ui.edge[:len(v)] == v
        return ui, ui.edge[len(v):]


def construct_suffix_tree(inputstr, printstuff=False):
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
        # if i == 5:
        #     break
        suff_i = S[i:]
        print('i: %i' % i)

        if head_i == root:
            tail_i = tail_i[1:]
            head_i, remaining = slowscan(root, tail_i)
            # add i+1 and head(i+1) as node if necessary
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str = S[i:]
            leaf_iplus1.edge = remaining

            head_i.add_child(leaf_iplus1)

            tail_i = tail_i[len(head_i.str):]
            print(root.fancyprint_mcc())
            print('head(%i): %s   tail(%i): %s\n%s\n' % (i+1, head_i.str, i+1, tail_i, '-'*50))
            # break
            continue

        u = head_i.parent
        v = head_i.edge
        print('u: ', u.str, '\tv: ', v)

        if u != root:
            print('fastscanning from s(u)=', u.suffix_link, ' looking for v=', v)
            w, remaining = fastscan(u.suffix_link, v)
            print('w = ', w.str, ' remaining: ', remaining)
            if w is None:
                w = root
        else:
            print('fastscanning from root looking for v[1:]=', v[1:])
            w, remaining = fastscan(root, v[1:])

            if w is None:
                w = root

        if remaining:
            # "w is an edge"
            # print('case not handled yet')
            parent = w.parent
            leaf = w
            w = Node(aId='inner')
            w.edge = leaf.edge[:len(leaf.edge)-len(remaining)]
            w.str = parent.str + w.edge

            parent.add_child(w)
            parent.remove_child(leaf)
            w.add_child(leaf)

            leaf.edge = leaf.edge[len(w.edge):]

            head_i.suffix_link = w
            head_i = w

            new_leaf = Node(aId=i + 1)
            new_leaf.str = S[i:]
            new_leaf.edge = new_leaf.str[len(w.edge):]
            w.add_child(new_leaf)


        else:
            print("here?", tail_i)
            head_i.suffix_link = w
            head_i, remaining = slowscan(w, tail_i)
            print(head_i, remaining)
            leaf_iplus1 = Node(aId=i + 1)
            leaf_iplus1.str = S[i:]
            leaf_iplus1.edge = remaining
            
            head_i.add_child(leaf_iplus1)
            print(head_i, head_i.str)
            tail_i = S[i + len(head_i.str):]

        print(root.fancyprint_mcc())
        print('head(%i): %s   tail(%i): %s\n%s\n' % (i+1, head_i.str, i+1, tail_i, '-'*50))
    
    root.update_leaf_list()
    
    def add_str_length(node):
        node.str_length = len(node.str)
    root.traverse(add_str_length)

    def test(node):
        if node.is_leaf():
            print(node.id, node.str, node.str_length)
    root.traverse(test)
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
