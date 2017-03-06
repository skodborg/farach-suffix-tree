import farach
from check_correctness import check_correctness2
from utils import Node


def run_tests():
    str12121()
    print('tests succeeded!')


def str12121():
    string = '12121'
    string = farach.str2int(string)
    constructed_tree = farach.construct_suffix_tree(string)

    actual_tree = Node(aId='root')
    inner1 = Node(1, 'inner')
    inner2 = Node(2, 'inner')
    inner3 = Node(3, 'inner')
    leaf1 = Node(6, 1)
    leaf2 = Node(5, 2)
    leaf3 = Node(4, 3)
    leaf4 = Node(3, 4)
    leaf5 = Node(2, 5)
    leaf6 = Node(1, 6)
    actual_tree.add_child(inner1)
    actual_tree.add_child(inner2)
    actual_tree.add_child(leaf6)
    inner1.add_child(inner3)
    inner1.add_child(leaf5)
    inner3.add_child(leaf1)
    inner3.add_child(leaf3)
    inner2.add_child(leaf2)
    inner2.add_child(leaf4)

    actual_tree.update_leaf_list()

    print(actual_tree.fancyprint(string))
    print(constructed_tree.fancyprint(string))

    check_correctness2('12121')

    assert constructed_tree.fancyprint(string) == actual_tree.fancyprint(string)

    # check_correctness2(string[:-1])


if __name__ == '__main__':
    run_tests()
