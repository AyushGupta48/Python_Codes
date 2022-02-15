import datetime
import csv

def weather(date, location):
    '''
    
    Read from csv and load certain values
    
    '''
    
    date_num = date[:2]
    month_num = date[3:5]
    year_num = date[6:]
    
    data_appended = []
    
    with open("weatherAUS.csv") as f:
        file_reader = csv.reader(f, delimiter = ',')
        
        for data in file_reader:
            data_appended.append(data)
    
    # Create variables to check exact format of the appended data
    
    exact_format = f'{year_num}-{month_num}-{date_num}'
    
    true_data = 0
    
    # if inputed data matches date and location
    
    for item in data_appended:
        if item[0] == exact_format and item[1] == location:
            true_data = 1
            break
    
    if true_data == 0:
        return(None, None)
        
        
    # must calculate max and min
    maximum = 0
    minimum = 0
    counter = 0
    for i in data_appended:
        if i[1] == location:
            
            counter = counter + 1
            
            if i[2] != 'NA':
                minimum = minimum + float(i[2])
            
            if i[3] != 'NA':
                maximum = maximum + float(i[3])
    
    minimum_ave = minimum/counter
    maximum_ave = maximum/counter
    
    return_minimum = round(minimum_ave - float(item[2]), 1)
    return_maximum = round(float(item[3]) - maximum_ave, 1)
    
    return(return_minimum, return_maximum)
