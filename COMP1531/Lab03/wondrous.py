import math
def wondrous(start):
    '''
    Returns the wondrous sequence for a given number.
    '''
    current = start
    sequence = []

    while current != 1:
        sequence.append(current)
        if (current % 2 == 0):
            current = math.trunc(current/2) # math.trunc gets rid of decimal
        else:
            current = (current * 3) + 1
    
    sequence.append(1)

    return sequence
