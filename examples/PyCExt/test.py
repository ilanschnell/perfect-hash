from timeit import timeit

from stations import locator


D = {}
for line in open('stations.dat'):
    c, l = (x.strip() for x in line.split(','))
    assert locator(c) == l
    D[c] = l

call = 'DL5BAC'
N = 1_000_000

print(D[call])
print(timeit("D[%r]" % call, "from __main__ import D", number=N))

print(locator(call))
print(timeit("locator(%r)" % call, "from __main__ import locator", number=N))
