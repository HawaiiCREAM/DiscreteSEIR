import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import fsolve
import math
class Simulation:
    def __init__(self, state, costate, beta, sigma, gamma, cost, control_max):
        self.sus, self.exp, self.inf, self.rec = state
        self.psus, self.pexp, self.pinf, self.prec = costate
        self.beta = beta
        self.sigma = sigma
        self.gamma = gamma
        self.cost = cost
        self.control_max = control_max
        self.control = 0
    def update_state(self, new_state):
        self.sus, self.exp, self.inf, self.rec = new_state
    def update_costate(self, new_costate):
        self.psus, self.pexp, self.pinf, self.prec = new_costate
    def return_backwards_state(self):
        ### This is the quadratic root solving method
        coef = [
            (self.beta/(1-self.gamma))*self.sus*self.inf + (self.beta/(1-self.gamma))*self.exp*self.inf - self.exp,
            1-self.sigma-(self.beta/(1-self.gamma))*self.sigma*self.sus - (self.beta/(1-self.gamma))*self.sigma * self.exp - (self.beta/(1-self.gamma))*(1-self.sigma)*self.inf,
            (self.beta/(1-self.gamma))*self.sigma*(1-self.sigma)
        ]
        p = Polynomial(coef = coef)
        ans = Polynomial.roots(p)
        # print("roots are {}".format(ans))
        new_exp = max(ans)
        new_inf = (self.inf-self.sigma*new_exp)/(1-self.gamma)
        new_sus = (self.sus + self.exp - (1-self.sigma)*new_exp)/(1-self.control)
        new_rec = 1 - new_exp - new_inf - new_sus
        return [new_sus,new_exp,new_inf,new_rec]

        ### This is the numerical solving method
        # def equations(x):
        #     S, E, I, R = x
        #     return (
        #         self.sus - S + self.beta*(1-self.control)*S*I + self.control*S,
        #         self.exp - E - self.beta*(1-self.control)*S*I + self.sigma*E,
        #         self.inf - I - self.sigma*E + self.gamma*I,
        #         self.rec - R - self.gamma*I - self.control*S
        #     )
        # return fsolve(equations, [1,0,0,0])

    def return_forward_state(self, state):
        sus, exp, inf, rec = state
        sus_new = sus - self.beta*sus*exp*(1-self.control) - self.control*sus
        exp_new = exp + self.beta*sus*exp*(1-self.control) - self.sigma*exp
        inf_new = inf + self.sigma*exp - self.gamma*inf
        rec_new = rec + self.gamma*inf + self.control*sus
        return [sus_new, exp_new, inf_new, rec_new]
    def return_backwards_costate(self):
        temp = [
            self.psus - self.psus*(self.beta*(1 - self.control)*self.inf + self.control) + self.pexp*self.beta*(1-self.control)*self.inf,
            self.pexp - self.pexp*self.sigma + self.pinf*self.sigma,
            -1 + self.pinf - self.psus*self.beta*(1-self.control)*self.sus + self.pexp*self.beta*(1-self.control)*self.sus - self.pinf*self.gamma,
            self.prec
        ]
        return temp
    def return_state(self):
        return [self.sus,self.exp,self.inf,self.rec]
    def return_costate(self):
        return [self.psus,self.pexp,self.pinf,self.prec]
    def return_switching(self):
        #psus is k+1, sus is k. so update_backwards_state, then do switching, then do update_backwards_costate
        switching = -self.cost + self.psus *(self.beta * self.sus * self.inf - self.sus) - self.pexp * self.beta * self.sus * self.inf + self.prec * self.sus
        # print(switching)
        return switching
    def update_control(self):
        if self.return_switching() < 0:
            self.control = 0
        elif self.return_switching() > 0:
            self.control = self.control_max
        else:
            self.control = 0
            print('singular!!')
