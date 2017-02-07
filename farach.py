import math
import radixsort
import utils

unique_char = '$'
A = {0: 1, 1: 2}
#input = '121112212221'
input = '111222122121'

# TODO: test that it works for inputs of odd length
# input = '1211122122211'

# assumes integer alphabets; works, as we can translate every alphabet
# to an integer one; we suppose that the last integer in the alphabet 
# is contained in O(n)? page 127 in book

def construct_suffix_tree(inputstr):
    inputstr += unique_char
    print(inputstr)

    t_odd = T_odd(inputstr)
    # t_even = T_even(t_odd)
    # t_overmerged = overmerge(t_even, t_odd)
    # suffix_tree = cleanup_overmerge(t_overmerged)
    # return suffix_tree


def T_odd(inputstr):
    S = inputstr
    n = len(S)

    def toInt(char):
        if char == '$':
            return len(A) + 1
        else:
            return int(char)

    # strings are 0-indexed in python, and 1-indexed in the book's examples
    # so we -2 and -1 from pos 'i' to let our match the book's examples
    chr_pairs = [(toInt(S[2*i-2]), toInt(S[2*i-1])) for i in range(1, math.floor(n / 2) + 1)]
    #assert chr_pairs == [(1, 2), (1, 1), (1, 2), (2, 1), (2, 2), (2, 1)]

    # sort in O(k * n) using radix sort (k = 2 here, guaranteed)
    radixsort.sort(chr_pairs)
    #assert chr_pairs == [(1, 1), (1, 2), (1, 2), (2, 1), (2, 1), (2, 2)]
    
    # remove duplicates, O(n)
    unique_chr_pairs = [chr_pairs[0]]
    for pair in chr_pairs[1:]:
        if unique_chr_pairs[-1] != pair:
            unique_chr_pairs.append(pair)
    chr_pairs = unique_chr_pairs
    #assert chr_pairs == [(1, 1), (1, 2), (2, 1), (2, 2)]
    
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
        pair = (toInt(S[2*i-2]), toInt(S[2*i-1]))
        Sm += str(pair2single[pair])
    Sm += unique_char
    #assert Sm == '212343$'

    # TODO: recursively call construct_suffix_tree(Sm) to create suffix tree for Sm
    tree_Sm = faked_tree() #construct_suffix_tree(Sm)

    def rank_to_char(node):
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

    rank_to_char(tree_Sm)



    def resolve_suffix_tree(node):


        # Takes every child in merge list, adds a new node with these children as children to the new node
        def merge():
            node = utils.Node(current_char)
            node.children = current_merg
            for n in node.children:
                # Removes first char, that char is already accounted for on parent node
                n.parentEdge = n.parentEdge[1:]
            children_list.append(node)

        current_char = ''
        current_merg = []
        children_list = []

        # If node is a leaf node, update node id to represent the actually length of string after de-ranking
        if(node.is_leaf()):
            node.id = node.id*2-1
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

    resolve_suffix_tree(tree_Sm)
    print(tree_Sm.fancyprint())


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


def T_even(t_odd):
    print('Not implemented yet')


def overmerge(t_even, t_odd):
    print('Not implemented yet')


def cleanup_overmerge(t_overmerged):
    print('Not implemented yet')


def main():
    construct_suffix_tree(input)
    

if __name__ == '__main__':
    main()
