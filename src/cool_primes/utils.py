"""
Encoding: UTF-8
Author: kkmonlee
Copyright 2017 kkmonlee
"""

"""
Utility functions
"""
import itertools
import math
from operator import gt
from functools import partial
from collections import namedtuple
from typing import Iterable, Iterator, Optional, TypeVar

T = TypeVar('T')

def filter_between(
        iterable: Iterator[T],
        start: Optional[T] = None,
        end: Optional[T] = None
) -> Iterator[T]:
    """
        Yield items from an iterator in the range [start, end).

    If start is provided, drops items until an item >= start is found.
    If end is provided, stops yielding when an item >= end is found.
    """
    isqrt = math.isqrt

    iterator = iter(iterable)
    if start is not None:
        iterator = itertools.dropwhile(lambda x: x < start, iterator)
    if end is not None:
        iterator = itertools.takewhile(lambda x: x < end, iterator)
    return iterator

class MethodStats:
    """Statistics for is_probably_prime methods"""
    def __init__(
        self, 
        hits: int = 0, 
        low: Optional[int] = None, 
        high: Optional[int] = None
    ):
        self.hits = hits
        self.low = low
        self.high = high

    def __repr__(self) -> str:
        name = type(self).__name__
        return f"{name}(hits={self.hits}, low={self.low}, high={self.high})"
    
    def update(self, value: int):
        self.hits += 1
        self.low = min(self.low, value) if self.low is not None else value
        self.high = max(self.high, value) if self.high is not None else value

class Instrument:
    """Instrumentation wrapper for a primality testing function"""
    def __init__(self, owner: str, methods: Iterable):
        self.calls = 0
        self.uncertain = 0
        self.prime = 0
        self.notprime = 0
        self._owner = owner
        self._stats = {func.__name__: MethodStats() for func in methods}

    def display(self):
        """Prints the instrumentation statistics to the console."""
        print(str(self))

    def __str__(self) -> str:
        """Returns a string representation of the statistics."""
        items = sorted(self._stats.items())
        items_str = '\n'.join(
            f'  - {name}: {stats}' for name, stats in items if stats.hits > 0
        )
        return (
            f'Instrumentation for {self._owner}\n'
            f'  - Total calls:           {self.calls}\n'
            f'  - Definitely not prime:  {self.notprime}\n'
            f'  - Definitely prime:      {self.prime}\n'
            f'  - Probably prime:        {self.uncertain}\n'
            f'Method Hits:\n{items_str}\n'
        )

    def update(self, name: str, n: int, flag: int):
        """
        Update stats for a given method.
        Flag: 0 = not prime, 1 = prime, 2 = uncertain.
        """
        if name not in self._stats:
            raise ValueError(f"Method '{name}' not registered for instrumentation.")

        self._stats[name].update(n)
        self.calls += 1
        if flag == 0:
            self.notprime += 1
        elif flag == 1:
            self.prime += 1
        else: # flag == 2
            self.uncertain += 1