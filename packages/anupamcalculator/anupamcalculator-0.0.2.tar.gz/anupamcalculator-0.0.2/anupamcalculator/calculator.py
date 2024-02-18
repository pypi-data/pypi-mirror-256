# calculator.py
# This module contains the calculator functions

# Import the math module
import math

# Define the calculator functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x / y

def sqrt(x):
    if x < 0:
        return "Error! Square root of a negative number."
    else:
        return math.sqrt(x)

def power(x, y):
    return x ** y

def sine(x):
    return math.sin(math.radians(x))

def cosine(x):
    return math.cos(math.radians(x))

def tangent(x):
    return math.tan(math.radians(x))

def logarithm(x, base):
    if x <= 0 or base <= 0 or base == 1:
        return "Error! Invalid input for logarithm."
    else:
        return math.log(x, base)
