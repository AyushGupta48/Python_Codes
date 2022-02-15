import math
def divisors(n):
  pass

# You may find this helpful
def is_prime(n):
    return n != 1 and divisors(n) == {1, n}

def factors(n):
    '''
    A function that generates the prime factors of n. For example
    >>> factors(12)
    [2,2,3]

    Params:
      n (int): The operand

    Returns:
      List (int): All the prime factors of n in ascending order.

    Raises:
      ValueError: When n is <= 1.
    '''

    if n <= 1:
	    raise ValueError("Number must be more than 1")
    i = 2
    factors = []
    while i * i <= n:
	    if (n % i) > 0:
		    i += 1
	    else:
		    n //= i
		    factors.append(i)
    if n > 1:
	    factors.append(n)
    
    return factors

    

