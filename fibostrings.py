def generate(n):
    if n < 0:
        return ''
    if n == 0:
        return 'b'
    if n == 1:
        return 'a'

    prevprev = 'b'
    prev = 'a'
    curr = 'ab'
    for _ in range(n - 2):
        prevprev = prev
        prev = curr
        curr = prev + prevprev
    return curr


def main():
    print('type in a number of iterations:')
    n = input()
    try:
        n = int(n)
    except:
        print('error: not an int')
        return
    print(generate(n))


if __name__ == '__main__':
    main()
