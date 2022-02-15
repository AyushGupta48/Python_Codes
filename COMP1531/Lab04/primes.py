import math

def factors(num):
    '''
    Returns a list containing the prime factors of 'num'. The primes should be
    listed in ascending order.

    For example:
    >>> factors(16)
    [2, 2, 2, 2]
    >>> factors(21)
    [3, 7]
    '''
    # In the case that n is even
    prime_factors = []
    
    while (num % 2 == 0):
        prime_factors.append(2)
        num = num/2
    
    # When num becomes odd
    
    for factor in range(3, int(math.sqrt(num)) + 1, 2):
        while (num % factor == 0):
            prime_factors.append(factor)
            num = num/factor
    
    if num > 2:
        prime_factors.append(num)
    
    
    return prime_factors
