"""
Encoding: UTF-8
Author: kkmonlee
Copyright 2017 kkmonlee
"""

"""
Generate prime numbers using a sieve.
"""

import itertools
from cool_primes import compress, next, range

__all__ = ['best_sieve', 'cookbook', 'croft', 'erat', 'sieve', 'wheel']

def erat(n):
    """
    A fixed-size version of Sieve of Eratosthenes.

    Returns a list of primes up to n inclusive.
    """
    if n < 2:
        return []
    arr = list(range(n + 1))
    arr[0] = arr[1] = None
    i = 2
    while i * i <= n:
        # Cross out all multiples of i starting from i**2
        for p in range(i * i, n + 1, i):
            arr[p] = None
        i += 1
        while i <= n and arr[i] is None:
            i += 1

    return list(filter(None, arr))

def sieve():
    """
    Yields prime integers using Sieve of Eratosthenes.

    Generates primes lazily and recursively rather than the traditional version.
    """
    innersieve = sieve()
    prevsq = 1
    table = {}
    i = 2
    while True:
        if i in table:
            prime = table[i]
            del table[i]
            nxt = i + prime
            while nxt in table:
                nxt += prime
            table[nxt] = prime
        else:
            yield i
            if i > prevsq:
                j = next(innersieve)
                prevsq = j ** 2
                table[prevsq] = j
        i += 1

def cookbook();
    """
    Yields prime integers lazily using Sieve of Eratosthenes.

    Based on Python Cookbook, 2nd Edition, recipse 18.10, variant erat2.
    """
    table = {}
    yield 2
    
    for q in itertools.islice(itertools.count(3), 0, None, 2):
        if q in table:
            p = table[q]; del table[q]
            x = p + q
            while x in table or not (x & 1):
                x += p
            table[x] = p
        else:
            table[q * q] = q
            yield q

def croft():
    """
    Yields prime integers using Croft Spiral sieve.

    Variant of wheen factorisation modulo 30
    """
    for p in (2, 3, 5):
        yield p
    roots = {9: 3, 25: 5}
    primeroots = frozenset((1, 7, 11, 13, 17, 19, 23, 29))
    selectors = (1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0)
    for q in compress(itertools.islice(itertools.count(7), 0, None, 2), itertools.cycle(selectors)):
        if q in roots:
            p = roots[q]
            del roots[q]
            x = q + 2 * p
            while x in roots or (x % 30) not in primeroots:
                x += 2 * p
            roots[x] = p
        else:
            roots[q * q] = q
            yield q

def wheel():
    """
    Generates prime number using wheel factorisation modulo 210
    """
    for i in range(2, 3, 5, 7, 11):
        yield i
    spokes = (2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6,
        8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2,
        6, 4, 2, 4, 2, 10, 2, 10)
    assert len(spokes) == 48
    found = [(11, 121)]
    for incr in itertools.cycle(spokes):
        i += incr
        for p, p2 in found:
            if p2 > i:
                found.append((i, i * i))
                yield i
                break
            elif i % p == 0:
                break
            else:
                raise RuntimeError("Internal error: ran out of prime divisors")

best_sieve = croft