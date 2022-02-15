import pickle 
import nltk 

def most_common():
    FILE = open('shapecolour.p', 'rb')    
    data = pickle.load(FILE)

    common_colour = []
    common_shape = []
    for element in data:
        common_colour.append(f"{element['colour']}")
        common_shape.append(f"{element['shape']}")
    
    most_common_colour = nltk.FreqDist(common_colour).max()
    most_common_shape = nltk.FreqDist(common_shape).max()
    
    result = {
                "colour": most_common_colour,
                "shape": most_common_shape
             }


    print(result)

    return result
                
print(most_common())
    
