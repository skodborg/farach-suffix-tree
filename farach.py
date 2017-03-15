import math
import radixsort
from utils import Node
import check_correctness
from collections import deque

input = '121112212221'
# input = '111222122121'
# input = '12121212121'
# input = 'banana'
# input = 'mississippi'
# input = 'mississippiisaniceplaceithink'
# input = '123232'
# input = '12122'
input = '12121'
# input = '121112212221'
# input = "121112212221"
# input = "111222122121"
# input = '126226037782486288489207273602'
# input = '0928330960'
# input = '9200662209'

# input = '1600637607'
# input = '6656559814'
# input = '8848442145'
# input = '5515119'
# input = '1708753703'
# input = '7955656566'
# input = '9444479944'

# input = '0101001'  # different than the ones above

# FAILING INPUTS
# input = '47641143403300303358'

# input = '4747744779'
# input = '277653677653329'
# input = '984615083464848'
# input = '202040025603256'

# input = '246919686846819'

# input = '05999'
# input = '0727279295'
# input = '4462002852916712528896186210216114803635460468672254689891567755196614186539689399314081854222959575'
# input = '2009910000'
# input = '5266890832377881042143492847875713654849313015328496190712228381480260997898074306528359078484668401'
# input = '4402530220'
# input = '9380802918'
input = '7644766807'
input = '6494926486'
input = '4586074584'
input = '0479047380'
input = '3486949489'
input = '2576942512'
input = '296842296705529'
input = '773683253687536'
input = '633648376335563'
input = '7770653892593881164670670'
input = 'banana'
input = '11112122'



def str2int(string):
    ''' list append is O(1), string join() is O(n), totaling O(n) conversion
        time from string to string over int alphabet '''
    int_alph = {}
    new_str_list = []
    count = 1
    for c in string:
        if c not in int_alph:
            int_alph[c] = count
            count += 1
        new_str_list.append(int_alph[c])
    # new_str = ''.join(new_str_list)
    return new_str_list


def append_unique_char(string):
    # O(n) running time
    count = 0
    seen_chars = {}
    for c in string:
        if c not in seen_chars:
            count += 1
            seen_chars[c] = count
    string.append(count + 1)
    return string


def construct_suffix_tree(inputstr, printstuff=False):
    # assumes inputstr converted to integer alphabet, takes O(n) to do anyway
    inputstr = append_unique_char(inputstr)

    if len(inputstr) - 1 == 1:
        # inputstr was just a single char before we appended the unique_char
        root = Node(aId='root')
        root.add_child(Node(aId=1, aStrLength=2))
        root.add_child(Node(aId=2, aStrLength=1))
        return root
    elif len(inputstr) - 1 == 2:
        # inputstr was two chars before we appended the unique_char
        root = Node(aId='root')
        suffix1 = inputstr
        suffix2 = inputstr[1:]
        if suffix1[0] == suffix2[0]:
            inner = Node(aId='inner', aStrLength=1)
            root.add_child(inner)
            inner.add_child(Node(aId=1, aStrLength=2))
            inner.add_child(Node(aId=2, aStrLength=1))
            root.add_child(Node(aId=3, aStrLength=1))
        elif suffix1[0] < suffix2[0]:
            root.add_child(Node(aId=1, aStrLength=3))
            root.add_child(Node(aId=2, aStrLength=2))
            root.add_child(Node(aId=3, aStrLength=1))
        else:
            root.add_child(Node(aId=2, aStrLength=2))
            root.add_child(Node(aId=1, aStrLength=3))
            root.add_child(Node(aId=3, aStrLength=1))
        return root

    t_odd = T_odd(inputstr)
    if printstuff:
        print('odd tree for %s' % inputstr)
        print(t_odd.fancyprint(inputstr))

    t_even = T_even(t_odd, inputstr)
    if printstuff:
        print('even tree for %s' % inputstr)
        print(t_even.fancyprint(inputstr))   
    
    if printstuff:
        t_overmerged = overmerge(t_even, t_odd, inputstr, printstuff)
        print('overmerge tree for %s' % inputstr)
        print(t_overmerged.fancyprint(inputstr))
    else:
        t_overmerged = overmerge(t_even, t_odd, inputstr, printstuff)

    #print('before')
    # test_child_parent_relations(t_overmerged)
    compute_lcp_tree(t_overmerged)
    adjust_overmerge(t_overmerged, t_even, t_odd, inputstr)


    #print('after')
    # test_child_parent_relations(t_overmerged)
    #print('good')

    cleanup_tree(t_overmerged)
    if printstuff:
        print('adjusted tree for %s' % inputstr)
        print(t_overmerged.fancyprint(inputstr))
    
    return t_overmerged


def create_tree(tree, root):
    def helper(lvl, node):
        for n in node.children:
            n_id = n.id
            if type(n_id) is str:
                n_id = "\"%s\"" % n.id
            print("inner%s = Node(%s, %s)"
                  % (lvl + 1, n.str_length, n_id))
            print("inner%s.add_child(inner%s)" % (lvl, lvl + 1))
            helper(lvl + 1, n)
    tree_id = tree.id
    if type(tree_id) is str:
                tree_id = "\"%s\"" % tree.id
    print("%s = Node(%s,%s)" % (root, tree.str_length, tree_id))
    for n in tree.children:
        n_id = n.id
        if type(n_id) is str:
            n_id = "\"%s\"" % n.id
        print("inner1 = Node(%s, %s)" % (n.str_length, n_id))
        print("%s.add_child(inner1)" % root)
        helper(1, n)


def T_odd(inputstr):
    S = inputstr
    n = len(S)

    # def rank2char(node, eos_char):
    #     ''' swaps ranks in trees with corresponding character pair
    #         from original string
    #         NOTE! This is an O(n^2) operation!! Cannot use as a premise
    #               for constructing trees and claim linear time spent,
    #               this can only be used for pretty representations during
    #               implementation
    #     '''
    #     new_edge = []
    #     for c in node.parentEdge:
    #         if(c == eos_char):
    #             #       we never want to replace eos_char with anything.
    #             #       eos_char is added specifically for
    #             #       Sm, and we want to adjust the tree edges to correspond
    #             #       to strings found in S and not Sm, therefore there is
    #             #       no corresponding character in S to replace eos_char in
    #             #       Sm with, hence we replace with nothing. This leaves a
    #             #       single edge with only eos_char on it, which we manually
    #             #       remove in the adjustment code, the same code that also
    #             #       makes use of this rank2char-function
    #             if len(S) % 2 == 1:
    #                 if node.is_leaf():
    #                     # we have a leaf node! and we have an even inputstr!
    #                     # we need to append '$' to the end of the parentEdge
    #                     # in this case
    #                     new_edge.append(S[-1])

    #             # if(len(inputstr) % 2 == 1):
    #                 # SPECIAL CASE:
    #                 #   the eos_char ('$' in the book) is not a part of
    #                 #   any of the ranks, but it must still sit at the end
    #                 #   of every suffix in the final suffix tree T_odd,
    #                 #   so we simply swap the last character of the string
    #                 #   of ranks (the '$' added by the recursive call) and
    #                 #   the last character of the inputstr (the actual '$' on
    #                 #   the current alphabet on the current input)
    #                 # example:
    #                 #   inputstr is 121112212221
    #                 #   construct_suffix_tree adds the '$', which is then
    #                 #   converted to a '3' in str2int, giving 1211122122213
    #                 #   The string of rankings of character pairs are then
    #                 #   created, giving us '212343'
    #                 #   This string is now subject to a recursive call, which
    #                 #   also appends a '$', which in this case is converted
    #                 #   to '5'
    #                 #   If, when ranking the original inputstr, '13' was not
    #                 #   a character pair (because the string was of even
    #                 #   length), then we need to insert these '3's manually.
    #                 #   They have to be placed exactly where '5' occurs in
    #                 #   the returned suffix tree, which is what happens here
    #             continue
    #         else:
    #             pair = single2pair[int(c)]
    #             new_edge.append(pair[0])
    #             new_edge.append(pair[1])
    #     node.parentEdge = new_edge

    #     for n in node.children:
    #         rank2char(n, eos_char)

    def extend_length(node):

        def helper(node):
            if node.is_leaf():
                node.id = node.id * 2 - 1
                node.str_length = n - node.id + 1
            else:
                node.str_length *= 2
        node.traverse(helper)



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
            inner = Node(node.str_length + 1, "inner")
            for cm in current_merg:
                inner.add_child(cm)
            children_list.append(inner)

        current_char = ''
        current_merg = []
        children_list = []

        # If node is a leaf, update node id to represent the actually length
        # of string after de-ranking
        if(node.is_leaf()):
            return

        for child in node.children:
            if child.str_length == 0:
                continue

            if child.is_leaf():
                leaf_id = child.id
            else:
                leaf_descendant = child.leaflist[0]
                leaf_id = leaf_descendant.id

            first_edge_char = S[leaf_id + child.parent.str_length-1]

            if(first_edge_char == current_char or current_char == ''):
                current_merg.append(child)
                current_char = first_edge_char
            else:
                if(len(current_merg) > 1):
                    merge()
                else:
                    children_list.extend(current_merg)

                current_char = first_edge_char
                current_merg = [child]

        if(len(current_merg) > 1):
            merge()
        else:
            children_list.extend(current_merg)

        node.children = []
        for n in children_list:
            node.add_child(n)
        
        # Correcting tree if a node only has one child.
        # This happens when the parentEdges of all children started with the
        # same character
        # In this case we must delete it by updating parent's parentEdge
        # and transfer all children
        if len(children_list) == 1 and node.id is not 'root':
            # node.parentEdge += node.children[0].parentEdge
            node.str_length = node.children[0].str_length
            node.children = node.children[0].children
            for n in node.children:
                n.parent = node

        for n in node.children:
            resolve_suffix_tree(n)

    # strings are 0-indexed in python, and 1-indexed in the book's examples
    # so we -2 and -1 from pos 'i' to let our match the book's examples
    chr_pairs = [(int(S[2 * i - 2]), int(S[2 * i - 1]))
                 for i in range(1, math.floor(n / 2) + 1)]

    # sort in O(k * n) using radix sort (k = 2 here, guaranteed)
    radixsort.sort(chr_pairs)

    # remove duplicates, O(n)
    unique_chr_pairs = [chr_pairs[0]]
    for pair in chr_pairs[1:]:
        if unique_chr_pairs[-1] != pair:
            unique_chr_pairs.append(pair)
    chr_pairs = unique_chr_pairs

    # compute S'[i] = rank of (S[2i - 1], S[2i])
    Sm = []
    count = 1
    pair2single = {}  # lookup is O(1) for pairs to single character mapping
    #single2pair = {}  # lookup is O(1) for single to pair character mapping

    for pair in chr_pairs:
        pair2single[pair] = count
        #single2pair[count] = pair
        count += 1
    for i in range(1, math.floor(n / 2) + 1):
        pair = (int(S[2 * i - 2]), int(S[2 * i - 1]))
        Sm.append(pair2single[pair])


    tree_Sm = construct_suffix_tree(Sm)
    tree_Sm.update_leaf_list()

    # print('for Sm = %s the returned tree is' % Sm)
    # print(tree_Sm.fancyprint())

    # convert edge characters from ranks to original character pairs
    # + convert leaf ids to corresponding original suffix ids
    #eos_char = tree_Sm.leaflist()[0].parentEdge[-1]
    #rank2char(tree_Sm, eos_char)

    extend_length(tree_Sm)

    # print('after rank2char:')
    # print(tree_Sm.fancyprint())

    # massage into proper compacted trie
    # (no edges of a node share first character)

    tree_Sm.update_leaf_list()

 
    resolve_suffix_tree(tree_Sm)



    tree_Sm.update_leaf_list()
    return tree_Sm


def T_even(t_odd, inputstr):
    S = inputstr
    n = len(S)

    # (i)
    # find the lexicographical ordering of the even suffixes
    odd_suffix_ordering = [node.id for node in t_odd.leaflist]

    # even_suffixes is a list of tuples (x[2i], suffix[2i + 1]) to radix sort
    even_suffixes = [(int(S[node - 2]), node) for node in odd_suffix_ordering
                     if node != 1]

    radixsort.sort(even_suffixes, 0)

    even_suffixes = [tup[1] - 1 for tup in even_suffixes]
    # in case S is of even length, n % 2 == 0, the even suffix at pos n
    # is the last one in the sorted list, as it starts with character '$'
    # which, by definition, is ranked as |alphabet| + 1, i.e. last character
    # We need to add this one specifically, as it is not found by counting
    # all odd suffixes down by one
    # e.g.: if the inputstr is of length 4, then odd suffixes are 1 and 3
    #       if we only count even suffixes as odd suffixes prefixed with
    #       a character, we will never capture 4, as 5 is not an odd suffix
    #       hence why we need to manually add it as the last one as it is '$'
    if n % 2 == 0:
        even_suffixes.append(n)

    # (ii)
    # compute lcp for adjacent even suffixes
    # TODO: NOT O(n), TREE SHOULD BE PREPROCESSED ACCORDING TO [HT84]
    lcp = {}
    for idx in range(0, len(even_suffixes) - 1):
        i = even_suffixes[idx]
        j = even_suffixes[idx + 1]
        curr_lcp = 0
        while i < n and j < n:
            if S[i - 1] == S[j - 1]:
                curr_lcp += 1
                i += 1
                j += 1
            else:
                break
        lcp[(even_suffixes[idx], even_suffixes[idx + 1])] = curr_lcp

    # (iii)
    # construct T_even using information from (i) and (ii)
    root = Node(aId='root')
    fst_suf = even_suffixes[0]
    fst_suf_len = n - fst_suf + 1 # S[fst_suf - 1:]


    node_fst_suf = Node(fst_suf_len, fst_suf)
    root.add_child(node_fst_suf)
    id2node = {fst_suf: node_fst_suf}
    for i in range(1, len(even_suffixes)):
        prev_suf = even_suffixes[i - 1]
        curr_suf = even_suffixes[i]
        curr_lcp = lcp[(prev_suf, curr_suf)]
        prev_lcp = None
        if i > 1:
            prevprev_suf = even_suffixes[i - 2]
            prev_lcp = lcp[(prevprev_suf, prev_suf)]

        if curr_lcp == 0:
            curr_suf_len = n - curr_suf + 1
            new_node = Node(curr_suf_len, curr_suf)
            root.add_child(new_node)
            id2node[curr_suf] = new_node
        else:
            if prev_lcp:

                prev_node = id2node[prev_suf]

                # str_prev_suf = S[prev_suf - 1:]
                # prev_node_prevprev_node_lcp =
                #   len(str_prev_suf) - len(prev_node.parentEdge)
                # TODO: why not use len(prev_lcp) instead of the above?
                # assert prev_lcp == prev_node_prevprev_node_lcp

            
                # we need to append the new node to somewhere on the
                # path from root to the parent of the prev_node.
                # This might involve following a lot of nodes'
                # parentEdges to find the spot
                # TODO: is it O(n)???
                remaining_until_insertion = prev_lcp - curr_lcp

                possible_insertion_node = prev_node.parent
                while remaining_until_insertion > 0:
                    # run up through parentEdges until
                    # remaining_until_insertion is 0
                    len_of_edge = possible_insertion_node.str_length - possible_insertion_node.parent.str_length

                    remaining_until_insertion -= len_of_edge
                    possible_insertion_node = possible_insertion_node.parent

                # possible_insertion_node is now the spot at which we
                # should place curr_suf
                # we need to pop the rightmost child of the
                # possible_insertion_node as we need to insert an inner
                # node with this child and our new_node as children in
                # place of this rightmost child, if
                # remaining_until_insertion is negative and not exactly
                # 0, in which case we can just add_child(new_node)

                if remaining_until_insertion == 0:
                    # new_node_parentEdge = S[curr_suf - 1 + curr_lcp:]
                    len_newnode = n - curr_suf + 1
                    # new_node = Node(new_node_parentEdge, curr_suf)
                    new_node = Node(len_newnode, curr_suf)
                    id2node[curr_suf] = new_node
                    possible_insertion_node.add_child(new_node)
                else:
                    
                    child_of_insertion_node = possible_insertion_node.children.pop()
                    split_idx = abs(remaining_until_insertion)
                    #inner_parentEdge = child_of_insertion_node.parentEdge[:split_idx]
                    inner_parentEdge_len = child_of_insertion_node.parent.str_length + split_idx 
                    #child_of_insertion_parentEdge = child_of_insertion_node.parentEdge[split_idx:]
                    innernode = Node(inner_parentEdge_len, 'inner')
                    # child_of_insertion_node.parentEdge = child_of_insertion_parentEdge
                    # new_node_parentEdge = S[curr_suf - 1 + curr_lcp:]
                    len_newnode = n - curr_suf + 1
                    # new_node = Node(new_node_parentEdge, curr_suf)
                    new_node = Node(len_newnode, curr_suf)

        
                    possible_insertion_node.add_child(innernode)

                    innernode.add_child(child_of_insertion_node)
                    innernode.add_child(new_node)

                    id2node[curr_suf] = new_node

            else:

                #str_curr_lcp = S[curr_suf - 1:curr_suf - 1 + curr_lcp]
                innernode_len = curr_lcp
                innernode = Node(innernode_len, 'inner')

                #str_curr_remaining = S[curr_suf - 1 + curr_lcp:]
                new_node_len = n - curr_suf + 1
                new_node = Node(new_node_len, curr_suf)

                id2node[curr_suf] = new_node
                prev_node = id2node[prev_suf]

                # update prev_node by removing lcp from its parentEdge
                # as it has been assigned a new parent who's parentEdge
                # is exactly lcp
                #prev_node.parentEdge = prev_node.parentEdge[len(str_curr_lcp):]

                prev_node.parent.children[-1] = innernode
                innernode.parent = prev_node.parent

                # important! prev_node must be added before new_node to
                # keep lexicographic ordering of children
                innernode.add_child(prev_node)
                innernode.add_child(new_node)
    t_even = root
    t_even.update_leaf_list()
    return t_even


def overmerge(t_even, t_odd, S, printstuff=False):

    t_overmerged = Node(aId="root", aStrLength=0)

    def merger_helper(current, even, odd):
        even_children = even.children
        odd_children = odd.children
        e = 0
        o = 0

        while (e < len(even_children) or o < len(odd_children)):
            e_child = None
            e_char = None
            o_child = None
            o_char = None

            if(e < len(even_children)):
                e_child = even_children[e]
                if e_child.is_leaf():
                    leaf_id = e_child.id
                else:
                    leaf_descendant = e_child.leaflist[0]
                    leaf_id = leaf_descendant.id
           
                e_char = S[leaf_id + e_child.parent.str_length -1]
                
            if(o < len(odd_children)):
                o_child = odd_children[o]
                if o_child.is_leaf():
                    leaf_id = o_child.id
                else:
                    leaf_descendant = o_child.leaflist[0]
                    leaf_id = leaf_descendant.id

                o_char = S[leaf_id + o_child.parent.str_length -1]
                
            if(e_child is None):
                o += 1
                o_child.old_parent = o_child.parent
                current.add_child(o_child)
                # prepare the LCA nodepair thingy during the overmerge            
                if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca'):
                    if o_child.is_leaf():
                        current.lca_odd = o_child
                    else:
                        current.lca_odd = o_child.leaflist[0]
                    if printstuff:
                        print('case 1 added %s' % current.lca_odd)
                if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca') and hasattr(current, 'lca_odd'):
                    if hasattr(e_child, 'lca_even'):
                        current.lca_even = e_child.lca_even
                continue

            if(o_child is None):
                e += 1
                e_child.old_parent = e_child.parent
                current.add_child(e_child)
                # prepare the LCA nodepair thingy during the overmerge
                if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca'):
                    if e_child.is_leaf():
                        current.lca_even = e_child
                    else:
                        current.lca_even = e_child.leaflist[0]
                    if printstuff:
                        print('case 2 added %s' % current.lca_even)
                    # continue
                if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca') and hasattr(current, 'lca_even'):
                    if hasattr(e_child, 'lca_odd'):
                        current.lca_odd = e_child.lca_odd
                continue

            if(o_char != e_char):
                # Case 1
                # If the first char of the two parentEdges doesnt match, insert
                # the the first char (by lexicographic order), and insert.
                # Count that up to preceed to next child in child list
                if(o_char < e_char):
                    o_child.old_parent = o_child.parent
                    current.add_child(o_child)
                    o += 1
                    # prepare the LCA nodepair thingy during the overmerge
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca'):
                        if o_child.is_leaf():
                            current.lca_odd = o_child
                        else:
                            current.lca_odd = o_child.leaflist[0]
                        if printstuff:
                            print('case 3 added %s' % current.lca_odd)
                    if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca') and hasattr(current, 'lca_odd'):
                        if hasattr(o_child, 'lca_even'):
                            current.lca_even = o_child.lca_even
                else:
                    e_child.old_parent = e_child.parent
                    current.add_child(e_child)
                    e += 1
                    # prepare the LCA nodepair thingy during the overmerge
                    if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca'):
                        if e_child.is_leaf():
                            current.lca_even = e_child
                        else:
                            current.lca_even = e_child.leaflist[0]
                        if printstuff:
                            print('case 4 added %s' % current.lca_even)
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca'):
                        if hasattr(e_child, 'lca_odd'):
                            current.lca_odd = e_child.lca_odd
            else:
                # Even and odd have same first char in parent edge
                e_parentEdge_len = e_child.str_length - current.str_length
                o_parentEdge_len = o_child.str_length - current.str_length
                #e_parentEdge = e_child.parentEdge
                #o_parentEdge = o_child.parentEdge
                if(e_parentEdge_len != o_parentEdge_len):
                    # Case 3
                    # If the two parentEdge's start with the same char, and is
                    # not of equal length
                    # We will then decide which node has the longest parent
                    # edge, insert this into our current merge tree
                    # we will then call recursively on this edge, and on the
                    # child with the longer edge. We do this be introducing
                    # an substitue node, which only purpose is to make the
                    # recursive call possible.
                   
                    short_child = o_child
                    long_child = e_child
                    swapped = False
                    if e_parentEdge_len < o_parentEdge_len:
                        swapped = True
                        short_child = e_child
                        long_child = o_child

                    short_child.old_parent = short_child.parent
                    long_child.old_parent = long_child.parent

                    inner_node = Node(short_child.str_length, short_child.id)
                    current.add_child(inner_node)
                    
                    # subtrees added for reference in adjust_overmerge
                    inner_node.even_subtree = e_child
                    inner_node.odd_subtree = o_child

                    #e_child.old_parentEdge = e_child.parentEdge
                    #o_child.old_parentEdge = o_child.parentEdge
                    short_child_sub = Node(short_child.str_length, aId="sub_" + str(short_child.id))

                    #long_child.parentEdge = long_child.parentEdge[len(short_child.parentEdge):]
                    short_child_sub.add_child(long_child)

                    if not short_child.children:
                        # prepare the LCA nodepair thingy in case short_child
                        # is a leaf node itself and is overmerged to have some
                        # subtree containing another heterogenous leaf node
                        if swapped:
                            inner_node.lca_even = short_child
                        else:
                            inner_node.lca_odd = short_child


                    if swapped:
                        # short_child originates in even_tree
                        merger_helper(inner_node, short_child, short_child_sub)
                    else:
                        # short_child originates in odd_tree
                        merger_helper(inner_node, short_child_sub, short_child)

                    had_lca_even_too = False
                    overwrote = False
                    if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca'):
                        if hasattr(inner_node, 'lca_even'):
                            current.lca_even = inner_node.lca_even
                            had_lca_even_too = True
                            if hasattr(current, 'overwrite_lca'):
                                overwrote = True
                            if printstuff:
                                print('case 5 added %s to %s' % (inner_node.lca_even, current))
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca') and not overwrote:
                        if hasattr(inner_node, 'lca_odd'):
                            current.lca_odd = inner_node.lca_odd
                            if printstuff:
                                print('case 6 added %s to %s' % (inner_node.lca_odd, current))
                            if had_lca_even_too:
                                # we cached both lca_even and lca_odd from same
                                # child, mark this so one can be overwritten by
                                # whatever leafnode we may see next in another
                                # subtree
                                current.overwrite_lca = True
                                if printstuff:
                                    print('overwrite added to %s with both %s and %s' % (current, inner_node.lca_odd, inner_node.lca_even))


                else:
                    # Case 2
                    # If two parent edge's start with the same char, and are of
                    # equal length, we will ad an internal node, and call our
                    # merger_helper recursively with the two sub trees.

                    # SPECIAL CASE:
                    # if one of either e_child or o_child does not have any children,
                    # then it is a leaf node itself. This means, that we are not
                    # creating and merging into a new inner, but rather into this
                    # particular leaf node, creating a leaf node with a subtree
                    # being the subtree of the other node
                    # Note, that both e_child and o_child cannot have empty children
                    # lists, as that would mean they were both leaf nodes. But as
                    # we have already made sure that their string lengths are equal,
                    # there would be two suffixes in the tree of equal length,
                    # which is impossible

                    # W.r.t. LCA nodepairs, this current node should never be LCA
                    # of any odd/even nodepair as a result of this merge, as every
                    # odd/even node in the merge will be child of 'inner', which is
                    # current's child, so the nodepairs should instead have 'inner'
                    # as LCA. It may still be LCA of some nodepair, but this is a
                    # result of one of the other overmerge cases
                    e_parentEdge_len = o_child.str_length
                    inner_id = 'inner'
                    inner = Node(e_parentEdge_len, inner_id)
                    # print('processing node %s with subtrees %s and %s' % (current, e_child, o_child))

                    if not e_child.children:
                        inner.id = e_child.id
                        inner.lca_even = e_child
                        if printstuff:
                            print('case 7 added %s to %s' % (e_child, inner))
                    if not o_child.children:
                        inner.id = o_child.id
                        inner.lca_odd = o_child
                        if printstuff:
                            print('case 8 added %s to %s' % (o_child, inner))

                    current.add_child(inner)
                    inner.even_subtree = e_child
                    inner.odd_subtree = o_child
                    merger_helper(inner, e_child, o_child)

                    had_lca_even_too = False
                    overwrote = False
                    if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca'):
                        if hasattr(inner, 'lca_even'):
                            current.lca_even = inner.lca_even
                            had_lca_even_too = True
                            if hasattr(current, 'overwrite_lca'):
                                overwrote = True
                            if printstuff:
                                print('case 9 added %s to %s' % (current.lca_even, current))
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca') and not overwrote:
                        if hasattr(inner, 'lca_odd'):
                            current.lca_odd = inner.lca_odd
                            if printstuff:
                                print('case 10 added %s to %s' % (current.lca_odd, current))
                            if had_lca_even_too:
                                current.overwrite_lca = True
                o += 1
                e += 1
    merger_helper(t_overmerged, t_even, t_odd)
    t_overmerged.update_leaf_list()
    return t_overmerged


def naive_lca(node1, node2, tree, id2node):
    ''' strategy:   from node1, test if node2 is in the subtree of node1
                        - if so, report node1 as LCA
                    if not, proceed to parent node and do:
                        - if parent node is node2, report parent node as LCA
                        - if parent node has node2 in its subtree, report
                          parent node as LCA
                        - if neither, recurse to parent's parent
        running time: awful!
    '''
    # Notice:   there may be a difference between the node1 and node2
    #           as they are given and the final state of node1 and node2,
    #           therefore id2node is necessary for now
    node1 = id2node[node1.id]
    node2 = id2node[node2.id]

    def node_is_descendant(node1, node2):
        descendants = []
        node1.traverse(lambda n: descendants.append(n)
                       if 'inner' not in str(n.id) else 'do nothing')
        is_descendant = True in [n.id == node2.id for n in descendants]
        return is_descendant

    curr_node = node1
    no_result = True

    while no_result:
        if curr_node.id == "root":
            no_result = False

        if node_is_descendant(curr_node, node2):
            no_result = False
            return curr_node
        else:
            curr_node = curr_node.parent

    return None


def compute_lcp_tree(t_overmerged):
    ''' Augments every, to the algorithm relevant, node in t_overmerged with
        an attribute, node.suffix_link, pointing to the node representing
        the string of the current node minus first character
        Running time: O(n)
    '''


    


    leafnode_occurences = []
    # pairs2append = []
    def append_leafnodes(node):
        if type(node.id) is int:
            leafnode_occurences.append(node)
            # if node.children:

            #     first = node.children[0]
            #     if type(first.id) is int:
            #         for c in node.parent.children:
            #             if type(c.id) is int and c.id != node.id:
            #                 if c.id % 2 != first.id % 2:
            #                     pairs2append.append((first, c))
            #                     break
                    #for c in node.parent.children:
                    #    if type(c.id) is str:
                    #        for c2 in c.children:
                    #            if type(c2.id) is int and c2.id != node.id:
                    #                if c2.id % 2 != first.id % 2:
                    #                    pairs2append.append((first, c2))
           
                    

            

    t_overmerged.traverse(append_leafnodes)

  
    #print("pairs 2 append")
    #print(pairs2append)

    # lca_nodepairs = []
    # prev_node = None
    # pairings = []
    # for n in range(len(leafnode_occurences)):
    #     node = leafnode_occurences[n]
    #     # print(node.id)
    #     if not prev_node and n > 0 and node.id % 2 != leafnode_occurences[n - 1].id % 2:
    #         for pairingnode in pairings[:-1]:
    #             if pairingnode.id %2 != node.id % 2:
    #                 lca_nodepairs.append((pairingnode, node))
    #         prev_node = leafnode_occurences[n - 1]
    #         pairings = []
    #     if prev_node and node.id % 2 == prev_node.id % 2:
    #         for pairingnode in pairings:
    #             if pairingnode.id %2 != prev_node.id % 2:
    #                 lca_nodepairs.append((prev_node, pairingnode))
    #         for pairingnode in pairings:
    #             if pairingnode.id %2 != node.id % 2:
    #                 lca_nodepairs.append((pairingnode, node))
    #         prev_node = node
    #         pairings = []
    #         continue
    #     pairings.append(node)
    #     # print(pairings)
    # if pairings:
    #     for pairingnode in pairings:
    #         if pairingnode.id %2 != prev_node.id % 2:
    #             lca_nodepairs.append((prev_node, pairingnode))


    # CHEAT
    # lca_nodepairs = []
    # for n1 in leafnode_occurences:
    #     for n2 in leafnode_occurences:
    #         if n1.id % 2 != n2.id % 2:
    #             lca_nodepairs.append((n1, n2))
    # print(lca_nodepairs)
    # print(lca_nodepairs[0][0].children)

    
    '''curr_node = leafnode_occurences[0]
    for node in leafnode_occurences[1:]:
        if curr_node.id % 2 == node.id % 2:
            # we found a homogenous pair, swap curr_node for last seen
            # node with parity (even/odd) opposite node
            if lca_nodepairs:
                curr_node = lca_nodepairs[-1][1]
            else:
                curr_node = node
                continue

        lca_nodepairs.append((curr_node, node))'''

    # prev_node = None
    # curr_node = leafnode_occurences[0]
    

    # for n in range(1, len(leafnode_occurences)):
    #     node = leafnode_occurences[n]

    #     # if prev_node:

    #         # if(prev_node.id % 2 != leafnode_occurences[n-1].id % 2):

    #             # pairs2append.append((prev_node, leafnode_occurences[n-1]))
    #         # prev_node = None

    #     if curr_node.id % 2 == node.id % 2:
    #         # we found a homogenous pair, swap curr_node for last seen
    #         # node with parity (even/odd) opposite node
    #         if lca_nodepairs:
    #             curr_node = lca_nodepairs[-1][1]
    #         else:
    #             # prev_node = leafnode_occurences[0]
    #             curr_node = node
    #             continue

    #     # prev_node = leafnode_occurences[n-2]
    #     lca_nodepairs.append((curr_node, node))

    lca_nodepairs = []
    def helper(node):
        nonlocal lca_nodepairs
        if hasattr(node, 'lca_even'):
            lca_nodepairs.append((node.lca_even, node.lca_odd))
    t_overmerged.traverse(helper)    
    # print(lca_nodepairs)


    # given 'i', access node representing i'th suffix in O(1)
    # using O(n) preprocessing time - assumed in algorithm
    # if pairs2append:
    #     lca_nodepairs.extend(pairs2append)

    # print(lca_nodepairs)
    
    id2node = []
    t_overmerged.traverse(lambda n: id2node.append((n.id, n))
                          if 'inner' not in str(n.id) else 'do nothing')
    id2node = dict(id2node)


    # ---------------------------------------
    # CREATE LCP TREE
    # ---------------------------------------
    for node1, node2 in lca_nodepairs:
        # TODO: using naive_lca to find lca to create suffix link, this
        #       must instead be the constant time lookup as described in
        #       the article [Ht84], otherwise we do not achieve O(n) running
        #       time for the algorithm
        lca = naive_lca(node1, node2, t_overmerged, id2node)

        if (lca.id == 'root' or
                node1.id + 1 not in id2node or
                node2.id + 1 not in id2node):
            # we cannot create a suffix link from root as it is undefined
            continue
        node1_next = id2node[node1.id + 1]
        node2_next = id2node[node2.id + 1]
        lca_parent = naive_lca(node1_next, node2_next, t_overmerged, id2node)

        lca.suffix_link = lca_parent
    # ---------------------------------------
    # ADD LCP DEPTH TO ALL NODES USING A SINGLE DFS
    # ---------------------------------------
    def lcp_depth(node):
        if hasattr(node, 'lcp_depth'):
            # we already computed this node as a result of computing an
            # earlier node with a suffix link to this node, no need to
            # repeat the computation

            return node.lcp_depth

        if hasattr(node, 'suffix_link'):
            if not hasattr(node.suffix_link, 'lcp_depth'):
                # our suffix link is to a node for which we have not yet
                # computed the lcp depth; do so, return it to here and
                # continue the bfs. This is still within O(n) as we simply
                # skip the node when we encounter it the second time in
                # the initial bfs
                node.lcp_depth = lcp_depth(node.suffix_link) + 1
            node.lcp_depth = node.suffix_link.lcp_depth + 1
     
            return node.lcp_depth
        # print(node.children)
   
    t_overmerged.lcp_depth = 0
    t_overmerged.bfs(lcp_depth)


def test_child_parent_relations(tree):
    def helper(node):
        for child in node.children:
            assert child.parent == node
    tree.traverse(helper)



def adjust_overmerge(t_overmerged, t_even, t_odd, S):
    # def add_str_length(node, prev_length):
    #     # TODO: consider do this as we form the overmerge tree
    #     node.str_length = prev_length + len(node.parentEdge)
    #     for n in node.children:
    #         add_str_length(n, node.str_length)

    # add_str_length(t_overmerged, 0)

    def bfs(tree, fn):
        # breadth-first search
        fifo = deque()
        fifo.append(tree)
        while fifo:
            node = fifo.pop()
            result = fn(node)
            if result == 'continue':
                # skip because we do not need to process this node's children
                continue
            fifo.extendleft(node.children)

    def adjust_overmerge_helper(curr_node):
        # print('adjusting in node %s' % curr_node)

        if(hasattr(curr_node, "lcp_depth")):

            if curr_node.str_length != curr_node.lcp_depth:
                parentEdge_length = curr_node.lcp_depth - curr_node.parent.str_length

                #new_node_parentEdge = curr_node.parentEdge[:parentEdge_length]
        
                curr_node.children = []
                #curr_node.parentEdge = new_node_parentEdge

                curr_node.str_length = curr_node.lcp_depth

                curr_node.id = "inner"
                even_tree = curr_node.even_subtree
                odd_tree = curr_node.odd_subtree

                def helper(node):
                    for child in node.children:
                        child.parent = node
                even_tree.bfs(helper)
                odd_tree.bfs(helper)
                

                # if hasattr(even_tree, "old_parentEdge"):
                #     even_tree.parentEdge = even_tree.old_parentEdge

                # if hasattr(odd_tree, "old_parentEdge"):
                #     odd_tree.parentEdge = odd_tree.old_parentEdge

                # even_tree.parentEdge = even_tree.parentEdge[parentEdge_length:]
                # odd_tree.parentEdge = odd_tree.parentEdge[parentEdge_length:]
                if even_tree.is_leaf():
                    even_leaf_id = even_tree.id
                else:
                    even_leaf_descendant = even_tree.leaflist[0]
                    even_leaf_id = even_leaf_descendant.id

                even_tree_parentEdge_char = S[even_leaf_id - 1 + curr_node.lcp_depth]


                if odd_tree.is_leaf():
                    odd_leaf_id = odd_tree.id
                else:
                    odd_leaf_descendant = odd_tree.leaflist[0]
                    odd_leaf_id = odd_leaf_descendant.id

                odd_tree_parentEdge_char = S[odd_leaf_id - 1 + curr_node.lcp_depth]
                
                if even_tree_parentEdge_char < odd_tree_parentEdge_char:
                    curr_node.add_child(even_tree)
                    curr_node.add_child(odd_tree)
                else:
                    curr_node.add_child(odd_tree)
                    curr_node.add_child(even_tree)
                return 'continue'
                
    # TODO: bfs does not work here, as in the case where we identify
    #       that we can just insert subtrees directly as found in
    #       t_even and t_odd, we do not need to visit children of
    #       this node and process them again, as the subtrees just
    #       inserted are correct. If we queue all children for a bfs
    #       visit, and then replace the whole children list with two
    #       subtrees as found in t_even and t_odd, we will encounter
    #       problems when these are popped from the bfs queue while no
    #       longer part of the tree. This may modify parent nodes of
    #       these replaced children, which were correct, but might be
    #       modified according to some issue found deeper down the wrong,
    #       but already correctly modified subtree of the parent
    #       Fix: custom bfs which, in the case of inserting subtrees from
    #            t_even and t_odd directly, also remembers to pop off the
    #            children of the node, as these should no longer be visited
               
    # t_overmerged.bfs(adjust_overmerge_helper)
    bfs(t_overmerged, adjust_overmerge_helper)
    t_overmerged.update_leaf_list()


def cleanup_tree(t_overmerged):
    # remove suffix links on all nodes with one
    def helper(node):
        if hasattr(node, 'suffix_link'):
            delattr(node, 'suffix_link')
        if hasattr(node, 'old_parent'):
            delattr(node, 'old_parent')
        if hasattr(node, 'old_parentEdge'):
            delattr(node, 'old_parentEdge')
        if hasattr(node, 'lcp_depth'):
            delattr(node, 'lcp_depth')
        if hasattr(node, 'lca_even'):
            delattr(node, 'lca_even')
        if hasattr(node, 'lca_odd'):
            delattr(node, 'lca_odd')
    t_overmerged.traverse(helper)


def main():
    inputstr = str2int(input)
    inputstr_copy = inputstr[:]

    suffix_tree = construct_suffix_tree(inputstr, True)
    print('final tree for input %s:' % inputstr)
    print(suffix_tree.fancyprint(inputstr))

    check_correctness.check_correctness2(inputstr_copy)


if __name__ == '__main__':
    main()
