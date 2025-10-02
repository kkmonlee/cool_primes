"""
cool_primes: A library for generating and testing prime numbers.
"""

from .sieves import (
    best_sieve,
    cookbook,
    croft,
    erat,
    sieve,
    wheel_210,
)

from .primality import (
    is_prime,
    is_prime_trial_division,
)

from .utils import filter_between, Instrument 

__all__ = [
    # Sieves
    'best_sieve', 'cookbook', 'croft', 'erat', 'sieve', 'wheel_210',
    # Primality tests
    'is_prime', 'is_prime_trial_division',
    # Utilities
    'filter_between',
    'Instrument',
]