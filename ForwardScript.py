from ForwardSimulation import ForwardSimulation
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

input_state = [0.75477475, 0.04110227, 0.09558576, 0.10853721]
input_costate = [-5.93516233, -7.6998874, -8.14133978, 0]
[beta, sigma, gamma] = [0.5, 0.1, 0.2]
cost = 0.5
control_max = 0.00005
simulation = ForwardSimulation(input_state, input_costate, beta, sigma, gamma)
time_end = 80
forward_simulation_data = np.zeros((time_end, 4))
forward_simulation_control_data = np.zeros(time_end)
forward_simulation_data[0,:] = input_state
forward_simulation_control_data[0] = 0
for i in range(1,time_end):
    simulation.update_state(simulation.return_forward_state())
    forward_simulation_data[i,:] = simulation.return_state()

total_cost = sum(forward_simulation_data[:time_end, 2]) + sum(forward_simulation_control_data[:time_end]*cost)
# print(recforward_simulation_data[:time_end, 2])

x_axis = range(0,time_end)[::-1]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 13))
ax1.plot(x_axis, forward_simulation_data[:time_end,0], '.', label ='S')
ax1.plot(x_axis, forward_simulation_data[:time_end,1], '.', label ='E')
ax1.plot(x_axis, forward_simulation_data[:time_end,2], '.', label ='I')
ax1.plot(x_axis, forward_simulation_data[:time_end,3], '.', label ='R')
ax1.set(xlabel = "Time Step", ylabel = "Ratio of Population")
ax1.set_title("SEIR Model")
ax1.legend()
# ax1.xaxis.set_inverted(True)

ax2.plot(x_axis, forward_simulation_control_data[:time_end], '.', label = 'u')
ax2.set(xlabel = "Time Step", ylabel = "Control Value with Max {:.8f}".format(control_max))
ax2.set_title("SEIR Model Control with Total Cost {:.8f} and Constant {:.8f}".format(total_cost, cost))
ax2.legend()

print(np.real(forward_simulation_data[time_end-1,:]))
print(time_end)
# ax2.xaxis.set_inverted(True)
plt.show()
