import sys
import random
import unittest


from perfect_hash import (
    Graph, PerfHash, Format, Hash1, Hash2, generate_code, run_code,
    builtin_template
)


def flush_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


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


class TestsPerfHash(unittest.TestCase):

    def test_basic(self):
        d = PerfHash({'foo': (429, 'bar'),
                      42: True,
                      False: 'baz'})

        self.assertEqual(d['foo'], (429, 'bar'))
        self.assertRaises(IndexError, d.__getitem__, 'Foo')
        self.assertEqual(d[42], True)
        self.assertEqual(d[False], 'baz')
        self.assertTrue(d.has_key('foo'))
        self.assertFalse(d.has_key('bar'))

    def test_500(self):
        d = PerfHash({100 - i: i * i for i in range(500)})
        for i in range(500):
            self.assertEqual(d[100 - i], i * i)


class TestsFormat(unittest.TestCase):

    def test_basic(self):
        class o:
            delimiter = ': '
            width = 75
            indent = 4

        x = Format(o)
        self.assertEqual(x(list(range(10))), '0: 1: 2: 3: 4: 5: 6: 7: 8: 9')
        o.delimiter = '; '
        x = Format(o)
        self.assertEqual(x(list(range(5))), '0; 1; 2; 3; 4')

        o.delimiter = ' '
        x = Format(o)
        self.assertEqual(x(list(range(5)), quote=True),
                         '"0" "1" "2" "3" "4"')
        self.assertEqual(x(42), '42')
        self.assertEqual(x('Hello'), 'Hello')


class TestsIntegration(unittest.TestCase):

    def run_letters(self, K, Hash):
        keys = [chr(65 + i) for i in range(K)]
        hashes = list(range(K))

        random.shuffle(keys)

        class options:
            width = 80
            indent = 4
            delimiter = ','

        code = generate_code(list(zip(keys, hashes)),
                             builtin_template(Hash),
                             Hash,
                             options)
        run_code(code)

    def test_letters(self):
        for Hash in Hash1, Hash2:
            for K in range(0, 27):
                self.run_letters(K, Hash)
                flush_dot()


if __name__ == '__main__':
    import perfect_hash

    print('Python location:', sys.executable)
    print('Python version:', sys.version)
    print('perfect_hash location:', perfect_hash.__file__)
    print('perfect_hash version:', perfect_hash.__version__)
    print('Starting self tests ...')
    unittest.main()
