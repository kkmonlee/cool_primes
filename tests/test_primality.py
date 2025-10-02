import pytest
from cool_primes import is_prime, is_prime_trial_division

KNOWN_PRIMALITY = [
    (-1, False),
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (91, False),
    (7919, True),
    (7921, False),
]

@pytest.mark.parametrize("number, expected", KNOWN_PRIMALITY)
def test_is_prime_known_values(number, expected):
    """Test is_prime against a list of known values."""
    assert is_prime(number) == expected

@pytest.mark.parametrize("number, expected", KNOWN_PRIMALITY)
def test_is_prime_trial_division_known_values(number, expected):
    """Test the slower trial division method against known values."""
    if number < 1000:
        assert is_prime_trial_division(number) == expected

def test_is_prime_large_mersenne():
    """Test a very large known prime (Mersenne prime)."""
    large_prime = 2**61 - 1
    assert is_prime(large_prime) is True

def test_is_prime_large_composite():
    """Test a very large known composite number."""
    large_composite = 2**61 - 1 + 6
    assert is_prime(large_composite) is False