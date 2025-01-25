from Simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

input_state = [4.51649476e-03, 9.78424926e-03, 9.48564045e-03, 9.76213616e-01]
input_costate = [0, 0, 0, 0]
[beta, sigma, gamma] = [0.5, 0.1, 0.2]
cost = 0.05
time_end = 40

simulation = Simulation(input_state, input_costate, beta, sigma, gamma, cost)

backwards_simulation_data = np.empty((time_end, 4))
backwards_simulation_pdata = np.empty((time_end, 4))
backwards_simulation_data[0,:] = input_state
backwards_simulation_pdata[0,:] = input_costate

for i in range(1,3):
    diff = np.subtract(simulation.return_state(), simulation.return_forward_state(simulation.return_backwards_state()))
    print("difference of calc {}".format(diff))
    simulation.update_state(simulation.return_backwards_state())
    simulation.update_costate(simulation.return_backwards_costate())
    backwards_simulation_data[i,:] = simulation.return_state()
    backwards_simulation_pdata[i,:] = simulation.return_costate()
for i in range(3,time_end):
    diff = np.subtract(simulation.return_state(), simulation.return_backwards_state())
    print("difference of calc {}".format(diff))
    simulation.update_state(simulation.return_backwards_state())
    simulation.update_costate(simulation.return_backwards_costate())
    backwards_simulation_data[i,:] = simulation.return_state()
    backwards_simulation_pdata[i,:] = simulation.return_costate()
print(simulation.return_state())
plt.plot(range(0,time_end), backwards_simulation_data[:,0], label ='S')
plt.plot(range(0,time_end), backwards_simulation_data[:,1], label ='E')
plt.plot(range(0,time_end), backwards_simulation_data[:,2], label ='I')
plt.plot(range(0,time_end), backwards_simulation_data[:,3], label ='R')
plt.xlabel("Time Steps")
plt.ylabel("Percent of Population")
plt.legend()
plt.title('SEIR Model')
plt.gca().invert_xaxis()
plt.show()
