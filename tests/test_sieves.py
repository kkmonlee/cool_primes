import pytest
import itertools
from cool_primes import erat, sieve, cookbook

SIEVE_GENERATORS = [
    sieve,
    cookbook,
]

@pytest.fixture(scope="module")
def first_1000_primes():
    """
    A "fixture" that provides the first 1000 primes.
    This is calculated once and reused for all tests in this module.
    """
    return erat(7920)

@pytest.mark.parametrize("generator", SIEVE_GENERATORS)
def test_sieves_match_reference(generator, first_1000_primes):
    """
    Verify that the first 1000 primes from each generator
    match the list from our trusted erat() sieve.
    """
    generated_primes = list(itertools.islice(generator(), 1000))
    assert generated_primes == first_1000_primes