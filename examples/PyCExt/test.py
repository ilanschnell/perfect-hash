from __future__ import print_function
import sys
from timeit import timeit

from stations import locator


call = sys.argv[1]
print(repr(call))

D = {}
N = 1000 * 1000

for line in open('stations.dat'):
    c, l = [x.strip() for x in line.split(',')]
    D[c] = l

print(repr(D[call]))
print(timeit("D[%r]" % call, "from __main__ import D", number=N))

print(repr(locator(call)))
print(timeit("locator(%r)" % call, "from __main__ import locator", number=N))
