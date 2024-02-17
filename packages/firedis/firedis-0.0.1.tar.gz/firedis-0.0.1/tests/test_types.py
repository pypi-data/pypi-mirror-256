import math
import pickle
from typing import Any
import datetime as dt
from timeit import timeit
from redis import Redis
from firedis import Firedis, Namespace


def testtime(label: str, code: str, n: int):
    t = timeit(code, number=n, globals=globals())
    time_per_call_us = (t / n) * 1_000_000
    print(
        f"{label}: {round(t, 4)} s total, {time_per_call_us:.10f} microseconds per call"
    )


class MyRedis(Firedis):
    a: Namespace[Any]
    b: Namespace[Any]

keys = []
chars = ["a", "b", "c", "d"]
len_chars = len(chars)

# mset: 0.127 s total, 12.6961583039 microseconds per call
# mset2: 0.1188 s total, 11.8783875019 microseconds per call

for i in range(1000):
    char = chars[i % len_chars]
    key_length = (math.floor(i / len_chars) + 1) * 2
    new_key = char * key_length
    keys.append(new_key)


r = MyRedis()
rr = Redis()

for k in keys:
    r.a.set(k, 1)

r.a.set('a', 1)
testtime('items_old', 'r.a.items_old()', 10_000)
testtime('items', 'r.a.items()', 10_000)
quit()
r.a.clear()
r.b.clear()
r.a.set('a', 1)
r.a.set('b', 2)

r.b.set('a', 3)
r.b.set('c', 4)
r.b.set('d', 5)

print(len(r.a))
quit()
# print(r.b == {'a': 3, 'c': 4, 'd': 5})
# print({'a': 3, 'c': 4, 'd': 5} == r.b)
# print({'a': 11} | r.a)
# r.e.set('a', 1)
# print({'b': 2}.__ior__({'a': 1, 'b': 3}))
# print(*dir({}), sep='\n')
# {}.__ior__
# print({'a': 1 , 'b': 2} == {'b': 2, 'a': 1})
# print(*dir(object()), sep='\n')
quit()
d = r.e.dump("a")
print(d)
r.e.restore("a", 0, d, replace=True)
quit()

testtime('s', 'r.e.set("a", 1)', 100_000)
testtime('s2', 'r.e.set2("a", 1)', 100_000)

quit()

r = MyRedis()

r.e.set('a', 1)

testtime("p", "r.e.pexpire('a', 100_000_000)", 130_000)
quit()

n = 10_00
r.e.set("a", 1)
testtime("mget", "r.e.mget(keys)", n)
testtime("mget2", "r.e.mget2(keys)", n)
