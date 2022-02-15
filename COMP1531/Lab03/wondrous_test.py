from wondrous import wondrous

def test_basic():
    assert wondrous(3) == [3, 10, 5, 16, 8, 4, 2, 1]
    assert wondrous(2) == [2, 1]
def test_2():
    assert wondrous(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
def test_3():
    assert wondrous(4) == [4, 2, 1]
def test_4():
    assert wondrous(5) == [5, 16, 8, 4, 2, 1]
def test_5():
    assert wondrous(11) == [11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
