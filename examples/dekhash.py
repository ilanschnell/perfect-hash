import sys
import random

sys.path.append('..')
from perfect_hash import generate_code, run_code


class DEKHash(object):
    """
    Random hash function generator.
    """
    def __init__(self, N):
        self.N = N
        self.salt = random.getrandbits(31)

    def DEKhash(self, x, key):
        for c in key:
            x = ((x << 5) ^ (x >> 27) ^ ord(c)) % (1 << 31)
        return x

    def __call__(self, key):
        return self.DEKhash(self.salt, key) % self.N

    template = """
def DEKhash(x, s):
    for c in s:
        x = ((x << 5) ^ (x >> 27) ^ ord(c)) % (1 << 31)
    return x % $NG

def perfect_hash(key):
    return (G[DEKhash($S1, key)] +
            G[DEKhash($S2, key)]) % $NG
"""

keys = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()

code = generate_code(keys, DEKHash)
print(code)
run_code(code)
