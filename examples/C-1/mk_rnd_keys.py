import sys
from string import ascii_uppercase
from random import choice, randint

def key():
    return ''.join(choice(ascii_uppercase) for i in range(randint(1, 8)))

N = int(sys.argv[1])

result = set()
while len(result) < N:
    result.add(key())

for k in result:
    print(k)
