from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}

def test_case1():
    assert count_char("HelloOo!") == {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}

def test_case2():
    assert count_char("p1ZZa") == {'p': 1, '1': 1, 'Z': 2, 'a': 1}
    
def test_case3():
    assert count_char("...3") == {'.': 3, '3': 1}




