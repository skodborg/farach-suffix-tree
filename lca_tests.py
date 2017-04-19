from utils import Node
import lca
import farach
import random
import string
import traceback
import time


def createExampleToReport():

    nodes = []
    rootNode = Node(aId="root")

    inner_2 = Node(aId="inner2")
    inner_8 = Node(aId="inner8")

    rootNode.add_child(inner_2)

    nodes.append(Node(aId=3))
    inner_2.add_child(nodes[0])

    inner_4 = Node(aId="inner4")

    inner_2.add_child(inner_4)

    nodes.append(Node(aId=5))
    nodes.append(Node(aId=6))
    nodes.append(Node(aId=7))


    inner_4.add_child(nodes[1])
    inner_4.add_child(nodes[2])
    inner_4.add_child(nodes[3])
    



    rootNode.add_child(inner_8)
    nodes.append(Node(aId=9))
    nodes.append(Node(aId=10))
    inner_8.add_child(nodes[4])
    inner_8.add_child(nodes[5])

    lca_al = lca.LCA()
    lca_al.preprocess(rootNode)

    print(rootNode.fancyprintLCA())


def createTreeOne():
    rootNode = Node(aStrLength=0, aId="root")
    n1_l = Node(aId="inner1",aStrLength=1,)
    n1_r = Node(aId="inner2", aStrLength=1)
    rootNode.add_child(n1_l)
    rootNode.add_child(n1_r)
    n2_1_l = Node(aId=1, aStrLength=2)
    n2_1_r = Node(aId=2, aStrLength=2)
    n1_l.add_child(n2_1_l)
    n1_l.add_child(n2_1_r)
    n2_2_l = Node(aId=3, aStrLength=2)
    n2_2_r = Node(aId=4, aStrLength=2)
    n1_r.add_child(n2_2_l)
    n1_r.add_child(n2_2_r)
    return rootNode, [n2_1_l, n2_1_r, n2_2_l, n2_2_r, n1_l, n1_r]

def createTreeTwo():
    rootNode = Node(aStrLength=0, aId="root")
    inner1 = Node(aId="inner1")
    inner2 = Node(aId="inner2")
    rootNode.add_child(inner1)
    rootNode.add_child(inner2)
    nodes = []
    nodes.append(Node(aId=1))
    nodes.append(Node(aId=2))
    nodes.append(Node(aId=3))
    nodes.append(Node(aId=4))
    nodes.append(Node(aId=5))
    nodes.append(Node(aId=6))
    inner1.add_child(nodes[0])
    inner1.add_child(nodes[1])
    nodes.append(inner1)
    nodes.append(inner2)
    inner2_1 = Node(aId="inner2_1")
    inner2.add_child(nodes[2])
    inner2.add_child(nodes[3])
    inner2.add_child(inner2_1)
    nodes.append(inner2_1)
    inner2_1.add_child(nodes[4])
    inner2_1.add_child(nodes[5])

    return rootNode, nodes

def test_tree_one():
    tree, nodes = createTreeOne()


    lca_al = lca.LCA()
    lca_al.preprocess(tree)
    assert lca_al.query(nodes[0], nodes[1]).id == "inner1"
    assert lca_al.query(nodes[2], nodes[3]).id == "inner2"
    assert lca_al.query(nodes[0], nodes[3]).id == "root"
    assert lca_al.query(nodes[3], nodes[0]).id == "root"
    assert lca_al.query(nodes[4], nodes[5]).id == "root"



def test_tree_two():
    tree, nodes = createTreeTwo()
    lca_al = lca.LCA()
    lca_al.preprocess(tree)
    assert lca_al.query(nodes[7], nodes[8]).PREORDER == 5
    assert lca_al.query(nodes[0], nodes[1]).PREORDER == 2
    assert lca_al.query(nodes[1], nodes[3]).PREORDER == 1
    assert lca_al.query(nodes[1], nodes[4]).PREORDER == 1
    assert lca_al.query(nodes[1], nodes[5]).PREORDER == 1
    assert lca_al.query(nodes[0], nodes[5]).PREORDER == 1
    assert lca_al.query(nodes[4], nodes[5]).PREORDER == 8



def test_tree_three():
    string = '12121'
    string = farach.str2int(string)
    constructed_tree = farach.construct_suffix_tree(string)
    constructed_tree.update_leaf_list
    leaflist = constructed_tree.leaflist
    lca_al = lca.LCA()
    lca_al.preprocess(constructed_tree)
    
    assert str(lca_al.query(leaflist[0], leaflist[1]).leaflist) == "[node1, node3]"
    assert str(lca_al.query(leaflist[2], leaflist[3]).leaflist) == "[node1, node3, node5, node2, node4, node6]"
    assert str(lca_al.query(leaflist[0], leaflist[2]).leaflist) == "[node1, node3, node5]"
    assert str(lca_al.query(leaflist[3], leaflist[4]).leaflist) == "[node2, node4]"
    assert str(lca_al.query(leaflist[0], leaflist[5]).leaflist) == "[node1, node3, node5, node2, node4, node6]"

def test_tree_four():
    string = 'mississippi'
    string = farach.str2int(string)
    constructed_tree = farach.construct_suffix_tree(string)
    constructed_tree.update_leaf_list
    leaflist = constructed_tree.leaflist

 
    lca_al = lca.LCA()
    lca_al.preprocess(constructed_tree)

    assert str(lca_al.query(leaflist[1], leaflist[2]).leaflist) == "[node2, node5]"
    assert str(lca_al.query(leaflist[0], leaflist[2]).leaflist) == "[node1, node2, node5, node8, node11, node4, node7, node3, node6, node10, node9, node12]"
    assert str(lca_al.query(leaflist[6], leaflist[8]).leaflist) == "[node4, node7, node3, node6]"
    assert str(lca_al.query(leaflist[9], leaflist[10]).leaflist) == "[node10, node9]"




def check_correctness(string):

    string = farach.str2int(string)
    constructed_tree = farach.construct_suffix_tree(string)
    
    id2node = []
    constructed_tree.traverse(lambda n: id2node.append((n.id, n))
                          if 'inner' not in str(n.id) else 'do nothing')


    id2node = dict(id2node)
    constructed_tree.update_leaf_list
    leaflist = constructed_tree.leaflist
    lca_al = lca.LCA()
    lca_al.preprocess(constructed_tree)

    for i in leaflist:
        for j in leaflist:
            assert farach.naive_lca(i,j, constructed_tree, id2node) == lca_al.query(i,j)

def preprocess_and_one_query(tree, leaflist):
    lca.preprocess(tree)
    #lca.query(leaflist[0],leaflist[len(leaflist)-1])

def check_speed():

    for i in range(100, 500):
        S = ''.join(random.choice(string.digits) for _ in range(i*50))


        S = farach.str2int(S)
        constructed_tree = farach.construct_suffix_tree(S)
        
        id2node = []
        constructed_tree.traverse(lambda n: id2node.append((n.id, n))
                              if 'inner' not in str(n.id) else 'do nothing')

        id2node = dict(id2node)
        constructed_tree.update_leaf_list
        leaflist = constructed_tree.leaflist

        start = time.time()
        preprocess_and_one_query(constructed_tree, leaflist)
        end = time.time()
        print('%i,%f' % ((i*50),(end - start)))

def run_tests():
    # test_tree_two()
    # test_tree_one()
    # test_tree_three()
    # test_tree_four()
    # check_correctness("mississippi")
    # check_correctness("121112212221")
    # check_correctness("111222122121")
    # check_correctness("12121212121")
    # check_correctness("banana")
    # check_correctness("mississippiisaniceplaceithink")
    # check_correctness("12121")
    print("lca_tests success")




def automaticTests():
    while True:
        try:
            # outputfilename = 'outputtree.txt'
            S = ''.join(random.choice(string.digits) for _ in range(400))
            start = time.time()
            correct_tree = check_correctness(S)
            end = time.time()
            print('worked')
            print('took %f' % (end - start))
            # outputfile = open(outputfilename, 'w')
            # outputfile.write(correct_tree.fancyprint(S, onlylengths=True))
            # outputfile.close()
            # print('stored in %s' % outputfilename)
        except AssertionError:
            print('attempting string: %s' % S)
            print('assertion error!')
            traceback.print_exc()
        except TypeError:
            print('attempting string: %s' % S)
            print('type error!')
            traceback.print_exc()
        except:
            print('attempting string: %s' % S)
            print('some error!')
            traceback.print_exc()



def main():
    createExampleToReport()
    #run_tests()
    #automaticTests()
    #check_speed()

if __name__ == '__main__':
    main()