from typing import List

def add(values: List[float]) -> float:
    """ Add a list of values. """
    return sum(values)

def subtract(values: List[float]) -> float:
    """ Subtract a list of values. """
    return values[0] - sum(values[1:])

def multiply(values: List[float]) -> float:
    """ Multiply a list of values. """
    product = 1
    for v in values:
        product *= v
    return product

def divide(values: List[float]) -> float:
    """ Divide a list of values. """
    result = values[0]
    for v in values[1:]:
        if v == 0:
            raise ValueError('Cannot divide by zero')
        result /= v
    return result
