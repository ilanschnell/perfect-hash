import sys
from random import choice, randint
from string import ascii_letters, digits

def key():
    return ''.join(choice(ascii_letters + digits)
                   for i in range(randint(6, 10)))

N = int(sys.argv[1])

for n in range(N):
    print(key())
