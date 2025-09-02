# python mk_rnd_keys.py 10000 | sort | uniq | shuf >keywords.txt

import sys
from random import choices, randint
from string import ascii_letters, digits

def key():
    return ''.join(choices(ascii_letters + digits, k=randint(6, 20)))

N = int(sys.argv[1])

for n in range(N):
    print(key())
