from roman import roman

def test_single_values():
    assert roman('I') == 1
    assert roman('V') == 5
    assert roman('X') == 10
    assert roman('L') == 50
    assert roman('C') == 100
    assert roman('D') == 500
    assert roman('M') == 1000

def test_one_at_end():
    assert roman('VI') == 6
    assert roman('XI') == 11
    assert roman('LI') == 51
    assert roman('CI') == 101
    assert roman('DI') == 501
    assert roman('MI') == 1001

    assert roman('LXI') == 61
    assert roman('MDCCLXXVI') == 1776

def test_one_before_end():
    assert roman('IV') == 4
    assert roman('IX') == 9
    
    assert roman('MMXIX') == 2019