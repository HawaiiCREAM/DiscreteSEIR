from Simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

input_state = [1.07000172e-01, 8.93135541e-03, 6.40945233e-03, 8.77659020e-01]
input_costate = [0, 0, 0, 0]
[beta, sigma, gamma] = [0.5, 0.1, 0.2]
cost = 1
control_max = 0.05
max_time = 100

simulation = Simulation(input_state, input_costate, beta, sigma, gamma, cost, control_max)

backwards_simulation_data = np.zeros((max_time, 4))
backwards_simulation_pdata = np.zeros((max_time, 4))
backwards_simulation_control_data = np.zeros(max_time)
backwards_simulation_switching_data = np.zeros(max_time)
backwards_simulation_data[0,:] = input_state
backwards_simulation_pdata[0,:] = input_costate
backwards_simulation_control_data[0] = 0
backwards_simulation_switching_data[0] = simulation.return_switching()

for i in range(1,3):
    # diff = np.subtract(simulation.return_state(), simulation.return_forward_state(simulation.return_backwards_state()))
    # print("difference of calc {}".format(diff))
    simulation.update_state(simulation.return_backwards_state())
    simulation.update_costate(simulation.return_backwards_costate())
    backwards_simulation_data[i,:] = simulation.return_state()
    backwards_simulation_pdata[i,:] = simulation.return_costate()
    backwards_simulation_control_data[i] = simulation.control
    backwards_simulation_switching_data[i] = simulation.return_switching()
for i in range(3,max_time):
    simulation.update_control()
    simulation.update_state(simulation.return_backwards_state())
    simulation.update_costate(simulation.return_backwards_costate())
    backwards_simulation_data[i,:] = simulation.return_state()
    backwards_simulation_pdata[i,:] = simulation.return_costate()
    backwards_simulation_control_data[i] = simulation.control
    backwards_simulation_switching_data[i] = simulation.return_switching()

def first_bad(list):
    count = 0
    for number in list:
        count += 1      #moved it outside of the if
        if number < 0 or number > 1:
            return count

time_end = min(first_bad(backwards_simulation_data[:,1]), first_bad(backwards_simulation_data[:,2]))-1

total_cost = sum(backwards_simulation_data[:time_end, 2]) + sum(backwards_simulation_control_data[:time_end]*cost)
# print(backwards_simulation_data[:time_end, 2])

x_axis = range(0,time_end)[::-1]

plt.show()
