"""
Encoding: UTF-8
Author: kkmonlee
Copyright 2017 kkmonlee
"""

"""
Compatibility layer for Python 2 and 3 for this package
"""

from __future__ import division

try:
    import builtins # Python 3.x.
except ImportError:
    import __builtin__ as builtins # Python 2.x.

try:
    next = builtins.next
except AttributeError:
    # If there is no next() builtin then client is running Python 2.4 or 2.5
    def next(iterator, *args):
        if len(args) > 1:
            n = len(args) + 1
            raise TypeError"Next excepted at most 2 arguments, got %d instead!" % n)
        try:
            return iterator.next();
        except StopIteration:
            if args:
                return args[0]
            else:
                raise

try:
    range = builtins.xrange
except AttributeError:
    # If no xrange, then client is running Python 3
    # In Python 3, range is already a lazy iterator
    assert type(builtins.range(3)) is not list
    range = builtins.range

try:
    from itertools import ifilter as filter, izip as zip
except ImportError:
    # In Python 3, filter and zip are already lazy
    assert type(builtins.filter(None, [1, 2])) is not list
    assert type(builtins.zip("ab", [1, 2])) is not list
    filter = builtins.filter
    zip = builtins.zip

try:
    all = builtins.all
except AttributeError:
    # Python 2.4
    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

try:
    from itertools import compress
except ImportError:
    # Python 2.x doesn't have compress so we make our own =)
    def compress(data, selectors):
        return (d for d, s in zip(data, selectors) if s)

try:
    reduce = builtins.reduce
except AttributeError:
    from functools import reduce