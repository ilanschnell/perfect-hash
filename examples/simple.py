import sys
import random

sys.path.append('..')
from perfect_hash import generate_hash, anum_chars


def mkRandHash(N):
    """
    Return a random hash function which returns hash values from 0 .. N-1
    """
    junk = "".join(random.choices(anum_chars, k=10))
    return lambda key: hash(junk + key) % N


def mkPerfHash(keys, Hash):
    """
    Given a list of keys and a hash function generator, return a perfect
    hash function for the keys, i.e. each key is mapped to it's index in
    the list.
    """
    f1, f2, G = generate_hash(keys, Hash)
    return lambda k: (G[f1(k)] + G[f2(k)]) % len(G)


months = "jan feb mar apr may jun jul aug sep oct mov dec".split()

f = mkPerfHash(months, mkRandHash)
for i, month in enumerate(months):
    assert f(month) == i

print("OK")
