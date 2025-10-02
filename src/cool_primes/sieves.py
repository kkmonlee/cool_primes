"""
Encoding: UTF-8
Author: kkmonlee
Copyright 2017 kkmonlee
"""

"""
Generate prime numbers using various sieve algorithms.
"""

import itertools
from typing import Iterator, List

__all__ = ['best_sieve', 'cookbook', 'croft', 'erat', 'sieve', 'wheel_210']

def erat(n: int) -> List[int]:
    """A fixed-size Sieve of Eratosthenes."""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False
    return [i for i, prime in enumerate(is_prime) if prime]

def sieve() -> Iterator[int]:
    """Yields prime integers using a lazy Sieve of Eratosthenes."""
    composites = {}
    i = 2
    while True:
        if i not in composites:
            yield i
            composites[i * i] = i
        else:
            prime = composites.pop(i)
            next_composite = i + prime
            while next_composite in composites:
                next_composite += prime
            composites[next_composite] = prime
        i += 1

def cookbook() -> Iterator[int]:
    """Yields prime integers lazily, based on a Python Cookbook recipe."""
    yield 2
    composites = {}
    for q in itertools.count(3, 2):
        if q not in composites:
            yield q
            composites[q * q] = q
        else:
            prime = composites.pop(q)
            next_composite = q + 2 * prime
            while next_composite in composites:
                next_composite += 2 * prime
            composites[next_composite] = prime

def croft() -> Iterator[int]:
    """Yields prime integers using the Croft Spiral sieve (a wheel mod 30)."""
    for p in (2, 3, 5):
        yield p
    composites = {}
    wheel_increments = itertools.cycle([6, 4, 2, 4, 2, 4, 6, 2])
    q = 7
    while True:
        if q not in composites:
            yield q
            composites[q * q] = q
        else:
            prime = composites.pop(q)
            next_composite = q + 2 * prime
            while next_composite in composites:
                next_composite += 2 * prime
            composites[next_composite] = prime
        q += next(wheel_increments)

def wheel_210() -> Iterator[int]:
    """Generates prime numbers using wheel factorization modulo 210."""
    for p in (2, 3, 5, 7):
        yield p
    composites = {}
    increments = (6, 4, 2, 4, 2, 4, 6, 2, 4, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10)
    q = 11
    # Create the wheel generator object once
    wheel_gen = itertools.cycle(increments)
    while True:
        if q not in composites:
            yield q
            composites[q * q] = q
        else:
            prime = composites.pop(q)
            next_composite = q + 2 * prime
            while next_composite in composites:
                next_composite += 2 * prime
            composites[next_composite] = prime
        q += next(wheel_gen)

best_sieve = cookbook