from Simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial



input_state = [1.07000172e-01, 8.93135541e-03, 6.40945233e-03, 8.77659020e-01]
input_costate = [0, 0, 0, 0]
[beta, sigma, gamma] = [0.5, 0.1, 0.2]
cost = 1
control_max = 0.05
max_time = 56 # not passed to sim

def RunBackwardsSimulation(input_state, input_costate, beta, sigma, gamma, cost, control_max, max_time):
    simulation = Simulation(input_state, input_costate, beta, sigma, gamma, cost, control_max)
    def first_bad(list):
        count = 0
        for number in list:
            count += 1      #moved it outside of the if
            if number < 0 or number > 1:
                return count
        return max_time

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
    time_end = min(
        first_bad(backwards_simulation_data[:,0]),
        first_bad(backwards_simulation_data[:,1]),
        first_bad(backwards_simulation_data[:,2]),
        first_bad(backwards_simulation_data[:,3])
        ) - 1
    total_cost = sum(backwards_simulation_data[:time_end, 2]) + sum(backwards_simulation_control_data[:time_end]*cost)

    x_axis = range(0,time_end)[::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 6))
    ax1.plot(x_axis, backwards_simulation_data[:time_end,0], '.', label ='S')
    ax1.plot(x_axis, backwards_simulation_data[:time_end,1], '.', label ='E')
    ax1.plot(x_axis, backwards_simulation_data[:time_end,2], '.', label ='I')
    ax1.plot(x_axis, backwards_simulation_data[:time_end,3], '.', label ='R')
    ax1.set(xlabel = "Time Step", ylabel = "Ratio of Population")
    ax1.set_ylim([0, 1])
    ax1.set_title("SEIR Model")
    ax1.legend(loc = 'upper left')
    # ax1.xaxis.set_inverted(True)

    ax2.plot(x_axis, backwards_simulation_control_data[:time_end], '.', label = 'u')
    ax2.set(xlabel = "Time Step", ylabel = "Control Value with Max {:.8f}".format(control_max))
    ax2.set_ylim([-0.01, 0.06])
    ax2.set_title("Control with Total Cost {:.8f} and Cost Constant {:.8f}".format(total_cost, cost))
    ax2.legend(loc = 'upper right')

    plt.figure()
    plt.plot(x_axis, backwards_simulation_switching_data[:time_end], '.', label = 'SwitchingFunc')
    plt.xlabel("Time Step")
    plt.ylabel("Switching Function Value")
    plt.title("Switching Function with Cost Constant {:.8f}".format(cost))
    plt.legend(loc = 'upper right')

    fig.savefig('{}_cost_1.png'.format(cost))
    plt.savefig('{}_cost_2.png'.format(cost))
    plt.close()
    return [
        np.real(backwards_simulation_data[time_end-1,:]), # initial
        np.real(backwards_simulation_data[0,:]), # final
        cost, # b
        time_end - 1, # N
        total_cost, # total cost
        backwards_simulation_switching_data[:time_end] # switching data
    ]

sample = np.arange(start = 0, stop = 5.5, step = 0.5)
for i in sample:
    results = RunBackwardsSimulation(input_state, input_costate, beta, sigma, gamma, i, control_max, max_time)
    file_object = open(r'.\{}_cost_data.txt'.format(i), 'w')
    file_object.write('{}\n'.format(results[0]))
    file_object.write('{}\n'.format(results[1]))
    file_object.write('{}\n'.format(results[2]))
    file_object.write('{}\n'.format(results[3]))
    file_object.write('{}\n'.format(results[4]))
    file_object.close()
