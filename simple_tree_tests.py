import farach
from utils import Node

def run_tests():
    inputstr = farach.str2int('1')

    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    expected_result.add_child(Node(aId=1, aParentEdge=[1,2]))
    expected_result.add_child(Node(aId=2, aParentEdge=[2]))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()
    print('hooray')

    inputstr = farach.str2int('12')
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    expected_result.add_child(Node(aId=1, aParentEdge=[1,2,3]))
    expected_result.add_child(Node(aId=2, aParentEdge=[2,3]))
    expected_result.add_child(Node(aId=3, aParentEdge=[3]))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = farach.str2int('11')
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    innernode = Node(aId='inner', aParentEdge=[1])
    expected_result.add_child(innernode)
    innernode.add_child(Node(aId=1, aParentEdge=[1,2]))
    innernode.add_child(Node(aId=2, aParentEdge=[2]))
    expected_result.add_child(Node(aId=3, aParentEdge=[2]))
    # print('inputstr: %s' % inputstr)
    # print('expected:')
    # print(expected_result.fancyprint())
    # print('actual:')
    # print(constructed_tree.fancyprint())
    assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = farach.str2int('111')
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge=[1])
    inner2 = Node(aId='inner', aParentEdge=[1])
    leaf1 = Node(aId=1, aParentEdge=[1,2])
    leaf2 = Node(aId=2, aParentEdge=[2])
    leaf3 = Node(aId=3, aParentEdge=[2])
    leaf4 = Node(aId=4, aParentEdge=[2])
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

    # inputstr = farach.str2int('122')
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge=[12]))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    inputstr = farach.str2int('1222')
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge=[2])
    inner2 = Node(aId='inner', aParentEdge=[2])
    leaf1 = Node(aId=1, aParentEdge=[1,2,2,2,3])
    leaf2 = Node(aId=2, aParentEdge=[2,3])
    leaf3 = Node(aId=3, aParentEdge=[3])
    leaf4 = Node(aId=4, aParentEdge=[3])
    leaf5 = Node(aId=5, aParentEdge=[3])
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

    # inputstr = farach.str2int('1221')
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge=[12]))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    # inputstr = farach.str2int('2221')
    # constructed_tree = farach.construct_suffix_tree(inputstr)
    # expected_result = Node(aId='root')
    # expected_result.add_child(Node(aId=1, aParentEdge=[12]))
    # assert constructed_tree.fancyprint() == expected_result.fancyprint()

    banana_test()

    print('tests succeeded!')

def current_test():
    inputstr = farach.str2int('1222')
    constructed_tree = farach.construct_suffix_tree(inputstr)
    expected_result = Node(aId='root')
    inner1 = Node(aId='inner', aParentEdge=[2])
    inner2 = Node(aId='inner', aParentEdge=[2])
    leaf1 = Node(aId=1, aParentEdge=[1,2,2,2,3])
    leaf2 = Node(aId=2, aParentEdge=[2,3])
    leaf3 = Node(aId=3, aParentEdge=[3])
    leaf4 = Node(aId=4, aParentEdge=[3])
    leaf5 = Node(aId=5, aParentEdge=[3])
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

def banana_test():
    # banana
    # 123232
    inputstr = farach.str2int('123232')

    root = Node(aId="root")
    root.add_child(Node([1,2,3,2,3,2,4],"1"))

    inner = Node([2], "inner")
    root.add_child(inner)

    inner2 = Node([3,2], "inner")
    inner2.add_child(Node([3,2,4], 2))
    inner2.add_child(Node([4], 4))

    inner.add_child(inner2)

    inner.add_child(Node([4],6))

    inner = Node([3,2], "inner")

    inner.add_child(Node([3,2,4], 3))
    inner.add_child(Node([4], 5))

    root.add_child(inner)

    root.add_child(Node([4], 7))


    constructed_tree = farach.construct_suffix_tree(inputstr)


    assert constructed_tree.fancyprint() == root.fancyprint() 



def main():
    run_tests()
    

if __name__ == '__main__':
    main()
