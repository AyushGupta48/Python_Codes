def reduce(f, xs):
    if xs == []:
        return None
    
    elif len(xs) == 1:
        return xs[0]
        
    #https://thepythonguru.com/python-builtin-functions/reduce/

    else:
        first = xs[0]
        for i in xs[1:]:
            first = f(first, i)
        return first
    

# if __name__ == '__main__':
#     print(reduce(lambda x, y: x + y, [1,2,3,4,5]))
#     print(reduce(lambda x, y: x * y, [1,2,3,4,5]))