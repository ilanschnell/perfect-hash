import sys

sys.path.append('..')
from perfect_hash import generate_hash


class PerfectDict(object):
    """
    This class is designed for creating perfect hash tables at run time,
    which is not really useful, except for teaching and testing.
    """
    def __init__(self, dic):
        self.N = len(dic)
        self.keys = []
        self.values = []
        for k, v in dic.items():
            self.keys.append(k)
            self.values.append(v)

        f1, f2, G = generate_hash(self.keys)
        self.hashval = lambda k: (G[f1(k)] + G[f2(k)]) % len(G)

    def __getitem__(self, key):
        h = self.hashval(key)
        if h < self.N and key == self.keys[h]:
            return self.values[h]
        else:
            raise KeyError(key)

    def __contains__(self, key):
        h = self.hashval(key)
        return h < self.N and key == self.keys[h]


d = {'foo': 429, 'bar': 686, 'baz': 128}
p = PerfectDict(d)

assert p['foo'] == 429
assert p['bar'] == 686
assert p['baz'] == 128
assert 'foo' in p
assert 'matchbox' not in p
print("OK")
