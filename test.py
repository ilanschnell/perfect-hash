from __future__ import print_function
import sys
import random
import string
import unittest


from perfect_hash import (
    generate_hash, Graph, Format, Hash1, Hash2, Hash3, Hash4,
    generate_code, run_code, builtin_template
)


def flush_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


class PerfectDict(object):
    """
    This class is designed for creating perfect hash tables at run time,
    which is not really useful, except for teaching and testing.
    """
    def __init__(self, dic, Hash):
        self.N = len(dic)
        self.keys = []
        self.values = []
        for k, v in dic.items():
            self.keys.append(k)
            self.values.append(v)

        self.f1, self.f2, self.G = generate_hash(self.keys, Hash)

    def hashval(self, key):
        return (self.G[self.f1(key)] + self.G[self.f2(key)]) % len(self.G)

    def __getitem__(self, key):
        h = self.hashval(key)
        if h < self.N and key == self.keys[h]:
            return self.values[h]
        else:
            raise IndexError("no such key: %s" % key)

    def __contains__(self, key):
        h = self.hashval(key)
        return h < self.N and key == self.keys[h]


class TestsGenerateCode(unittest.TestCase):

    def test_month(self):
        month = 'jan feb mar apr may jun jul aug sep oct mov dec'.split()

        def mkRandHash(N):
            """
            Return a random hash function which
            returns hash values from 0..N-1
            """
            junk = "".join(random.choice(string.ascii_letters + string.digits)
                           for unused in range(10))
            return lambda key: hash(junk + str(key)) % N

        f1, f2, G = generate_hash(month, mkRandHash)

        for h, k in enumerate(month):
            self.assertEqual(h, (G[f1(k)] + G[f2(k)]) % len(G))


class TestsGraph(unittest.TestCase):

    def test_basic(self):
        G = Graph(3)
        # is acyclic
        self.assertTrue(G.assign_vertex_values())

        # now we make an edge between vertex 0 and 1 with desired edge value 2
        G.connect(0, 1, 2)
        # the graph is still acyclic
        self.assertTrue(G.assign_vertex_values())

        # make another edge 1:2 with desired edge value 1
        G.connect(1, 2, 1)
        self.assertTrue(G.assign_vertex_values())
        self.assertEqual(G.vertex_values, [0, 2, 2])
        # What do these values mean?
        # When you add the values for edge 0:1 you get 0 + 2 = 2, as desired.
        # For edge 1:2 you add 2 + 2 = 4 = 1 (mod 3), as desired.

        # adding edge 0:2 produces a loop, so the graph is no longer acyclic
        G.connect(0, 2, 0)
        self.assertFalse(G.assign_vertex_values())


class TestsPerfectDict(unittest.TestCase):

    def test_basic(self):
        d = {'foo': (429, 'bar'), 42: True, False: 'baz'}
        d = PerfectDict(d, Hash4)

        self.assertEqual(d['foo'], (429, 'bar'))
        self.assertRaises(IndexError, d.__getitem__, 'Foo')
        self.assertEqual(d[42], True)
        self.assertEqual(d[False], 'baz')
        self.assertTrue('foo' in d)
        self.assertFalse('bar' in d)
        self.assertFalse('matchbox' in d)


class TestsFormat(unittest.TestCase):

    def test_basic(self):
        x = Format(delimiter=': ')
        self.assertEqual(x(list(range(7))), '0: 1: 2: 3: 4: 5: 6')

        x = Format(delimiter='; ')
        self.assertEqual(x(list(range(5))), '0; 1; 2; 3; 4')

        x = Format(delimiter=' ')
        self.assertEqual(x(list(range(5)), quote=True),
                         '"0" "1" "2" "3" "4"')
        self.assertEqual(x(42), '42')
        self.assertEqual(x('Hello'), 'Hello')


class TestsIntegration(unittest.TestCase):

    def run_keys(self, keys, Hash):

        class options:
            width = 80
            indent = 4
            delimiter = ','

        code = generate_code(keys,
                             builtin_template(Hash),
                             Hash,
                             options)
        run_code(code)
        flush_dot()

    def test_letters(self):
        for Hash in Hash1, Hash2, Hash3, Hash4:
            for K in range(0, 27):
                keys = [chr(65 + i) for i in range(K)]
                random.shuffle(keys)
                self.run_keys(keys, Hash)

    def test_random(self):

        def random_word():
            return ''.join(random.choice(string.ascii_letters + string.digits)
                           for i in range(random.randint(1, 20)))

        N = 250
        for Hash in Hash1, Hash2, Hash3, Hash4:
            keys = list(set(random_word() for unused in range(N)))
            random.shuffle(keys)
            self.run_keys(keys, Hash)


if __name__ == '__main__':
    import perfect_hash

    print('Python location:', sys.executable)
    print('Python version:', sys.version)
    print('perfect_hash location:', perfect_hash.__file__)
    print('perfect_hash version:', perfect_hash.__version__)
    unittest.main()
