import sys
import string
from random import choice, randint

def key():
    return ''.join(choice(string.ascii_uppercase)
                   for i in range(randint(1, 3)))

N = int(sys.argv[1])

result = set()
while len(result) < N:
    result.add(key())

for k in result:
    print(k)
