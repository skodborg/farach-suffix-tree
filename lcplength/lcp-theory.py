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


def read_fasta(fname):
    with open(fname, 'r') as f:
        # skip first line, a description
        f.readline()
        content = f.read().replace('\n', '')
    return content


def avg_suff_lcp_length(fname):
    string = read_fasta(fname)
    m = len(string)

    sum_lcp_length = 0
    no_of_summands = m * (m - 1) / 2

    # determine sum of length of all LCPs of the strings
    for i in range(m):
        # if i % 1000 == 0:
        print(i)
        for j in range(m):
            if j <= i:
                # only calculate each unique pair once
                continue
            sum_lcp_length += lcp(string[i:], string[j:])

    avg_lcp = sum_lcp_length / no_of_summands

    print('length: %i \t avg suffix lcp length: %i \t percentage of length: %f' % (m, avg_lcp, avg_lcp / m * 100))


def character_frequency(fname):
    string = read_fasta(fname)
    m = len(string)

    seen_chars = {}

    for i in range(m):
        if i % 1000 == 0:
            print(i)
        if string[i] in seen_chars:
            seen_chars[string[i]] += 1
        else:
            seen_chars[string[i]] = 1

    return seen_chars


def alphabet_dependence(A, n=100, m=100, points=10000, use_suffixes=False):
    ''' Constructs m strings of length n, drawn from an alphabet of size A,
        and determines the average LCP length, average repeated over i times'''
    median_lcp_length_per_a = []

    prefix = 'suff_' if use_suffixes else 'rnd_'

    for a in A:
        data = []

        for _ in range(points):
            strings = []
            
            if use_suffixes:
                # generate a random str of length n, list all its m suffixes
                S = random.choices(range(a), k=n)
                for i in range(len(S)):
                    strings.append(S[i:])
            else:
                # generate m random strings of length n, look at their LCPs
                for _ in range(m):
                    strings.append(random.choices(range(a), k=n))

            sum_lcp_length = 0
            no_of_summands = m * (m - 1) / 2

            # determine sum of length of all LCPs of the strings
            for i in range(m):
                for j in range(m):
                    if j <= i:
                        # only calculate each unique pair once
                        continue
                    sum_lcp_length += lcp(strings[i], strings[j])

            avg_lcp = sum_lcp_length / no_of_summands

            # generates 1 of i points to plot
            data.append(sum_lcp_length)
            print('n=%i, m=%i, points=%i \t %f' % (n, m, points, sum_lcp_length))\
        
        # save data to file
        f = open('%sdata_alph-size-%i.txt' % (prefix, a), 'w')
        for e in data:
            f.write('%f\n' % e)
        f.close()

        # plot data
        fig = plt.figure(figsize=(9, 6))
        plt.hist(data, 50)
        plt.xlabel('sum of lcp lengths')
        plt.ylabel('probability')
        plt.grid(True)

        median = statistics.median(data)
        # save medians to file
        f = open('%smediandata.txt' % prefix, 'a')
        f.write('%i, %s\n' % (a, repr(median)))
        f.close()
        
        # plot middle value
        median_lcp_length_per_a.append((a, median))
        plt.axvline(x=median, linewidth=2, color='k')
        fig.savefig('%sdataalph-size-%i.png' % (prefix, a), bbox_inches='tight')

    # plot lcp length median as a function of alphabet size
    fig = plt.figure(figsize=(9, 6))
    x, y = zip(*median_lcp_length_per_a)
    plt.scatter(x, y)
    plt.xlabel('alphabet size')
    plt.ylabel('median sum of lcp lengths')
    # plt.yscale('log')
    plt.grid(True)

    fig.savefig('%sdata-median-lcp-lengths.png' % prefix, bbox_inches='tight')


def main():
    avg_suff_lcp_length('BRCA1_chromosome-17-excerpt.fasta')


if __name__ == '__main__':
    main()
