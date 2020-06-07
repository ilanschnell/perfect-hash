import unittest


from perfect_hash import Graph, PerfHash



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


if __name__ == '__main__':
    unittest.main()
