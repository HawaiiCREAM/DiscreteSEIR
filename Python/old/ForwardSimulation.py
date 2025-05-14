import matplotlib.pyplot as plt
import numpy as np
class ForwardSimulation:
    def __init__(self, state, costate, beta, sigma, gamma):
        self.sus, self.exp, self.inf, self.rec = state
        self.psus, self.pexp, self.pinf, self.prec = costate
        self.beta = beta
        self.sigma = sigma
        self.gamma = gamma
        self.control = 0
    def update_state(self, new_state):
        self.sus, self.exp, self.inf, self.rec = new_state
    def update_costate(self, new_costate):
        self.psus, self.pexp, self.pinf, self.prec = new_costate
    def return_forward_state(self):
        sus_new = self.sus - self.beta*self.sus*self.inf*(1-self.control) - self.control*self.sus
        exp_new = self.exp + self.beta*self.sus*self.inf*(1-self.control) - self.sigma*self.exp
        inf_new = self.inf + self.sigma*self.exp - self.gamma*self.inf
        rec_new = self.rec + self.gamma*self.inf + self.control*self.sus
        return [sus_new, exp_new, inf_new, rec_new]
    def return_state(self):
        return [self.sus,self.exp,self.inf,self.rec]
    def return_costate(self):
        return [self.psus,self.pexp,self.pinf,self.prec]
    def update_control(self, control):
        self.control = control
    def print(self):
        print("State: {}\n Costate: {}".format(self.return_state,self.return_costate))
