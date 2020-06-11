import sys
import random
import string

sys.path.append('..')
from perfect_hash import generate_hash


months = 'jan feb mar apr may jun jul aug sep oct mov dec'.split()


def mkRandHash(N):
    """
    Return a random hash function which returns hash values from 0..N-1
    """
    junk = "".join(random.choice(string.ascii_letters + string.digits)
                   for unused in range(10))
    return lambda key: hash(junk + str(key)) % N


def mkPerfHash(keys, Hash):
    f1, f2, G = generate_hash(months, Hash)
    return lambda k: (G[f1(k)] + G[f2(k)]) % len(G)


f = mkPerfHash(months, mkRandHash)
for h, k in enumerate(months):
    assert h == f(k)
print("OK")
