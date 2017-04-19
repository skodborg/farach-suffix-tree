import math
import radixsort
from utils import Node
import check_correctness
from collections import deque
import lca as fast_lca
import time
import os

input = '121112212221'
# input = '111222122121'
# input = '12121212121'
input = 'mississippi'
# input = 'banana'
input = 'ababcacac'

maxLength = 0
timers = dict()

# input = '1222112221212'

_printstuff = False

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
    global _printstuff, maxLength, timers
    _printstuff = printstuff

    # assumes inputstr converted to integer alphabet, takes O(n) to do anyway
    inputstr = append_unique_char(inputstr)
    if maxLength < len(inputstr):
        maxLength = len(inputstr)
        totalTimerStart = time.time()
        

    if len(inputstr) - 1 == 1:
        # inputstr was just a single char before we appended the unique_char
        root = Node(aId='root')
        root.add_child(Node(aId=1, aStrLength=2))
        root.add_child(Node(aId=2, aStrLength=1))
        return root

    t_odd = T_odd(inputstr)
    printif('odd tree for %s' % inputstr)
    printif(t_odd.fancyprint(inputstr))

    t_even = T_even(t_odd, inputstr)
    printif('even tree for %s' % inputstr)
    printif(t_even.fancyprint(inputstr))
    
    t_overmerged = overmerge(t_even, t_odd, inputstr)
    printif('overmerge tree for %s' % inputstr)
    printif(t_overmerged.fancyprint(inputstr))

    if maxLength == len(inputstr):
        start = time.time()

    compute_lcp_tree(t_overmerged)

    if maxLength == len(inputstr):
        end = time.time()
        total = (end-start)
        if "compute_lcp_tree" in timers:
            timers["compute_lcp_tree"].append((maxLength, total))
        else:
            timers["compute_lcp_tree"] = [(maxLength, total)]

    if maxLength == len(inputstr):
        start = time.time()

    adjust_overmerge(t_overmerged, t_even, t_odd, inputstr)

    if maxLength == len(inputstr):
        end = time.time()
        total = (end-start)
        if "adjust_overmerge" in timers:
            timers["adjust_overmerge"].append((maxLength, total))
        else:
            timers["adjust_overmerge"] = [(maxLength, total)]


    cleanup_tree(t_overmerged)
    printif('adjusted tree for %s' % inputstr)
    printif(t_overmerged.fancyprint(inputstr))

    if maxLength == len(inputstr):
        totalTimerEnd = time.time()
        total = totalTimerEnd- totalTimerStart
        if "total" in timers:
            timers["total"].append((maxLength, total))
        else:
            timers["total"] = [(maxLength, total)]

    if maxLength == len(inputstr):
        os.system('clear')
        

        print(", " + ", ".join([key for key in timers]))
        for i in range(len(timers["total"])):
            print(str(timers["total"][i][0]) + ", " + ", ".join([str(value[i][1]) for value in timers.values()]))

  
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
    global _printstuff, timers
    if(len(inputstr) == maxLength):
        start = time.time()

    S = inputstr
    n = len(S)

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

    for pair in chr_pairs:
        pair2single[pair] = count
        count += 1
    for i in range(1, math.floor(n / 2) + 1):
        pair = (int(S[2 * i - 2]), int(S[2 * i - 1]))
        Sm.append(pair2single[pair])
    
    if(len(inputstr) == maxLength):
        end = time.time()
        curr_time = end - start

    tree_Sm = construct_suffix_tree(Sm, _printstuff)
    if(len(inputstr) == maxLength):
        start = time.time()
    tree_Sm.update_leaf_list()


    extend_length(tree_Sm)


    # massage into proper compacted trie
    # (no edges of a node share first character)

    tree_Sm.update_leaf_list()


    resolve_suffix_tree(tree_Sm)

    tree_Sm.update_leaf_list()
    if(len(inputstr) == maxLength):
        end = time.time()
        total = (end-start) + curr_time
        if "T_odd" in timers:
            timers["T_odd"].append((maxLength, total))
        else:
            timers["T_odd"] = [(maxLength, total)]

    return tree_Sm



def T_even(t_odd, inputstr):
    if(len(inputstr) == maxLength):
        start = time.time()
    S = inputstr
    n = len(S)

    # (i)
    # find the lexicographical ordering of the even suffixes
    leaflist = []
    def get_leafs(node):
        nonlocal leaflist
        if node.is_leaf():
            leaflist.append(node)
    
    t_odd.dfs(get_leafs)

    odd_suffix_ordering = [node.id for node in leaflist]#t_odd.leaflist]

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
    lca_f = fast_lca.LCA()
    lca_f.preprocess(t_odd)

    id2node = []
    t_odd.traverse(lambda n: id2node.append((n.id, n))
                          if 'inner' not in str(n.id) else 'do nothing')
    id2node = dict(id2node)


    lcp = {}
    for idx in range(0, len(even_suffixes) - 1):
        i = even_suffixes[idx]
        j = even_suffixes[idx + 1]
        curr_lcp = 0

        if(S[i-1] == S[j-1] and i < n and j < n):
            if j+1 in id2node and i+1 in id2node:
                lca_parent = lca_f.query(id2node[i+1], id2node[j+1])
                curr_lcp = lca_parent.str_length + 1
            else:
                curr_lcp = 1

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
                    len_newnode = n - curr_suf + 1
                    new_node = Node(len_newnode, curr_suf)
                    id2node[curr_suf] = new_node
                    possible_insertion_node.add_child(new_node)
                else:
                    
                    child_of_insertion_node = possible_insertion_node.children.pop()
                    split_idx = abs(remaining_until_insertion)
                    inner_parentEdge_len = child_of_insertion_node.parent.str_length + split_idx 
                    innernode = Node(inner_parentEdge_len, 'inner')
                    len_newnode = n - curr_suf + 1
                    new_node = Node(len_newnode, curr_suf)

                    possible_insertion_node.add_child(innernode)

                    innernode.add_child(child_of_insertion_node)
                    innernode.add_child(new_node)

                    id2node[curr_suf] = new_node
                root.update_leaf_list()


            else:
                innernode_len = curr_lcp
                innernode = Node(innernode_len, 'inner')

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
    if(len(inputstr) == maxLength):
        end = time.time()
        total = end-start
        if "T_even" in timers:
            timers["T_even"].append((maxLength, total))
        else:
            timers["T_even"] = [(maxLength, total)]
    return t_even


def overmerge(t_even, t_odd, S):
    if(len(S) == maxLength):
        start = time.time()
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
                    printif('case 1 added %s' % current.lca_odd)
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
                    printif('case 2 added %s' % current.lca_even)
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
                    t_overmerged.update_leaf_list()

                    o_child.old_parent = o_child.parent
                    current.add_child(o_child)

                    o += 1
                    # prepare the LCA nodepair thingy during the overmerge
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca'):
                        if o_child.is_leaf():
                            current.lca_odd = o_child
                        else:
                            current.lca_odd = o_child.leaflist[0]
                        printif('case 3 added %s' % current.lca_odd)
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
                        printif('case 4 added %s' % current.lca_even)
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca'):
                        if hasattr(e_child, 'lca_odd'):
                            current.lca_odd = e_child.lca_odd
            else:
                # Even and odd have same first char in parent edge
                e_parentEdge_len = e_child.str_length - current.str_length
                o_parentEdge_len = o_child.str_length - current.str_length

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

                    short_child_sub = Node(short_child.str_length, aId="sub_" + str(short_child.id))

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
                            printif('case 5 added %s to %s' % (inner_node.lca_even, current))
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca') and not overwrote:
                        if hasattr(inner_node, 'lca_odd'):
                            current.lca_odd = inner_node.lca_odd
                            printif('case 6 added %s to %s' % (inner_node.lca_odd, current))
                            if had_lca_even_too:
                                # we cached both lca_even and lca_odd from same
                                # child, mark this so one can be overwritten by
                                # whatever leafnode we may see next in another
                                # subtree
                                current.overwrite_lca = True
                                printif('overwrite added to %s with both %s and %s' % (current, inner_node.lca_odd, inner_node.lca_even))


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
                    if not e_child.children:
                        inner.id = e_child.id
                        inner.lca_even = e_child
                        printif('case 7 added %s to %s' % (e_child, inner))
                    if not o_child.children:
                        inner.id = o_child.id
                        inner.lca_odd = o_child
                        printif('case 8 added %s to %s' % (o_child, inner))

                    current.add_child(inner)
                    inner.even_subtree = e_child
                    inner.odd_subtree = o_child
                    merger_helper(inner, e_child, o_child)

                    t_overmerged.update_leaf_list()

                    had_lca_even_too = False
                    overwrote = False
                    if not hasattr(current, 'lca_even') or hasattr(current, 'overwrite_lca'):
                        if hasattr(inner, 'lca_even'):
                            current.lca_even = inner.lca_even
                            had_lca_even_too = True
                            if hasattr(current, 'overwrite_lca'):
                                overwrote = True
                            printif('case 9 added %s to %s' % (current.lca_even, current))
                    if not hasattr(current, 'lca_odd') or hasattr(current, 'overwrite_lca') and not overwrote:
                        if hasattr(inner, 'lca_odd'):
                            current.lca_odd = inner.lca_odd
                            printif('case 10 added %s to %s' % (current.lca_odd, current))
                            if had_lca_even_too:
                                current.overwrite_lca = True
                o += 1
                e += 1
    merger_helper(t_overmerged, t_even, t_odd)
    t_overmerged.update_leaf_list()
    if(len(S) == maxLength):
        end = time.time()
        total = end-start
        if "t_overmerged" in timers:
            timers["t_overmerged"].append((maxLength, total))
        else:
            timers["t_overmerged"] = [(maxLength, total)]
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

    lca_nodepairs = []
    def helper(node):
        nonlocal lca_nodepairs
        if hasattr(node, 'lca_even'):
            lca_nodepairs.append((node.lca_even, node.lca_odd))
    t_overmerged.traverse(helper)    
    
    id2node = []
    t_overmerged.traverse(lambda n: id2node.append((n.id, n))
                          if 'inner' not in str(n.id) else 'do nothing')
    id2node = dict(id2node)


    # ---------------------------------------
    # CREATE LCP TREE
    # ---------------------------------------
    lca_f = fast_lca.LCA()
    lca_f.preprocess(t_overmerged)
    for node1, node2 in lca_nodepairs:
        # TODO: using naive_lca to find lca to create suffix link, this
        #       must instead be the constant time lookup as described in
        #       the article [Ht84], otherwise we do not achieve O(n) running
        #       time for the algorithm


        lca = lca_f.query(id2node[node1.id], id2node[node2.id])
        #lca_naive = naive_lca(node1, node2, t_overmerged, id2node)

        #assert lca == lca_naive

        if (lca.id == 'root' or
                node1.id + 1 not in id2node or
                node2.id + 1 not in id2node):
            # we cannot create a suffix link from root as it is undefined
            continue
        node1_next = id2node[node1.id + 1]
        node2_next = id2node[node2.id + 1]

        lca_parent = lca_f.query(node1_next, node2_next)
        #lca_parent_naive = naive_lca(node1_next, node2_next, t_overmerged, id2node)
        
        #assert(lca_parent == lca_parent_naive)
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
     
        if(hasattr(curr_node, "lcp_depth")):

            if curr_node.str_length != curr_node.lcp_depth:
                # parentEdge_length = curr_node.lcp_depth - curr_node.parent.str_length
                # assert False

                curr_node.children = []

                curr_node.str_length = curr_node.lcp_depth

                curr_node.id = "inner"
                even_tree = curr_node.even_subtree
                odd_tree = curr_node.odd_subtree

                def helper(node):
                    for child in node.children:
                        child.parent = node
                even_tree.bfs(helper)
                odd_tree.bfs(helper)

                # if even_tree.is_leaf():
                #     even_leaf_id = even_tree.id
                # else:
                #     even_leaf_descendant = even_tree.leaflist[0]
                #     even_leaf_id = even_leaf_descendant.id

                even_leaf_id = curr_node.lca_even.id

                even_tree_parentEdge_char = S[even_leaf_id - 1 + curr_node.lcp_depth]


                # if odd_tree.is_leaf():
                #     odd_leaf_id = odd_tree.id
                # else:
                #     odd_leaf_descendant = odd_tree.leaflist[0]
                #     odd_leaf_id = odd_leaf_descendant.id

                odd_leaf_id = curr_node.lca_odd.id

                odd_tree_parentEdge_char = S[odd_leaf_id - 1 + curr_node.lcp_depth]
                
                if even_tree_parentEdge_char < odd_tree_parentEdge_char:
                    curr_node.add_child(even_tree)
                    curr_node.add_child(odd_tree)
                else:
                    curr_node.add_child(odd_tree)
                    curr_node.add_child(even_tree)
                return 'continue'
                
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
        if hasattr(node, 'INLABEL'):
            delattr(node, 'INLABEL')
        if hasattr(node, 'PREORDER'):
            delattr(node, 'PREORDER')
        if hasattr(node, 'bitList'):
            delattr(node, 'bitList')
    t_overmerged.traverse(helper)

def printif(s):
    global _printstuff
    if _printstuff:
        print(s)

def main():
    inputstr = str2int(input)
    inputstr_copy = inputstr[:]

    suffix_tree = construct_suffix_tree(inputstr, False)
    print('final tree for input %s:' % inputstr)
    print(suffix_tree.fancyprint(inputstr))

    check_correctness.check_correctness2(inputstr_copy)


if __name__ == '__main__':
    main()
