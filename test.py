from __future__ import print_function
import sys
import random
import string
import unittest


from perfect_hash import (
    generate_hash, Graph, Format, Hash1, Hash2, Hash3, Hash4,
    generate_code, run_code, builtin_template, TooManyInterationsError,
)


Hashes = Hash1, Hash2, Hash3, Hash4


def flush_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


def random_keys(N):
    keys = set()
    while len(keys) < N:
        keys.add(''.join(
            random.choice(string.ascii_letters + string.digits)
            for i in range(random.randint(1, 7))))
    keys = list(keys)
    random.shuffle(keys)
    return keys


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


class TestsGeneration(unittest.TestCase):

    def create_and_verify(self, keys, Hash):
        f1, f2, G = generate_hash(keys, Hash)
        f = lambda k: (G[f1(k)] + G[f2(k)]) % len(G)
        for i, k in enumerate(keys):
            self.assertEqual(i, f(k))
        flush_dot()

    def test_simple(self):
        for Hash in Hashes:
            self.create_and_verify(["Ilan", "Arvin"], Hash)

    def test_letters(self):
        for K in range(0, 27):
            keys = [chr(65 + i) for i in range(K)]
            random.shuffle(keys)
            for Hash in Hashes:
                self.create_and_verify(keys, Hash)

    def test_random(self):
        for Hash in Hash2, Hash4:
            for N in range(0, 50):
                self.create_and_verify(random_keys(N), Hash)

    def test_too_many_iterations(self):
        # through experiment, I found these two keys which cause
        # generate_hash not to work with Hash1
        keys = ['kg', 'jG']
        self.assertRaises(TooManyInterationsError,
                          generate_hash, keys, Hash1)


class TestsIntegration(unittest.TestCase):

    def run_keys(self, keys, Hash):
        code = generate_code(keys, builtin_template(Hash), Hash)
        run_code(code)
        flush_dot()

    def test_simple(self):
        for Hash in Hashes:
            self.run_keys(["Ilan", "Arvin"], Hash)

    def test_random(self):
        for Hash in Hash2, Hash4:
            self.run_keys(random_keys(50), Hash)


if __name__ == '__main__':
    import perfect_hash

    print('Python location:', sys.executable)
    print('Python version:', sys.version)
    print('perfect_hash location:', perfect_hash.__file__)
    print('perfect_hash version:', perfect_hash.__version__)
    unittest.main()
