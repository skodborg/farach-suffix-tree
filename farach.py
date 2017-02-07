import math
import radixsort

unique_char = '$'
A = {0: 1, 1: 2}
input = '121112212221'

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
    assert chr_pairs == [(1, 2), (1, 1), (1, 2), (2, 1), (2, 2), (2, 1)]

    # sort in O(k * n) using radix sort (k = 2 here, guaranteed)
    radixsort.sort(chr_pairs)
    assert chr_pairs == [(1, 1), (1, 2), (1, 2), (2, 1), (2, 1), (2, 2)]
    
    # remove duplicates, O(n)
    unique_chr_pairs = [chr_pairs[0]]
    for pair in chr_pairs[1:]:
        if unique_chr_pairs[-1] != pair:
            unique_chr_pairs.append(pair)
    chr_pairs = unique_chr_pairs
    assert chr_pairs == [(1, 1), (1, 2), (2, 1), (2, 2)]
    
    # compute S'[i] = rank of (S[2i - 1], S[2i])
    Sm = ''
    count = 1
    pair2single = {}  # lookup is O(1) for pairs to single character mapping
    for pair in chr_pairs:
        pair2single[pair] = count
        count += 1
    for i in range(1, math.floor(n / 2) + 1):
        pair = (toInt(S[2*i-2]), toInt(S[2*i-1]))
        Sm += str(pair2single[pair])
    Sm += unique_char
    assert Sm == '212343$'

    # TODO: recursively call construct_suffix_tree(Sm) to create suffix tree for Sm
    Tree_Sm = construct_suffix_tree(Sm)

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
