from ForwardSimulation import ForwardSimulation
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

input_state = [np.float64(0.5575167984500102), np.float64(0.19934041250892473), np.float64(0.015891381814292678), np.float64(0.22725140722677228)]
input_costate = [0, 0, 0, 0]
[beta, sigma, gamma] = [0.5, 0.1, 0.2]
simulation = ForwardSimulation(input_state, input_costate, beta, sigma, gamma)
time_end = 74
forward_simulation_data = np.empty((time_end, 4))
forward_simulation_data[0,:] = input_state
for i in range(1,time_end):
    simulation.update_state(simulation.return_forward_state())
    forward_simulation_data[i,:] = simulation.return_state()
plt.plot(range(0,time_end), forward_simulation_data[:,0], label ='S')
plt.plot(range(0,time_end), forward_simulation_data[:,1], label ='E')
plt.plot(range(0,time_end), forward_simulation_data[:,2], label ='I')
plt.plot(range(0,time_end), forward_simulation_data[:,3], label ='R')
plt.xlabel("Time Steps")
plt.ylabel("Percent of Population")
plt.legend()
plt.title('SEIR Model')
plt.show()
print(forward_simulation_data)
