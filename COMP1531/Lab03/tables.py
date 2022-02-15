from random import randint

num_1 = randint(2, 12)
num_2 = randint(2, 12)

real_answer = num_1 * num_2

user_answer = int(input(f'What is {num_1} x {num_2}? '))

while (user_answer != real_answer):
    print("Incorrect - try again.")
    user_answer = int(input(f'What is {num_1} x {num_2}? '))
    
    if (user_answer == real_answer):
        break

print("Correct!")