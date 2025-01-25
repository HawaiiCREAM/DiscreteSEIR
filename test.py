import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
coef = [np.float64(-26.669125449715718), np.float64(13.152119652432368), 0.05625]
poly = Polynomial(coef = coef,  domain = [0, 1])
print(Polynomial.roots(poly))
