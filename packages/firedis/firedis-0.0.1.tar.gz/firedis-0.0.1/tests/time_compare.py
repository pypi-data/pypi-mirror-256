import math
import pickle
from typing import Any
import datetime as dt
from timeit import timeit
from redis import Redis
from byeredis import Firedis, Namespace


def testtime(label: str, code: str, n: int):
    t = timeit(code, number=n, globals=globals())
    time_per_call_us = (t / n) * 1_000_000
    print(
        f"{label}: {round(t, 4)} s total, {time_per_call_us:.10f} microseconds per call"
    )


class MyRedis(Firedis):
    nums: Namespace[int | float]
    docs: Namespace[dict[str, Any]]


r = MyRedis()

r.nums.set("a", 1)
r.nums.set("b", b"1")

print(r.nums.get("a"))
print(r.nums.get("b"))

n = 200_000

testtime("")

quit()


n = 1_000_000

def func():
    for i in range(n):
        r.nums.set("a", i)


# t: 7.0066 s total, 7.0065705000 microseconds per call
testtime("pickle", "r.nums.get('a')", 1_000_000)
testtime("bytes", "r.nums.get('b')", 1_000_000)
testtime("bytesr", "rr.get('nums:b')", 1_000_000)
quit()
r = MyRedis()


keys = []
chars = ["a", "b", "c", "d"]
len_chars = len(chars)

for i in range(1000):
    char = chars[i % len_chars]
    key_length = (math.floor(i / len_chars) + 1) * 2
    new_key = char * key_length
    keys.append(new_key)


# testtime("t", "r.nums.mset({k: 1 for k in keys})", 1)
testtime("keys", "print(len(r.nums.keys()))", 5)
testtime("keys2", "print(len(r.nums.keys2()))", 5)

quit()

# r.nums.set('x', 1, px=30)
# print(r.nums['x'])
# print(r.nums.mget(['x']))
# print(r.nums.get("a"))
# print(r.nums.keys())
# print()


# x = r.nums.set('x', 2, px=30)
# print(r.nums['x'])
# print(r.nums['x'])
# print(r.nums.keys())
# print(x)
# r.nums.set('a', 1)
# del r.nums['a']
# del r.nums['a']
# print(r.nums.items())
# print(r.nums.keys())


quit()
r1 = MyRedis()
r2 = Redis()
n = 200_000

# 4.0552
# 4.068
# 4.0706
# 4.0462
value = "Hello world" * 1000
t1 = timeit("r1.nums.set('b', value)", number=200_000, globals=globals())
t2 = timeit("r2.set('nums:' + 'a', value)", number=200_000, globals=globals())

# t1 = timeit("r1.nums.mget(['a', 'b', 'c', 'd'])", number=n, globals=globals())
# t2 = timeit("[v for v in r2.mget(['nums' + ':' + s for s in ['a', 'b', 'c', 'd']])]", number=n, globals=globals())
print(f"{(t1 / n * 1_000_000)=:.12f}")
print(f"{(t2 / n * 1_000_000)=:.12f}")


test_results = [
    {
        "test": 2,
        "code_fastredis": "r.nums.mget(['a', 'b', 'c', 'd'])",
        "code_redis": "[pickle.loads(v) for v in r.mget(['nums' + ':' + s for s in ['a', 'b', 'c', 'd']])]",
        "time_fastredis": 21.8491,
        "time_redis": 28.7465,
        "percent_faster": 24,
    },
]
