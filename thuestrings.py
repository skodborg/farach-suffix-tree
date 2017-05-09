def generate_2_3(n):
    ''' ??? '''
    morphisms = {}
    morphisms['a'] = 'ab'
    morphisms['b'] = 'ba'

    t_i = 'a'
    for i in range(n):
        t_j = []
        for char in t_i:
            t_j.append(morphisms[char])
        t_i = ''.join(t_j)
        print(i, len(t_i))
    return t_i



def generate_3_2(n):
    ''' thue string (3,2), generates strings over an alphabet of size 3
        with no repetitions, i.e. no character is followed by an identical
        character immediately '''
    morphisms = {}
    morphisms['a'] = 'abcab'
    morphisms['b'] = 'acabcb'
    morphisms['c'] = 'acbcacb'

    t_i = 'a'
    for i in range(n):
        t_j = []
        for char in t_i:
            t_j.append(morphisms[char])
        t_i = ''.join(t_j)
        print(i, len(t_i))
    return t_i


def main():
    print('type in a number of iterations:')
    n = input()
    try:
        n = int(n)
    except:
        print('error: not an int')
        return
    print(generate_2_3(n))
    print(generate_3_2(n))


if __name__ == '__main__':
    main()
