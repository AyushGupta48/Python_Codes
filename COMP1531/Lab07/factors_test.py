from factors import factors, is_prime
from hypothesis import given, strategies, Verbosity, settings
import pytest

@given(strategies.integers(min_value=2, max_value=1000))
@settings(verbosity=Verbosity.verbose)
def test_prime_factors(n):
    prime_list = factors(n)

    assert len(prime_list) < n

