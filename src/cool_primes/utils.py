"""
Encoding: UTF-8
Author: kkmonlee
Copyright 2017 kkmonlee
"""

"""
Utility functions
"""

from __future__ import division

import itertools
import operator

try:
    # Improve speed with partial, if available
    from functools import partial
except ImportError:
    partial = None

def filter_between(iterable, start=None, end=None):
    """
    Yield items from iterable in the range(start, end).

    Returns an iterator from the given iterable.
    """
    iterator = iter(iterable)
    if start is not None:
        # Drop values strictly less than start
        if partial is None:
            drop = lambda p: p < start
        else:
            # Skip over any values where v < start but
            # partial assigns operands from left so
            # it has to be written as start > p
            drop = partial(operator.gt, start)
        iterator = itertools.dropwhile(drop, iterator)
    if end is not None:
        # Take values strictly less than end
        if partial is None:
            take = lambda p: p < end
        else:
            # Halt at the first value where v >= end but
            # partial assigns operabds from left so it
            # has to be written as end > p
            take = partial(operator.gt, end)
        iterator = itertools.takewhile(take, iterator)
    return iterator

# Every integer between 0 and MAX_EXACT inclusive
MAX_EXACT = 9007199254740991

# Get number of bits needed to represent an int in binary
try:
    _bit_length = int.bit_length
except AttributeError:
    def _bit_length(n):
        if n == 0:
            return 0
        elif n < 0:
            n = -n
        assert n >= 1
        numbits = 0
        # Accelerate function for larger values of n
        while n > 2**64:
            numbits += 64; n >>= 64
        while n:
            numbits += 1; n >>= 1
        return numbits

def isqrt(n):
    """
    Return the integer square root of n.
    """
    if n < 0:
        raise ValueError("Square root undefined for negative numbers!")
    elif n <= MAX_EXACT:
        # Floating point
        return int(n ** 0.5)
    return _isqrt(n)

def _isqrt(n):
    if n == 0:
        return 0
    bits = _bit_length(n)
    a, b = divmod(bits, 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y

try:
    from collections import namedtuple
except ImportError:
    # Raised if Python 2.4. We can use a regular typle.
    def namedtuple(name, fields):
        return tuple

class MethodStats(object):
    """
    Statistics for is_probably_prime
    """
    def __init__(self, hits=0, low=None, high=None):
        self.hits = hits
        self.low = low
        self.high = high
    
    def __repr__(self):
        template = "%s(hits=%d, low=%r, high=%r)"
        name = type(self).__name__
        return template % (name, self.hits, self.low, self.high)

    def update(self, value):
        self.hits += 1
        a, b = self.low, self.high
        if a is None: a = value
        else: a = min(a, value)
        if b is None: b = value
        else: b = max(b, value)
        self.low, self.high = a, b

class Instrument(object):
    """
    Instrumentation for is_probable_prime
    """
    def __init__(self, owner, methods):
        self.calls = 0
        self.uncertain = 0
        self.prime = 0
        self.notprime = 0
        self._owner = owner
        self._stats = {}
        for function in methods:
            self._stats[function.__name__] = MethodStats()

    def display(self):
        print(str(self))

    def __str__(self):
        template = (
                'Instrumentation for %s\n'
                '  - definitely not prime:  %d\n'
                '  - definitely prime:      %d\n'
                '  - probably prime:        %d\n'
                '  - total:                 %d\n'
                '%s\n'
            )
        items = sorted(self._stats.items())
        items = ['%s: %s' % item for item in items if item[1].hits != 0]
        items = '\n'.join(items)
        args = (self._owner, self.notprime, self.prime, self.uncertain, self.calls, items)
        return template % args

    def update(self, name, n, flag):
        assert flag in (0, 1, 2)
        self._stats[name].update(n)
        self.calls += 1
        if flag == 0:
            self.notprime += 1
        elif flag == 1:
            self.prime += 1
        else:
            self.uncertain += 1