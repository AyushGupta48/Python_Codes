from list_exercises import reverse_list, minimum, sum_list, maximum

def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]
    
    m = ["soccer", "fame", "money"]
    reverse_list(m)
    assert m == ["money", "fame", "soccer"]
    
    n = ["ronaldo", "messi", "mbappe"]
    reverse_list(n)
    assert n == ["mbappe", "messi", "ronaldo"]

def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1
    assert minimum([2, 4, 5, 10]) == 2
    assert minimum([5, 4, 7, 3]) == 3

def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21
    assert sum_list([1, 2, 3, 4]) == 10
    assert sum_list([7, 7, 6]) == 20
    
def test_max_positive():
    assert maximum([1, 2, 3, 10]) == 10
    assert maximum([20, 4, 5, 10]) == 20
    assert maximum([5, 4, 7, 3]) == 7
