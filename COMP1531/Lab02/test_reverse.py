'''
Tests for reverse_words()
'''
from reverse import reverse_words

def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
    assert reverse_words(["Good Evening", "There I am"]) == ['Evening Good', 'am I There']
    assert reverse_words(["Hello Ayush", "I am there"]) == ['Ayush Hello', 'there am I']
    assert reverse_words(["Cristiano Ronaldo", "Soccer Player"]) == ['Ronaldo Cristiano', 'Player Soccer']
    assert reverse_words(["Lionel Messi", "The Kid Laroi"]) == ['Messi Lionel', 'Laroi Kid The']
    
