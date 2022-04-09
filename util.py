""" Various utility functions. 
@author Kyle Guarco
"""

# https://dev.to/turbaszek/flat-map-in-python-3g98
def flatmap(f, xs):
    return [y for ys in xs for y in f(ys)]

