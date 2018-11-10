import networkx as nx
import random
import os
import math


def gen_graph(nodes, weight=0.5):
    g = nx.Graph()
    for i in range(nodes):
        g.add_node(i)
    for i in range(nodes):
        for j in range(i, nodes):
            if i != j and random.random() > (1-weight):
                g.add_edge(i, j)
                print((i, j))
    return g


def gen_sets(g, numSets):
    rv = []
    n = list(g.nodes)
    for i in range(numSets):
        size = min(len(n)-1, math.floor(random.expovariate(10)*(len(n)-1) + 2))
        print("Size: {}".format(size))
        lst = []
        seen = set()
        for j in range(size):
            idx = math.floor(random.random()*(len(n)-1))
            while idx in seen:
                idx = math.floor(random.random() * (len(n) - 1))
            lst += [n[idx]]
            seen.add(idx)
        rv += [lst]
    return rv


def gen_problem(nodes, buses, bus_size, sets, weight=0.5):

    g = gen_graph(nodes, weight)
    p = "./all_inputs/"

    if nodes >= 25 and nodes <= 50 and sets <= 100:
        p += "small/"
    elif nodes >= 250 and nodes < 500 and sets <= 1000:
        p += "medium/"
    elif nodes >= 500 and nodes <= 1000 and sets <= 2000:
        p += "large/"
    else:
        p += "other/"

    graph_name = "{0}-{1}-{2}-{3}".format(nodes, buses, bus_size, sets)
    p += graph_name
    if not os.path.isdir(p):
        os.mkdir(p)
    nx.write_gml(g, p + "/graph.gml")
    f = open( p + "/parameters.txt", "w")
    f.write(str(buses) + "\n")
    f.write(str(bus_size)+ "\n")
    s = gen_sets(g, sets)
    for i in range(sets):
        f.write(str(s[i])+ "\n")
    f.close()

#gen_problem(num_nodes, num_buses, bus_size, num_rowdy_sets, [OPTIONAL]edge_likelihood)
gen_problem(500, 50, 15, 10, 0.001)


