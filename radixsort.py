# source: http://www.geekviewpoint.com/python/sorting/radixsort
def sort(aTupleList, tup_idx=None):
    def sort_helper(aTupleList, tup_idx):
        RADIX = 10
        maxLength = False
        tmp, placement = -1, 1

        while not maxLength:
            maxLength = True
            # declare and initialize buckets
            buckets = [list() for _ in range(RADIX)]

            # split aTupleList between lists
            for tup in aTupleList:
                # if tup[1] == '$':

                tmp = int(tup[tup_idx] / placement)
                buckets[tmp % RADIX].append(tup)
                if maxLength and tmp > 0:
                    maxLength = False
            # print(buckets)
            # empty lists into aTupleList array
            a = 0
            for b in range(RADIX):
                buck = buckets[b]
                for i in buck:
                    aTupleList[a] = i
                    a += 1
            # move to next digit
            placement *= RADIX

    if tup_idx != None:
        sort_helper(aTupleList, tup_idx)
    else:
        sort_helper(aTupleList, 1)
        sort_helper(aTupleList, 0)


def test_sort():
    testlist = [(2, 11), (1, 11)]
    sort(testlist)
    assert testlist == [(1, 11), (2, 11)]

    testlist = [(2, 22), (2, 11)]
    sort(testlist)
    assert testlist == [(2, 11), (2, 22)]

    testlist = [(1, 22), (2, 11)]
    sort(testlist)
    assert testlist == [(1, 22), (2, 11)]

    testlist = [(2, 22), (1, 33), (2, 11)]
    sort(testlist)
    assert testlist == [(1, 33), (2, 11), (2, 22)]

    testlist = [(2, 22), (1, 33), (2, 11)]
    sort(testlist, 1)
    assert testlist == [(2, 11), (2, 22), (1, 33)]

    testlist = [(2, 22), (1, 33), (2, 11)]
    sort(testlist, 0)
    assert testlist == [(1, 33), (2, 22), (2, 11)]

    print('Unit tests succeeded!')


def main():
    test_sort()


if __name__ == '__main__':
    main()
