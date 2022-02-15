from circle import Circle

def test_small():
    c = Circle(3)
    assert(round(c.circumference(), 1) == 18.8)
    assert(round(c.area(), 1) == 28.3)

def test_new():
    c = Circle(10)
    assert(round(c.circumference(), 1) == 62.8)
    assert(round(c.area(), 1) == 314.2)

def test_one():
    c = Circle(1)
    assert(round(c.circumference(), 1) == 6.3)
    assert(round(c.area(), 1) == 3.1)

def test_eight():
    c = Circle(8)
    assert(round(c.circumference(), 1) == 50.3)
    assert(round(c.area(), 1) == 201.1)

def test_big():
    c = Circle(2000)
    assert(round(c.circumference(), 1) == 12566.4)
    assert(round(c.area(), 1) == 12566370.6)
