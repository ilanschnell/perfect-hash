import sys
from string import ascii_uppercase
from random import choices, randint

def key():
    return ''.join(choices(ascii_uppercase, k=randint(1, 8)))

N = int(sys.argv[1])

result = set()
while len(result) < N:
    result.add(key())

for k in result:
    print(k)
