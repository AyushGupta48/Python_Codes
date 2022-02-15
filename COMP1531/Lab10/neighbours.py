
def neighbours(iterable):
    '''
    A generator, that, given an iterable, yields the "neighbourhood" of each
    element. The neighbourhood is a tuple containing the element itself as well
    as the one that comes before and the one that comes after. For example,
    >>> list(neighbours([1,2,3,4]))
    [(1,2), (1,2,3), (2,3,4), (3,4)]

    Note that the first and last elements are pairs, while the rest are triples.

    Params:
      iterable (iterable): The iterable being processed. In the event it's empty,
      this generator should not yield anything. In the event it only contains
      one element, only that element should be yielded in a one-tuple.

    Yields:
      (tuple) : The neighbourhood of the current element.
    '''
    # Hint: Don't forget that iterables can produce values infinitely. You can't
    # rely on being able to retrieve all the elements at once.
    
	if len(iterable) == 0:
		yield []
	
	elif len(iterable) == 1:
		yield [(iterable[0])]
	
	elif:
		
		elements = len(iterable)

		lst_first = [iterable[0], iterable[1]]
		
		lst_last = [iterable[elements], iterable[elements-1]]

		lists = [[] for lsts in range(len(iterable) - 2)]

		i = 0
		num = i + 1

		for num in range(elements - 1):
			lists[num - 1].append(iterable[num - 1], iterable[num], iterable[num + 1])

		


