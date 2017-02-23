import t_even_tests
import simple_tree_tests
import overmerge_tests
import check_correctness
import tree_tests

def main():
    t_even_tests.run_tests()
    simple_tree_tests.run_tests()
    overmerge_tests.run_tests()
    tree_tests.run_tests()
    check_correctness.run_tests()
    print('completed all tests')

if __name__ == '__main__':
    main()
