import pytest
from fibonacci import fib

def test_for_10():
    assert fib(10) == [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 ]

def test_for_5():
    assert fib(5) == [ 0, 1, 1, 2, 3 ]

def test_for_1():
    assert fib(1) == [0]

def test_for_0():
    assert fib(0) == "Error: n must be greater than 0"