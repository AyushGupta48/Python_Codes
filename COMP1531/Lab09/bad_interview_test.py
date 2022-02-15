from bad_interview import bad_interview
import inspect

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(bad_interview), "bad_interview does not appear to be a generator"

def test_bad_interview_2():
    '''
    Check the first 5 numbers yielded by the iterator.
    '''
    g = bad_interview()
    first5 = [next(g) for _ in range(5)]
    assert first5 == [1, 2, 'Fizz', 4, 'Buzz']

def test_bad_interview():
    '''
    Check the first 20 numbers yielded by the iterator.
    '''
    g = bad_interview()
    first20 = [next(g) for _ in range(20)]
    assert first20 == [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz', 19, 'Buzz']
