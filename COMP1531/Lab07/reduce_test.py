from reduce import reduce

def test_addition():
    assert reduce(lambda x, y: x + y, [1,2,3,4,5]) == 15

def test_multiply():
    assert reduce(lambda x, y: x * y, [1,2,3,4,5]) == 120

def test_string():
    assert reduce(lambda x, y: x + y, 'abcdefg') == 'abcdefg'

def test_none():
    assert reduce(lambda x, y: x + y, []) == None

def test_one_element():
    assert reduce(lambda x, y: x + y, [1]) == 1
    assert reduce(lambda x, y: x + y, [4]) == 4
    assert reduce(lambda x, y: x + y, ['a']) == 'a'


