# ./mk_rnd_keys.py 10000 | sort | uniq | shuf >keywords.txt

import sys
from random import choice, randint
from string import digits, ascii_uppercase, ascii_lowercase

def key():
    return ''.join(choice(ascii_uppercase + ascii_lowercase + digits)
                   for i in range(randint(6, 20)))

N = int(sys.argv[1])


for n in range(N):
    print(key())
