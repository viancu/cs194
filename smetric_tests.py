### A set of sanity checks for the functions implemented in smetric.py

import helpers
import wbr_sim
import smetric
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

test_graph = {0: [2], 1: [2], 2: [0, 1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}
def test_degree_seq():
    correct = [3, 2, 2, 1, 1, 1]
    ds = smetric.deg_seq(test_graph)
    if ds == correct:
        print("degree sequence works")
    else:
        print("degree sequence does not work")

def test_smetric():
    correct = 18
    sm = smetric.s_metric(test_graph)
    if sm == correct:
        print("s_metric works")
    else:
        print("s_metric does not work")

def test_smax(graph):
    max = smetric.s_max(smetric.deg_seq(graph))
    if smetric.deg_seq(graph) != smetric.deg_seq(max):
        print("s_max graph has different degree sequence than input")
        return
    if smetric.s_metric(max) < smetric.s_metric(graph):
        print("s_max graph has lower s_metric than input")
        return
    print("s_max works")

def smetric_simulation(num_players, num_trials, strategy_functions, strategy_choices, alpha_function, random_walk=False):
    """
    Returns the mean and standard deviation of the scale-free metric of graphs generated by the wbr simulation
    """
    scale_free = []
    smetrics = []
    for i in range(num_trials):
        graph = wbr_sim.run_simulation(num_players, strategy_functions, strategy_choices,  alpha_function, random_walk)
        scale_free.append(smetric.scale_free(graph))
        smetrics.append(smetric.s_metric(graph))
    return np.mean(scale_free), np.std(scale_free), np.mean(smetrics), np.std(smetrics)


# unit tests
test_degree_seq()
test_smetric()
test_smax(test_graph)

# simulations
uniform = smetric_simulation(100, 100,
 [helpers.uniform_strategy], [0 for i in range(100)],
 lambda x, y: 0)

PA = smetric_simulation(100, 100,
 [helpers.PA_strategy], [0 for i in range(100)],
 lambda x, y: 0)

print("uniform strategy s_metric mean: " + str(uniform[2]) + " standard deviation: " + str(uniform[3]))
print("uniform strategy scale-free mean: " + str(uniform[0]) + " standard deviation: " + str(uniform[1]))
print("PA strategy s_metric mean: " + str(PA[2]) + " standard deviation: " + str(PA[3]))
print("PA strategy scalefreec mean: " + str(PA[0]) + " standard deviation: " + str(PA[1]))

# example networks
uniform_network = wbr_sim.run_simulation(100,
 [helpers.uniform_strategy], [0 for i in range(100)],
 lambda x, y: 1)

uniform_max = smetric.s_max(smetric.deg_seq(uniform_network))

plt.title("Uniform Random Choice Simulation Graph")
nx.draw_kamada_kawai(nx.Graph(uniform_network), node_size=100)
plt.savefig('URC_sim.png')
plt.show()

plt.title("Uniform Random Choice S_max Graph")
nx.draw_kamada_kawai(nx.Graph(uniform_max), node_size=100)
plt.savefig('URC_Smax.png')
plt.show()

print("Uniform Random Choice strategy:")
print(smetric.deg_seq(uniform_network))
print(smetric.s_metric(uniform_network))
print(smetric.scale_free(uniform_network))

PA_network = wbr_sim.run_simulation(100,
 [helpers.PA_strategy], [0 for i in range(100)],
 lambda x, y: 1)

PA_max = smetric.s_max(smetric.deg_seq(PA_network))

plt.title("PA Simulation Graph")
nx.draw_kamada_kawai(nx.Graph(PA_network), node_size=100)
plt.savefig('PA_sim.png')
plt.show()

plt.title("PA S_max Graph")
nx.draw_kamada_kawai(nx.Graph(PA_max), node_size=100)
plt.savefig('PA_Smax.png')
plt.show()

print("Preferential Attatchment strategy:")
print(smetric.deg_seq(PA_network))
print(smetric.s_metric(PA_network))
print(smetric.scale_free(PA_network))
