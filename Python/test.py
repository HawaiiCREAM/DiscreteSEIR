import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import fsolve
from scipy.linalg import expm, sinm, cosm
import math

t = 0.4879
T1 = 1.4985
x0 = np.array([-1.1, -0.2])
A0 = np.array([[0.4, 0.3], [-1.3, 1.1]])
A1 = np.array([[0.2, -1.4], [0.8, -0.7]])
print(expm(A0 * t + A1 * T1) @ x0)
