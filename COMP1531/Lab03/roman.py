def roman(numerals):
    '''
    Given Roman numerals as a string, return their value as an integer. You may
    assume the Roman numerals are in the "standard" form, i.e. any digits
    involving 4 and 9 will always appear in the subtractive form.

    For example:
    >>> roman("II")
    2
    >>> roman("IV")
    4
    >>> roman("IX")
    9
    >>> roman("XIX")
    19
    >>> roman("XX")
    20
    >>> roman("MDCCLXXVI")
    1776
    >>> roman("MMXIX")
    2019
    '''

    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    integer_value = 0
    for letter in range(len(numerals)):
        if (letter + 1) != len(numerals) and roman_values[numerals[letter]] < roman_values[numerals[letter + 1]]:
            integer_value = integer_value - roman_values[numerals[letter]]
        
        else:
            integer_value = integer_value + roman_values[numerals[letter]]
    
    return integer_value