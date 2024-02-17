# ----------------------------------------------------------------------
# |
# |  Math.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-02-10 15:40:00
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Basic math functions. This file illustrates how to create a python package that contains functions that can be invoked by other python code."""


# ----------------------------------------------------------------------
def Add(x, y):
    return x + y


# ----------------------------------------------------------------------
def Sub(x, y):
    return x - y


# ----------------------------------------------------------------------
def Mult(x, y):
    return x * y


# ----------------------------------------------------------------------
def Div(x, y):
    assert y != 0
    return x / y
