from __future__ import print_function
import sys
import string
from random import choice, randint


from perfect_hash import generate_hash


def flush_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


def random_key():
    return ''.join(choice(string.printable) for i in range(randint(1, 4)))


def main():
    for N in range(1, 100):
        print(N)
        for _ in range(100):
            keys = set()
            while len(keys) < N:
                keys.add(random_key())
            keys = list(keys)
            generate_hash(keys)


if __name__ == '__main__':
    main()
