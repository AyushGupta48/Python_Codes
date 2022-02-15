from primes import factors
import pytest 

def test_12():
    assert(factors(12)) == [2,2,3]

def test_16():
    assert(factors(16) == [2, 2, 2, 2])

def test_21():
    assert(factors(21) == [3, 7])

def test_100():
    assert (factors(100)) == [2,2,5,5]

def test_112():
    assert(factors(112)) == [2,2,2,2,7]
