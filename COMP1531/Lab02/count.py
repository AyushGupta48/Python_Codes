def count_char(message):
    '''
    Counts the number of occurrences of each character in a string. The result should be a dictionary where the key is the character and the dictionary is its count.

    For example,
    >>> count_char("HelloOo!")
    {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}
    '''
#inspiration from https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/

    frequency = {}
    
    for letter in message:
    
        #Incrementing number of characters
        if letter in frequency:
            frequency[letter] += 1
        
        #If only one character then put 1
        else:
            frequency[letter] = 1
    
    return frequency
    #pass
