import pytest
from cool_primes import is_prime, sieve, cookbook

def test_benchmark_is_prime(benchmark):
    """Benchmark the main is_prime function with a large number."""
    benchmark(is_prime, 2**61 - 1)

@pytest.mark.parametrize("generator_func", [sieve, cookbook])
def test_benchmark_sieves(benchmark, generator_func):
    """Benchmark how quickly sieves can generate 10,000 primes."""
    
    def generate_primes():
        g = generator_func()
        for _ in range(10000):
            next(g)

    benchmark(generate_primes)