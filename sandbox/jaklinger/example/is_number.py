'''
is_number

This snippet gives an example of some code that would never be promoted
to nesta-toolbox.official. 

The idea of the function is_number is determine whether the input is a
number or not. The problem is, however, poorly defined. For example, who
is to say that any of the strings:

    "NaN", "Inf", "Exp", "pi"

shouldn't be evaluated as numbers? The scope of the function is simply 
too broad, whilst the functionality is narrow.
'''

'''Determine whether the input is a number'''
def is_number(x):
    try:
        float(x)
    except ValueError:
        return False
    return True

