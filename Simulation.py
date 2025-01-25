import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
class Simulation:
    def __init__(self, state, costate, beta, sigma, gamma, cost):
        self.sus, self.exp, self.inf, self.rec = state
        self.psus, self.pexp, self.pinf, self.prec = costate
        self.beta = beta
        self.sigma = sigma
        self.gamma = gamma
        self.cost = cost
        self.control = 0
    def update_state(self, new_state):
        self.sus, self.exp, self.inf, self.rec = new_state
    def update_costate(self, new_costate):
        self.psus, self.pexp, self.pinf, self.prec = new_costate
    def return_backwards_state(self):
        # Checked: the roots are correct.
        coef = [
            (self.beta/(1-self.gamma))*self.sus*self.inf + (self.beta/(1-self.gamma))*self.exp*self.inf - self.exp,
            1-self.sigma-(self.beta/(1-self.gamma))*self.sigma*self.sus - (self.beta/(1-self.gamma))*self.sigma * self.exp - (self.beta/(1-self.gamma))*(1-self.sigma)*self.inf,
            (self.beta/(1-self.gamma))*self.sigma*(1-self.sigma)
        ]
        p = Polynomial(coef = coef)
        ans = Polynomial.roots(p)
        print("roots are {}".format(ans))
        new_exp = max(ans)
        new_inf = (self.inf-self.sigma*new_exp)/(1-self.gamma)
        new_sus = (self.sus + self.exp - (1-self.sigma)*new_exp)/(1-self.control)
        new_rec = 1 - new_exp - new_inf - new_sus
        return [new_sus,new_exp,new_inf,new_rec]

    def return_backwards_costate(self):
        temp = [
            self.psus - self.psus*(self.beta*(1 - self.control)*self.inf + self.control) + self.pexp*self.beta*(1-self.control)*self.inf,
            self.pexp - self.pexp*self.sigma + self.pinf*self.sigma,
            1 + self.pinf - self.psus*self.beta*(1-self.control)*self.sus + self.pexp*self.beta*(1-self.control)*self.sus - self.pinf*self.gamma,
            self.prec
        ]
        return temp
    def return_state(self):
        return [self.sus,self.exp,self.inf,self.rec]
    def return_costate(self):
        return [self.psus,self.pexp,self.pinf,self.prec]
    def print(self):
        print("State: {}\n Costate: {}".format(self.return_state,self.return_costate))
    def return_switching(self):
        #psus is k+1, sus is k. so update_backwards_state, then do switching, then do update_backwards_costate
        return (-self.cost + self.psus *(self.beta * self.sus * self.inf - self.sus) - self.pexp * self.beta * self.sus * self.inf + self.prec * self.sus )
    def update_control(self):
        if self.switching() < 0:
            self.control = 0
        elif self.switching() > 0:
            self.control = 1
        else:
            self.control = 0
            print('singular!!')
