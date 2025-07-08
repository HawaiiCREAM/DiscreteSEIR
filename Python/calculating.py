import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import fsolve
from scipy.linalg import expm, sinm, cosm, norm, eig, det, null_space
import sympy as sym
import math

t = 0.4879
t1 = 1.4985
x0 = np.array([-1.1, -0.2])
b0 = np.array([[0.4, 0.3],
               [-1.3, 1.1]])
b1 = np.array([[0.2, -1.4],
               [0.8, -0.7]])

a0 = b0
a1 = b1-b0

def lie_brac(X, Y):
    # Returns the matrix of the lie bracket
    return X@Y-Y@X

lamb = sym.Symbol('lamb')
f = a1-lamb*lie_brac(a1,a0)
deter = f[0,0]*f[1,1] - f[0,1]*f[1,0]
roots = sym.solveset(deter, lamb)
roots = list(roots)
for i in range(len(roots)):
    roots[i] = float(roots[i])
del globals()['lamb']
E = []
for k in roots:
    g = a1 - k*lie_brac(a1,a0)
    E.append(null_space(g))
m = [E[0][1]/E[0][0], E[1][1]/E[1][0]]

# Stupid patch because we have np.ndarray s
for i in range(len(m)):
    m[i] = m[i].tolist()[0]

lf0 = lie_brac(lie_brac(a1,a0),a0)
lf1 = lie_brac(lie_brac(a1,a0),a1)
u = [0]*len(m)
for i in range(len(m)):
    pa = a1@[1,m[i]]
    p = [1, -pa[0]/pa[1]]
    u[i] = -np.dot(p, lf0 @ [1,m[i]])/(np.dot(p, lf1 @ [1,m[i]]))

# fig, ax = plt.subplots(figsize=(4, 4.3))
# x = np.linspace(-2, 2, 100) # constructs a numpy array of [0.0, 1.0, ... 10.0]
# ax.set_xlim(-1.43, 0.24)
# ax.set_ylim(-0.65, 0.67)
# ax.set_xticks(np.linspace(-1.4,0.2,9))
# ax.set_yticks(np.linspace(-0.6,0.6,7))
# plt.plot(x, m[0]*x, linestyle='solid', label = 'D1')
# plt.plot(x, m[1]*x, linestyle='solid', label = 'D2')
# txt = "u = " + str(round(u[0],4)) + " and " + str(round(u[1],4))
# plt.figtext(0.5, 0.02, txt, wrap=True, horizontalalignment='center', fontsize=11)
# ax.legend()
# plt.show()


# print(str(eigs1) + "\n" + str(eigs2))
# print("E_1: y = " + str(m[0][0]) + "x. \nE_2: y = " + str(m[1][0]) + "x.")
