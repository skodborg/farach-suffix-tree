import farach
from utils import Node


def check_correctness(inputstr):

    inputstr = farach.str2int(inputstr)

    suffix_tree = farach.construct_suffix_tree(inputstr)

    add_str_length(suffix_tree, 0)
    farach.compute_lcp_tree(suffix_tree)
    make_inners_unique(suffix_tree)

    suffix_tree.traverse(check_suffix_link_length)
    print("check_suffix_link_length success")

    check_string_length(suffix_tree)
    print("check_string_length success")

    suffix_tree.traverse(check_descendants(inputstr))
    print("check_descendants success")

    suffix_tree.traverse(children_different_first_char)
    print("children_different_first_char success")
 
def children_different_first_char(node):
    # For each internal node x with children c1...ck 
    # then each of substr xci begins with a different char
    current_chars = set()    
    for n in node.children:
        assert n.parentEdge[0] not in current_chars
        current_chars.add(n.parentEdge[0])

def make_inners_unique(node):
    curr = 0

    def helper(n):
        nonlocal curr
        if n.id == "inner":
            n.id += str(curr)
            curr += 1
    node.bfs(helper)

def check_descendants(inputstr):
    # if y is a child of x, then sl(y) is a descendant of sl(x)
    def check_descendants_helper(node):
        if hasattr(node, "suffix_link"):
            for n in node.children:
                if hasattr(n, "suffix_link"):
                    assert node_is_descendant(node.suffix_link, n.suffix_link)


    return check_descendants_helper;



def node_is_descendant(node1, node2):
        descendants = []
        node1.traverse(lambda n: descendants.append(n))
        is_descendant = True in [n.id == node2.id for n in descendants]
        return is_descendant


def check_suffix_link_length(node):
    # For each node x,
    # |sl(x)| = |x| - 1

    if hasattr(node, "suffix_link"):
        assert node.str_length - 1 == node.suffix_link.str_length

def check_string_length(node):
    # If r is the root, then |r| = 0
    # If y is a child of x, then |y| > |x|

    if(node.id == "root"):
        assert node.str_length == 0

    else:
        for child in node.children:
            assert node.str_length < child.str_length
            check_string_length(child)



def add_str_length(node, prev_length):
        # TODO: consider do this as we form the overmerge tree
        node.str_length = prev_length + len(node.parentEdge)
        for n in node.children:
            add_str_length(n, node.str_length)


def main():
    check_correctness("mississippi")

if __name__ == '__main__':
    main()