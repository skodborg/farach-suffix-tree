import math
import radixsort
import utils

unique_char = '$'
A = {0: 1, 1: 2}
# input = '121112212221'
input = '111222122121'
# input = 'banana'
# input = 'mississippi'

# TODO: test that it works for inputs of odd length
# input = '1211122122211'


def str2int(string):
    ''' list append is O(1), string join() is O(n), totaling O(n) conversion
        time from string to string over int alphabet '''
    int_alph = {}
    new_str_list = []
    count = 1
    for c in string:
        if c not in int_alph:
            int_alph[c] = str(count)
            count += 1
        new_str_list.append(int_alph[c])
    new_str = ''.join(new_str_list)
    return new_str


def construct_suffix_tree(inputstr):
    inputstr += unique_char
    print(inputstr)
    # converting to integer alphabet
    inputstr = str2int(inputstr)
    print(inputstr)

    # TODO: return suffix tree if inputstr is of length 1 or 2

    t_odd = T_odd(inputstr)
    t_even = T_even(t_odd, inputstr)
    # t_overmerged = overmerge(t_even, t_odd)
    # suffix_tree = cleanup_overmerge(t_overmerged)
    # return suffix_tree


def T_odd(inputstr):
    S = inputstr
    n = len(S)

    def toInt(char):
        # TODO: redundant with conversion to integer alphabet?
        if char == '$':
            return len(A) + 1
        else:
            return int(char)

    def rank_to_char(node):
        ''' swaps ranks in trees with corresponding character pair
            from original string '''
        new_edge = ''
        for c in node.parentEdge:
            if(c == "$"):
                new_edge += "$"
            else:
                pair = single2pair[toInt(c)]
                new_edge += str(pair[0])
                new_edge += str(pair[1])
        node.parentEdge = new_edge

        for n in node.children:
            rank_to_char(n)

    def resolve_suffix_tree(node):
        ''' Takes suffix tree of S' (Sm in code) and massages it into suffix
            tree of odd (T_odd in book), which is a proper compacted trie.
            This involves checking first character of every edge of children
            of inner nodes to see if we need to introduce a new node with this
            common character as its parentEdge, and the two children who shared
            this character as its children. Further handles cases of a newly
            introduced node only having one child, and removes itself while
            correcting the tree structure around it (modify parentEdge to
            include its only child-nodes parentEdge and let its parent have
            its child as child before finally removing itself) '''
        def merge():
            # Takes every child in merge list, adds a new node with
            # these children as children to the new node
            node = utils.Node(current_char)
            node.children = current_merg
            for n in node.children:
                # Removes first char, as it is already accounted for on parent node
                n.parentEdge = n.parentEdge[1:]
            children_list.append(node)

        current_char = ''
        current_merg = []
        children_list = []

        # If node is a leaf, update node id to represent the actually length
        # of string after de-ranking
        if(node.is_leaf()):
            node.id = node.id * 2 - 1
            return

        for child in node.children:
            edge = child.parentEdge
            if(edge[0] == current_char or current_char == ''):
                current_merg.append(child)
                current_char = edge[0]
            else:
                if(len(current_merg) > 1):
                    merge()
                else:
                    children_list.extend(current_merg)

                current_char = edge[0]
                current_merg = [child]

        if(len(current_merg) > 1):
            merge()
        else:
            children_list.extend(current_merg)

        # Correcting tree if a node only has one child.
        # Merging with parent

        if(len(children_list) == 1):
            node.children = children_list[0].children
            node.parentEdge += children_list[0].parentEdge
        else:
            node.children = children_list

        for n in node.children:
            resolve_suffix_tree(n)

    # strings are 0-indexed in python, and 1-indexed in the book's examples
    # so we -2 and -1 from pos 'i' to let our match the book's examples
    chr_pairs = [(toInt(S[2 * i - 2]), toInt(S[2 * i - 1]))
                 for i in range(1, math.floor(n / 2) + 1)]
    # assert chr_pairs == [(1, 2), (1, 1), (1, 2), (2, 1), (2, 2), (2, 1)]

    # sort in O(k * n) using radix sort (k = 2 here, guaranteed)
    radixsort.sort(chr_pairs)
    # assert chr_pairs == [(1, 1), (1, 2), (1, 2), (2, 1), (2, 1), (2, 2)]

    # remove duplicates, O(n)
    unique_chr_pairs = [chr_pairs[0]]
    for pair in chr_pairs[1:]:
        if unique_chr_pairs[-1] != pair:
            unique_chr_pairs.append(pair)
    chr_pairs = unique_chr_pairs
    # assert chr_pairs == [(1, 1), (1, 2), (2, 1), (2, 2)]

    # compute S'[i] = rank of (S[2i - 1], S[2i])
    Sm = ''
    count = 1
    pair2single = {}  # lookup is O(1) for pairs to single character mapping
    single2pair = {}  # lookup is O(1) for single to pair character mapping
    for pair in chr_pairs:
        pair2single[pair] = count
        single2pair[count] = pair
        count += 1
    for i in range(1, math.floor(n / 2) + 1):
        pair = (toInt(S[2 * i - 2]), toInt(S[2 * i - 1]))
        Sm += str(pair2single[pair])
    Sm += unique_char
    # assert Sm == '212343$'

    # TODO: recursively call construct_suffix_tree(Sm) to create suffix tree for Sm
    # tree_Sm = construct_suffix_tree(Sm)
    tree_Sm = faked_tree()

    # convert edge characters from ranks to original character pairs
    # + convert leaf ids to corresponding original suffix ids
    rank_to_char(tree_Sm)

    # massage into proper compacted trie 
    # (no edges of a node share first character)
    resolve_suffix_tree(tree_Sm)

    # print(tree_Sm.fancyprint())
    return tree_Sm


def faked_tree():
    rootNode = utils.Node("")
    rootNode.add_child(utils.Node("$", 7))
    rootNode.add_child(utils.Node("124233$", 1))

    node = utils.Node("2")
    node.add_child(utils.Node("33$", 4))
    node.add_child(utils.Node("4233$", 2))
    rootNode.add_child(node)

    node = utils.Node("3")
    node.add_child(utils.Node("$", 6))
    node.add_child(utils.Node("3$", 5))
    rootNode.add_child(node)

    rootNode.add_child(utils.Node("4233$", 3))

    return rootNode

    # refine Tree_Sm to generate odd suffix tree Tree_o
    # TODO: fake above recursive call, implement refining of Tree_Sm

    print('Not implemented yet')


def T_even(t_odd, inputstr):
    S = inputstr
    n = len(S)

    # (i)
    # find the lexicographical ordering of the even suffixes
    odd_suffix_ordering = [n.id for n in t_odd.leaflist()]

    # even_suffixes is a list of tuples (x[2i], suffix[2i + 1]) to radix sort
    even_suffixes = [(int(S[n-2]), n) for n in odd_suffix_ordering if n != 1]
    
    radixsort.sort(even_suffixes, 0)

    even_suffixes = [tup[1] - 1 for tup in even_suffixes]
    # in case S is of even length, n % 2 == 0, the even suffix at pos n
    # is the last one in the sorted list, as it starts with character '$'
    # which, by definition, is ranked as |alphabet| + 1, i.e. last character
    if n % 2 == 0:
        even_suffixes.append(S[n - 1])
    
    assert even_suffixes == [12, 2, 10, 6, 8, 4]
    
    # (ii)
    # compute lcp for adjacent even suffixes
    lcp = {}
    for idx in range(0, len(even_suffixes) - 1):
        i = even_suffixes[idx]
        j = even_suffixes[idx + 1]
        curr_lcp = 0
        while i < n and j < n:
            if S[i-1] == S[j-1]:
                curr_lcp += 1
                i += 1
                j += 1
            else:
                break
        lcp[(even_suffixes[idx], even_suffixes[idx + 1])] = curr_lcp
    
    assert lcp[(12, 2)] == 1
    assert lcp[(2, 10)] == 1
    assert lcp[(10, 6)] == 0
    assert lcp[(6, 8)] == 1
    assert lcp[(8, 4)] == 2

    # (iii)
    # construct T_even using information from (i) and (ii)
    root = utils.Node(aId='root')
    fst_suf = even_suffixes[0]
    str_fst_suf = S[fst_suf - 1:]
    node_fst_suf = utils.Node(aParentEdge=str_fst_suf, aId=fst_suf)
    root.add_child(node_fst_suf)
    id2node = {fst_suf: node_fst_suf}

    # TODO: DESCRIBE THE THREE CASES BELOW
    #   - lcp = 0:          new child of root node
    #   - lcp = prev_lcp:   siblings, new node as child of prev_node's parent
    #   - lcp > prev_lcp:   new inner node somewhere on parentEdge of prev_node
    
    for i in range(1, len(even_suffixes)):
        prev_suf = even_suffixes[i - 1]
        curr_suf = even_suffixes[i]

        curr_lcp = lcp[(prev_suf, curr_suf)]
        prev_lcp = None
        if i > 1:
            prevprev_suf = even_suffixes[i - 2]
            prev_lcp = lcp[(prevprev_suf, prev_suf)]
        
        if curr_lcp == 0:
            new_node = utils.Node(aParentEdge=S[curr_suf - 1:], aId=curr_suf)
            root.add_child(new_node)
            id2node[curr_suf] = new_node
        else:
            if prev_lcp:
                if prev_lcp == curr_lcp:
                    # siblings
                    str_curr_remaining = S[curr_suf - 1 + curr_lcp:]
                    new_node = utils.Node(aParentEdge=str_curr_remaining, aId=curr_suf)
                    prev_node = id2node[prev_suf]
                    prev_node.parent.add_child(new_node)
                else:
                    # We need a nifty way to determine parentEdge of the
                    # added innernode in this case, based on parentEdge
                    # of prev_node, length of prev_suf and length of lcp

                    # See drawing on sharelatex for this particular case
                    
                    prev_node = id2node[prev_suf]

                    str_prev_suf = S[prev_suf - 1:]
                    prev_node_prevprev_node_lcp = len(str_prev_suf) - len(prev_node.parentEdge)

                    len_innernode_parentEdge = curr_lcp - prev_node_prevprev_node_lcp
                    start_idx = curr_suf - 1 + prev_node_prevprev_node_lcp
                    end_idx = start_idx + len_innernode_parentEdge
                    innernode_parentEdge = S[start_idx:end_idx]
                    newnode_parentEdge = S[end_idx:]

                    innernode = utils.Node(aParentEdge=innernode_parentEdge, aId='inner2')
                    new_node = utils.Node(aParentEdge=newnode_parentEdge, aId=curr_suf)
                    prev_node_parent = prev_node.parent
                    prev_node_parent.children[-1] = innernode
                    prev_node.parentEdge = prev_node.parentEdge[len_innernode_parentEdge:]
                    innernode.parent = prev_node_parent
                    innernode.add_child(prev_node)
                    innernode.add_child(new_node)

            else:
                str_curr_lcp = S[curr_suf - 1:curr_suf - 1 + curr_lcp]
                innernode = utils.Node(aParentEdge=str_curr_lcp, aId='inner')

                str_curr_remaining = S[curr_suf - 1 + curr_lcp:]
                new_node = utils.Node(aParentEdge=str_curr_remaining, aId=curr_suf)
                id2node[curr_suf] = new_node
                prev_node = id2node[prev_suf]

                # update prev_node by removing lcp from its parentEdge
                # as it has been assigned a new parent who's parentEdge
                # is exactly lcp
                prev_node.parentEdge = prev_node.parentEdge[len(str_curr_lcp):]

                prev_node.parent.children[-1] = innernode
                innernode.parent = prev_node.parent

                # important! prev_node must be added before new_node to
                # keep lexicographic ordering of children
                innernode.add_child(prev_node)
                innernode.add_child(new_node)

    t_even = root
    print(t_even.fancyprint())
    return t_even


def overmerge(t_even, t_odd):
    print('Not implemented yet')


def cleanup_overmerge(t_overmerged):
    print('Not implemented yet')


def main():
    construct_suffix_tree(input)


if __name__ == '__main__':
    main()
