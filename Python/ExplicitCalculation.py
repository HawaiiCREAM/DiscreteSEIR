import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import fsolve
from scipy.linalg import expm, sinm, cosm, norm, eig, det, null_space
import sympy as sym
import math

# \dot x = (A1 + uA2)x

a1_11, a1_12, a1_21, a1_22 = sym.symbols('a1_11, a1_12, a1_21, a1_22')
a2_11, a2_12, a2_21, a2_22 = sym.symbols('a2_11, a2_12, a2_21, a2_22')
A1 = sym.Matrix([[a1_11, a1_12], [a1_21, a1_22]])
A2 = sym.Matrix([[a2_11, a2_12], [a2_21, a2_22]])

def lie_brac(X, Y):
    # Returns the matrix of the lie bracket
    return X@Y-Y@X

# Finding lambda
B = lie_brac(A1, A2)
lamb = sym.symbols('lamb')
lamb = list(sym.solveset((A2-lamb*B).det(), lamb))

x1, x2 = sym.symbols('x1, x2')
x = sym.Matrix([x1, x2])
print(sym.solveset((A2-lamb[1]*B)@x, x))
# Finding the kernel
