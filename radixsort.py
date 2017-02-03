# source: http://www.geekviewpoint.com/python/sorting/radixsort

def sort(aTupleList):
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
            # print(tup)
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
  sort_helper(aTupleList, 1)
  sort_helper(aTupleList, 0)


def test_sort():
    l = [(2, 11), (1, 11)]
    sort(l)
    assert l == [(1, 11), (2, 11)]

    l = [(2, 22), (2, 11)]
    sort(l)
    assert l == [(2, 11), (2, 22)]

    l = [(1, 22), (2, 11)]
    sort(l)
    assert l == [(1, 22), (2, 11)]

    l = [(2, 22), (1, 33), (2, 11)]
    sort(l)
    assert l == [(1, 33), (2, 11), (2, 22)]

    print('Unit tests succeeded!')

def main():
    test_sort()


if __name__ == '__main__':
    main()
