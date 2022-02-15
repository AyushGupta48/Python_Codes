income = int(input("Enter your income: "))

if (income <= 18200):
    tax = 0

elif (income >= 18201 and income <= 37000):
    tax = float(0.19 * (income - 18200))

elif (income >= 37001 and income <= 87000):
    tax = 3572 + float(0.325 * (income - 37000))
    
elif (income >= 87001 and income <= 180000):
    tax = 19822 + float( 0.37 * (income - 87000))

elif (income >= 180001):
    tax = 54232 + float(0.45 * (income - 180000))

#https://intellipaat.com/community/2447/how-to-print-number-with-commas-as-thousands-separators
#Format for commas at thousands taken from above website
tax = '{:,.2f}'.format(tax)
print(f'The estimated tax on your income is ${tax}')
