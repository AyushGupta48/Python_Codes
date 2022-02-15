from inverse import inverse
from hypothesis import given, strategies, Verbosity, settings
import pytest

@given(strategies.dictionaries(keys=strategies.integers(), values=strategies.characters()))
@settings(verbosity=Verbosity.verbose)
def test_d_inverse(d):
    inverse_dictionary = inverse(d)

    #check if the numbers are in the correct place in the inversed dictionary
    for numbers in d:
        assert numbers in inverse_dictionary[d[numbers]]
    
    # check if alphabet values are in correct place and have right integer values
    for alphabet in inverse_dictionary:
        for numbers in inverse_dictionary[alphabet]:
            assert d[numbers] == alphabet

