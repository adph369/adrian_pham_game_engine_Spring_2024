#This file was created by Adrian Pham

'''
write a function that takes two arguments and multiplies them together
use a return statement
print it

write another function that converts the return from the first to a string and prints it out in a statement 

Write a while loop that uses both functions 10 times
'''

i = 0

def multiply(x, y):
    product = x * y
    return product

def printstr(x):
    print(str(x))


while i < 10:
    i += 1
    printstr(multiply(1, 10))

