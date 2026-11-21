import os
import random
import string
import subprocess
import sys
import tempfile
import unittest
from ast import literal_eval
from types import SimpleNamespace


from perfect_hash import (
    anum_chars, quote_string,
    generate_hash, Graph, Format, StrSaltHash, IntSaltHash,
    generate_code, run_code, builtin_template, TooManyIterationsError,
    read_table,
)


Hashes = StrSaltHash, IntSaltHash


def flush_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


def random_keys(N):
    keys = set()
    while len(keys) < N:
        keys.add(''.join(random.choices(anum_chars, k=random.randint(1, 7))))
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
        self.assertEqual(x(42), 42)
        self.assertEqual(x('Hello'), 'Hello')

    def test_quote_string(self):
        for a, b in [
                ('a', '"a"'),
                ("a'b", '"a\'b"'),    # single quote (') is not escaped
                ('a"b', r'"a\"b"'),   # double quote (") is escaped
                (r'a\b', r'"a\\b"'),
                ('a\tb', r'"a\tb"'),
                ('a\n', r'"a\n"'),
                ('\rz', r'"\015z"'),  # ord('\r') = ord('\015') = 0o15 = 13
                ('café', '"café"'),
                ('\x01z', r'"\001z"'),
                ('\x7fz', r'"\177z"'),
        ]:
            self.assertEqual(quote_string(a), b)
            self.assertEqual(literal_eval(b), a)


class TestsGenerateHash(unittest.TestCase):

    def test_args(self):
        generate_hash(["A", "B"])
        generate_hash(("A", "B", "C"))
        self.assertRaises(TypeError, generate_hash, {})
        self.assertRaises(TypeError, generate_hash, "ABC")
        self.assertRaises(TypeError, generate_hash, iter(["A", "B"]))
        self.assertRaises(TypeError, generate_hash, ["A", 8])
        self.assertRaises(TypeError, generate_hash, ["A", []])
        # duplicate keys
        self.assertRaises(ValueError, generate_hash, ["A", "B", "B"])
        self.assertRaises(ValueError, generate_hash, ["A", "B"], trials=0)

    def create_and_verify(self, keys, Hash, pow2=False):
        f1, f2, G = generate_hash(keys, Hash, pow2)
        self.assertEqual(len(f1.salt), len(f2.salt))
        self.assertTrue(f1.N == f2.N == len(G))
        if pow2:
            n = len(G)
            self.assertGreater(n, 0)
            self.assertEqual(n & (n - 1), 0)

        f = lambda k: (G[f1(k)] + G[f2(k)]) % len(G)
        for i, k in enumerate(keys):
            self.assertEqual(i, f(k))

        if keys:
            slen = max(len(k.encode()) for k in keys)
            self.assertEqual(slen, len(f1.salt))
        flush_dot()

    def test_simple(self):
        for Hash in Hashes:
            self.create_and_verify(["Ilan", "Arvin"], Hash)

    def test_unicode(self):
        for Hash in Hashes:
            self.create_and_verify([u"\ud55c", "A", u"\u00a2"], Hash)

    def test_letters(self):
        for k in range(27):
            keys = random.sample(string.ascii_uppercase, k)
            for Hash in Hashes:
                self.create_and_verify(keys, Hash)

    def test_random(self):
        for Hash in Hashes:
            for N in range(50):
                for pow2 in False, True:
                    self.create_and_verify(random_keys(N), Hash, pow2)

    def test_too_many_iterations(self):

        def Hash(N):
            # the returned hash function has no random salt
            return lambda key: hash(key) % N

        keys = ['kg', 'jG']
        self.assertRaises(TooManyIterationsError,
                          generate_hash, keys, Hash)


class TestsGenerateCode(unittest.TestCase):

    def test_args(self):
        run_code(generate_code(["A", "B"]))
        run_code(generate_code(["A", "B"],
                               IntSaltHash, builtin_template(IntSaltHash)))

    def run_keys(self, keys, Hash):
        code = generate_code(keys, Hash)
        run_code(code)
        flush_dot()

    def test_simple(self):
        for Hash in Hashes:
            self.run_keys(["Ilan", "Arvin"], Hash)

    def test_special_keys(self):
        keys = ['a"b', "a'b", r'a\b', 'a\tb', '\nz', 'a\rb', 'café']
        for Hash in Hashes:
            self.run_keys(keys, Hash)

    def test_random(self):
        for Hash in Hashes:
            self.run_keys(random_keys(50), Hash)


class TestReadTable(unittest.TestCase):

    def read(self, text, **kwargs):
        options = SimpleNamespace(comment='#', splitby=',', keycol=1)
        options.__dict__.update(kwargs)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'keys.txt')
            with open(path, 'w', encoding='utf-8') as fo:
                fo.write(text)
            return read_table(path, options)

    def test_basic(self):
        text = """\
# comment
0, Elephant, ignored
1, café, ignored  # trailing comment

2, Python, ignored
"""
        self.assertEqual(self.read(text, keycol=2),
                         ['Elephant', 'café', 'Python'])

    def test_errors(self):
        with self.assertRaisesRegex(ValueError, 'no keys found'):
            self.read('# comment\n\n')

        with self.assertRaisesRegex(ValueError, ':2: cannot read key'):
            self.read('0, Elephant\n1\n', keycol=2)


class TestsCLI(unittest.TestCase):

    def test_seed(self):
        root = os.path.dirname(__file__)
        cmd = [sys.executable, os.path.join(root, 'perfect_hash.py'),
               os.path.join(root, 'animals.txt'), '--seed', '123']
        self.assertEqual(subprocess.check_output(cmd),
                         subprocess.check_output(cmd))

    def test_template_output_path(self):
        root = os.path.dirname(__file__)
        with tempfile.TemporaryDirectory(prefix='tmpl-') as tmpdir:
            tmpl = os.path.join(tmpdir, 'example-tmpl.txt')
            with open(tmpl, 'w') as fo:
                fo.write('$NK\n')

            subprocess.check_call([
                sys.executable, os.path.join(root, 'perfect_hash.py'),
                os.path.join(root, 'animals.txt'), tmpl,
            ])
            with open(os.path.join(tmpdir, 'example-code.txt')) as fi:
                self.assertEqual(fi.read(), '6\n')


if __name__ == '__main__':
    import perfect_hash

    print('Python location:', sys.executable)
    print('Python version:', sys.version)
    print('perfect_hash location:', perfect_hash.__file__)
    print('perfect_hash version:', perfect_hash.__version__)
    unittest.main()
