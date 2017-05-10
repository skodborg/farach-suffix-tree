import math
import statistics
import random
import matplotlib.pyplot as plt


def lcp(str1, str2):
    len_of_shorter = min(len(str1), len(str2))
    len_lcp = 0
    for i in range(len_of_shorter):
        if str1[i] != str2[i]:
            break
        len_lcp += 1
    return len_lcp


def alphabet_dependence(A, n=10000, m=100, points=10):
    ''' Constructs m strings of length n, drawn from an alphabet of size A,
        and determines the average LCP length, average repeated over i times'''
    median_lcp_length_per_a = []

    for a in A:
        data = []

        for _ in range(points):
            strings = []
            for _ in range(m):
                strings.append(random.choices(range(a), k=n))

            sum_lcp_length = 0
            no_of_summands = m * (m - 1) / 2

            # LOOP
            for i in range(m):
                for j in range(m):
                    if j <= i:
                        # only calculate each unique pair once
                        continue
                    sum_lcp_length += lcp(strings[i], strings[j])

            avg_lcp = sum_lcp_length / no_of_summands

            # generates 1 of i points to plot
            data.append(avg_lcp)
            print('n=%i, m=%i, points=%i \t %f' % (n, m, points, avg_lcp))\

        # save data to file
        f = open('data_alph-size-%i.txt' % a, 'w')
        for e in data:
            f.write('%f\n' % e)
        f.close()

        # plot data
        fig = plt.figure(a, figsize=(9, 6))
        plt.hist(data, 50)
        plt.xlabel('avg. lcp length')
        plt.ylabel('probability')
        plt.grid(True)

        # plot middle value

        median = statistics.median(data)
        median_lcp_length_per_a.append((a, median))
        plt.axvline(x=median, linewidth=2, color='k')

        # plt.show()
        fig.savefig('alph-size-%i.png' % a, bbox_inches='tight')

    # save medians to file
    f = open('mediandata.txt', 'w')
    for tup in median_lcp_length_per_a:
        f.write('%i, %s\n' % (tup[0], repr(tup[1])))
    f.close()

    # plot lcp length median as a function of alphabet size
    fig = plt.figure(0, figsize=(9, 6))
    x, y = zip(*median_lcp_length_per_a)
    plt.scatter(x, y)
    plt.xlabel('alphabet size')
    plt.ylabel('median lcp length')
    # plt.yscale('log')
    plt.grid(True)

    # adjusted = [(x, y/math.log(y, x)) for x, y in median_lcp_length_per_a]
    print(median_lcp_length_per_a)
    # print(adjusted)
    # plt.scatter(*zip(*adjusted))

    # plt.show()
    fig.savefig('median-lcp-lengths.png', bbox_inches='tight')

    # TEORI: den gennemsnitlige længde af lcp for strenge over et alfabet af
    #        str. |A| er log |A|

    # find fine værdier for m, n og i, og varier dernæst A

    # 2 grafer:
    #   en hvor n, m, i og A holdes fast, og avg. lcp plottes 
            # (forventes en normalfordeling - histogram med intervaller)
            # validerer, at avg. lcp kan bruges som forventelig værdi
    #   en hvor |A| varieres, og avg. lcp plottes som funktion heraf
            # en hvor denne forventelige værdi har en udvikling - helst log |A|

    # should vary alphabet size, run for growing n
    # and verify that the median of the average lcp lengths is normally distributed
    # around log_{|A|} n ????

    # varier |A|, og for hver |A| varieres n for at finde den forventede værdi,
    # som er O(n log_{|A|} n)


def main():
    alphabet_dependence(list(range(2, 51, 1)))


if __name__ == '__main__':
    main()
