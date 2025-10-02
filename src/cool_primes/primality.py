"""
Functions for primality testing.
"""

import random
import math

# Prime generator for trial division
from .sieves import cookbook

def is_prime_trial_division(n: int) -> bool:
    """
    Tests if n is prime using trial division.
    
    Efficient for small numbers, but very slow for large n.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    limit = math.isqrt(n)
    # Check divisibility by primes (5, 7, 11, 13, ...)
    for p in cookbook():
        if p > limit:
            break
        if n % p == 0:
            return False
    return True

def _is_composite_miller_rabin(n: int, a: int) -> bool:
    """
    Miller-Rabin test for a single base 'a'.
    
    Returns True if n is definitely composite, False if it is
    probably prime.
    """
    if n % a == 0:
      return True

    # Write n-1 as (2^s) * d
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # x = a^d mod n
    x = pow(a, d, n)
    
    if x == 1 or x == n - 1:
        return False # Probably prime
        
    # Keep squaring x until we get n-1 or finish the loop
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False # Probably prime
    
    return True # Definitely composite

def is_prime(n: int, k: int = 8, *, instrument=None) -> bool:
    """
    Tests if n is prime using the Miller-Rabin primality test.

    For n < 3,317,044,064,279,371, this test is deterministic.
    For larger n, it is probabilistic.

    Args:
        n: The integer to test.
        k: The number of rounds for probabilistic testing (higher is more accurate).
    """
    def _update_stat(flag):
        if instrument:
            instrument.update(is_prime.__name__, n, flag)

    if n < 2:
        _update_stat(0) # 0 = Not prime
        return False
    
    if n in (2, 3):
        _update_stat(1) # 1 = Prime
        return True
        
    if n % 2 == 0 or n % 3 == 0:
        _update_stat(0) # 0 = Not prime
        return False
    
    # Use deterministic sets of bases for numbers within proven ranges
    if n < 1_373_653:
        bases = [2, 3]
    elif n < 25_326_001:
        bases = [2, 3, 5]
    elif n < 3_215_031_751:
        bases = [2, 3, 5, 7]
    elif n < 2_152_302_898_747:
        bases = [2, 3, 5, 7, 11]
    elif n < 3_474_749_660_383:
        bases = [2, 3, 5, 7, 11, 13]
    elif n < 341_550_071_728_321:
        bases = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3_317_044_064_279_371:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    else:
        bases = random.sample(range(2, n - 1), k)

    for a in bases:
        if a >= n: continue
        if _is_composite_miller_rabin(n, a):
            _update_stat(0) # 0 = Not prime
            return False # Definitely composite

    _update_stat(1) # 1 = Prime
    return True # Definitely (if in range) or probably prime