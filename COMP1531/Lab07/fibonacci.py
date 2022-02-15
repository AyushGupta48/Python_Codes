def fib(n):

    fiboncci_sequence = [0, 1]
    counter = 0

    if n <= 0:
        return ("Error: n must be greater than 0")
    
    elif n == 1:
        return [0]

    else:
        while counter < n - 2:
            next_number = fiboncci_sequence[-1] + fiboncci_sequence[-2]
            fiboncci_sequence.append(next_number)
            counter += 1
        
    return fiboncci_sequence 
    
    
