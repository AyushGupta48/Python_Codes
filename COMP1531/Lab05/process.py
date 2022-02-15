import pickle 
import nltk 
import operator
import json

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
        "mostCommon": {
                "colour": most_common_colour,
                "shape": most_common_shape
        },
             
             "rawData": data
    }

    FILE.close()
    with open("processed.json", 'w') as output_file:
        json.dump(result, output_file)
                
