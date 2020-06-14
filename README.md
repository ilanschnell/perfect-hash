Creating minimal perfect hash functions
---------------------------------------

Generate a minimal perfect hash function for a given set of keys.
A given code template is filled with parameters, such that the
output is code which implements the hash function.
Templates can easily be constructed for any programming language.


### Installation

The minimal perfect hash function generator is written in pure Python,
and can be installed using:

    $ pip install perfect-hash

The code supports Python 2.7 and Python 3.5 or higher.
However, some of the examples do not support Python 2 anymore.


### Introduction

A perfect hash function of a certain set S of keys is a hash function
which maps all keys in S to different numbers.
That means that for the set S, the hash function is collision-free,
or perfect.
Further, a perfect hash function is called "minimal" when it maps N keys
to N *consecutive* integers, usually in the range from 0 to N-1.


### Usage

Given a set of keys which are character string, the program returns a minimal
perfect hash function.  This hash function is returned in the form of Python
code by default.  Suppose we have a file with keys:

    # 'animals.txt'
    Elephant
    Horse
    Camel
    Python
    Dog
    Cat


The exact way this file is parsed can be specified using command line
options, for example it is possible to only read one column from a file
which contains different items in each row.
The program is invoked like this:

    $ perfect-hash animals.txt
    # =======================================================================
    # ================= Python code for perfect hash function ===============
    # =======================================================================

    G = [0, 3, 6, 0, 4, 1, 5]

    def hash_f(key, T):
        return sum(ord(T[i % 8]) * ord(c) for i, c in enumerate(key)) % 7

    def perfect_hash(key):
        return (G[hash_f(key, "1mmhoNMG")] +
                G[hash_f(key, "gf53KKbH")]) % 7

    # ============================ Sanity check =============================

    K = ["Elephant", "Horse", "Camel", "Python", "Dog", "Cat"]
    assert len(K) == 6

    for h, k in enumerate(K):
        assert perfect_hash(k) == h


The way the program works is by filling a code template with the calculated
parameters.  The program can take such a template in form of a file and
fill in the calculated parameters, this allows the generation of perfect
hash function in any programming language.  The hash function is kept quite
simple and does not require machine or language specific byte level operations
which might be hard to implement in the target language.
The following parameters are available in the template, and will expand to:

    string  |  expands to
    --------+--------------------------------
      $NS   |  the length of S1 and S2
      $S1   |  array of integers S1
      $S2   |  array of integers S2
      $NG   |  length of array G
      $G    |  array of integers G
      $NK   |  the number of keys, i.e. length of array K
      $K    |  array with the quoted keys
      $$    |  $ (a literal dollar sign)


Since the syntax for arrays is not the same in all programming languages,
some specifics can be adjusted using command line options.
The built-in template which creates the above code is:

    G = [$G]

    def hash_f(key, T):
        return sum(ord(T[i % $NS]) * ord(c) for i, c in enumerate(str(key))) % $NG

    def perfect_hash(key):
        return (G[hash_f(key, "$S1")] +
                G[hash_f(key, "$S2")]) % $NG


Using code templates, makes this program very flexible.  The source repository
includes several complete examples for C.  There are many choices one
faces when implementing a static hash table: do the parameter lists go into
a separate header file, should the API for the table only contain the hash
values, but not the objects being mapped, and so on.
All these various choices are possible because of the template is simply
filled with the parameters, no matter what else is inside the template.


### Hash function types

One important option the `perfect-hash` command provides is `--hft` which is
short of "hash function type".  There are two types to choose from:

1. A random hash function generation which creates hash function with a
   random string being used as it's salt.   This is the default.
   Since the generated random hash function does not include large enough
   output for a very large number of keys (over 10,000), the perfect hash
   function generation will fail for such large keys.  However, the
   implementation of this hash function is quite simple and fast.

2. A random hash function generation which creates hash function with a
   random integers being used as it's salt.  Using this option will always
   succeed, but an implementation requires two additional integer
   arrays (appart from the always present array `G`).


### Examples

The source repository contains many useful examples (in `examples/`) which
illustrate how to use the `perfect-hash` command, as well as `python_hash.py`
as a library.


### Acknowledgments

Part of the code is based on an a program A.M. Kuchling wrote:
http://www.amk.ca/python/code/perfect-hash

The algorithm this library is based on is described in the paper
"Optimal algorithms for minimal perfect hashing",
Z. J. Czech, G. Havas and B.S. Majewski.
http://cmph.sourceforge.net/papers/chm92.pdf

I tried to illustrate the algorithm and explain how it works on:
http://ilan.schnell-web.net/prog/perfect-hash/algo.html
