import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import fsolve
from scipy.linalg import expm, sinm, cosm, norm, eig, det, null_space
import sympy as sym
import math

class Simulation:
    def __init__(self, state, costate, xdot, control, epsilon):
        self.x = state
        self.p = costate
        self.f1, self.f2 = xdot # takes the form f1 + uf2
        self.u = control
        self.epsilon = 0.01
    def return_switching(self):
        # <p, f1>
        return np.inner(self.p, f1 @ self.x)
    def update_control(self):
        if np.abs(return_switching()) < epsilon:
            # Singular
        elif return_switching() < 0:
            # u_min
        else return_switching() > 0:
            # u_max

# Start at x(t_0) and p(t_0)
# Calculate Phi(t_0). Then find the corresponding control.
# Push the simulation by Delta t using this control.
# Repeat
