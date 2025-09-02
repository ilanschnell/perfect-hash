import sys
import random

sys.path.append('..')
import perfect_hash


class XORHash(object):
    """
    Random hash function generator.
    """
    def __init__(self, N):
        self.N = N
        self.salt = bytearray()

    def __call__(self, key):
        key = key.encode()
        while len(self.salt) < len(key):  # add more salt as necessary
            self.salt.append(random.choice(perfect_hash.anum_chars.encode()))

        return sum(self.salt[i] ^ c for i, c in enumerate(key)) % self.N

    template = """
def hash_f(key, salt):
    return sum(key[i] ^ salt[i] for i in range(len(key))) % $NG

def perfect_hash(key):
    key = key.encode()
    if len(key) > $NS:
        return -1
    return (G[hash_f(key, b"$S1")] +
            G[hash_f(key, b"$S2")]) % $NG
"""

keys = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()

perfect_hash.verbose = True
perfect_hash.trials = 100
code = perfect_hash.generate_code(keys, XORHash, pow2=1)
print(code)
perfect_hash.run_code(code)
