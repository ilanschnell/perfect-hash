from time import perf_counter

from stations import locator


D = {}
for line in open('stations.dat'):
    call, loc = (x.strip() for x in line.split(','))
    assert locator(call) == loc
    D[call] = loc

call = "DL5BAC"
N = 1_000_000

t0 = perf_counter()
for _ in range(N):
    loc1 = D[call]
t1 = perf_counter()
for _ in range(N):
    loc2 = locator(call)
t2 = perf_counter()

print("%s  %8.3f" % (loc1, 1e3 * (t1 - t0)))
print("%s  %8.3f" % (loc2, 1e3 * (t2 - t1)))
assert loc1 == loc2 == "JO43LG"

try:
    locator("W5UN")
except KeyError:
    print("OK")
