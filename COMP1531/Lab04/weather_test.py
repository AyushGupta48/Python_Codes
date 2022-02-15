from weather import weather
import pytest

def test_given():
    assert(weather('08-08-2010', 'Albury')) == (10.8, -10.0)

def test_Tuggeranong():
    assert(weather('07-07-2010', 'Tuggeranong')) == (9.2, -8.3)
    
def test_Portland():    
    assert(weather('29-09-2015', 'Portland')) == (0.2, -4.2)

def test_None():
    assert(weather('29-29-2029', 'UNSW')) == (None, None)
