import farach
from utils import Node

def run_tests():
    inputstr = '1'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    expected_result.add_child(Node(aId=1, aParentEdge='12'))
    expected_result.add_child(Node(aId=2, aParentEdge='2'))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = '12'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    expected_result.add_child(Node(aId=1, aParentEdge='123'))
    expected_result.add_child(Node(aId=2, aParentEdge='23'))
    expected_result.add_child(Node(aId=3, aParentEdge='3'))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = '11'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    innernode = Node(aId='inner', aParentEdge='1')
    expected_result.add_child(innernode)
    innernode.add_child(Node(aId=1, aParentEdge='12'))
    innernode.add_child(Node(aId=2, aParentEdge='2'))
    expected_result.add_child(Node(aId=3, aParentEdge='2'))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = '111'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge='1')
    inner2 = Node(aId='inner', aParentEdge='1')
    leaf1 = Node(aId=1, aParentEdge='12')
    leaf2 = Node(aId=2, aParentEdge='2')
    leaf3 = Node(aId=3, aParentEdge='2')
    leaf4 = Node(aId=4, aParentEdge='2')
    expected_result.add_child(inner1)
    expected_result.add_child(leaf4)
    inner1.add_child(inner2)
    inner1.add_child(leaf3)
    inner2.add_child(leaf1)
    inner2.add_child(leaf2)
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    # inputstr = '122'
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge='12'))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = '1222'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge='2')
    inner2 = Node(aId='inner', aParentEdge='2')
    leaf1 = Node(aId=1, aParentEdge='12223')
    leaf2 = Node(aId=2, aParentEdge='23')
    leaf3 = Node(aId=3, aParentEdge='3')
    leaf4 = Node(aId=4, aParentEdge='3')
    leaf5 = Node(aId=5, aParentEdge='3')
    expected_result.add_child(leaf1)
    expected_result.add_child(inner1)
    expected_result.add_child(leaf5)
    inner1.add_child(inner2)
    inner1.add_child(leaf4)
    inner2.add_child(leaf2)
    inner2.add_child(leaf3)
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    # inputstr = '1221'
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge='12'))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    # inputstr = '2221'
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge='12'))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    print('tests succeeded!')

def current_test():
    inputstr = '1222'
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge='2')
    inner2 = Node(aId='inner', aParentEdge='2')
    leaf1 = Node(aId=1, aParentEdge='12223')
    leaf2 = Node(aId=2, aParentEdge='23')
    leaf3 = Node(aId=3, aParentEdge='3')
    leaf4 = Node(aId=4, aParentEdge='3')
    leaf5 = Node(aId=5, aParentEdge='3')
    expected_result.add_child(leaf1)
    expected_result.add_child(inner1)
    expected_result.add_child(leaf5)
    inner1.add_child(inner2)
    inner1.add_child(leaf4)
    inner2.add_child(leaf2)
    inner2.add_child(leaf3)
    # print('-'*80)
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

def main():
    # run_tests()
    current_test()
    

if __name__ == '__main__':
    main()