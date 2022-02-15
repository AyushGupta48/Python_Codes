def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is
    reversed
    '''
    result_list = []
    for string in string_list:
        word = string.split()
        list_reverse = list(reversed(word))        
        result_list.append(" ".join(list_reverse))
    
    
    return result_list
    pass

if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']
