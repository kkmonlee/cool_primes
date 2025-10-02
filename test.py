import cool_primes
from cool_primes import Instrument
import itertools

primes_to_100 = cool_primes.erat(100)
print(f"Primes up to 100: {primes_to_100}")

first_20_primes = list(itertools.islice(cool_primes.best_sieve(), 20))
print(f"First 20 primes: {first_20_primes}")

print(f"Is 29 prime? {cool_primes.is_prime(29)}")
print(f"Is 91 prime? {cool_primes.is_prime(91)}")

large_prime = 2**61 - 1
print(f"Is 2**61 - 1 prime? {cool_primes.is_prime(large_prime)}")

prime_generator = cool_primes.best_sieve()

primes_in_range = cool_primes.filter_between(prime_generator, start=1_000_000, end=1_001_000)

print("Primes between 1,000,000 and 1,001,000:")
print(list(primes_in_range))

methods_to_track = [cool_primes.primality.is_prime] 

my_instrument = Instrument(owner="is_prime_profiling", methods=methods_to_track)

for i in range(1000):
    cool_primes.is_prime(i, instrument=my_instrument)

large_prime = 2**61 - 1
cool_primes.is_prime(large_prime, instrument=my_instrument)
cool_primes.is_prime(large_prime + 6, instrument=my_instrument)

my_instrument.display()