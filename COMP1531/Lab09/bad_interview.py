def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    num_check = 1
    temp = None
    while True:
        temp = num_check
        if num_check % 5 == 0 and num_check % 3 == 0:
            num_check = "FizzBuzz"
        
        elif num_check % 3 == 0:
            num_check = "Fizz"
        
        elif num_check % 5 == 0:
            num_check = "Buzz"       
        
            
        yield num_check
        num_check = temp
        num_check += 1
