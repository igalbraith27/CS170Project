import networkx as nx
import random
import os
import math
path_to_outputs = "./outputs/"
path_to_inputs = "./all_inputs/"


def gen_graph(nodes, weight=0.5):
    g = nx.Graph()
    for i in range(nodes):
        g.add_node(str(i))
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
    s = gen_sets(g,sets)
    write_problem(g,nodes,sets,buses,bus_size,s)

def write_problem(g,nodes,num_sets,buses,bus_size,sets):
    p = path_to_inputs

    if nodes >= 25 and nodes <= 50 and num_sets <= 100:
        p += "small/"
    elif nodes >= 250 and nodes < 500 and num_sets <= 1000:
        p += "medium/"
    elif nodes >= 500 and nodes <= 1000 and num_sets <= 2000:
        p += "large/"
    else:
        p += "other/"

    graph_name = "{0}-{1}-{2}-{3}".format(nodes, buses, bus_size, num_sets)
    p += graph_name
    if not os.path.isdir(p):
        os.mkdir(p)
    nx.write_gml(g, p + "/graph.gml")
    f = open(p + "/parameters.txt", "w")
    f.write(str(buses) + "\n")
    f.write(str(bus_size) + "\n")
    for i in range(num_sets):
        f.write(str(sets[i]) + "\n")
    f.close()


def gen_solution(nodes, buses, bus_size):
    solution = []
    s = set(list(range(0,nodes-1)))
    for i in range(buses):
        student = random.randint(0, nodes-1)
        while student not in s:
            student = random.randint(0, nodes - 1)
        solution += [[student]]
        s.remove(student)
    while s:
        rand_bus = math.floor(random.random()*buses)
        if len(solution[rand_bus]) < bus_size:
            student = random.randint(0, nodes - 1)
            while student not in s:
                student = random.randint(0, nodes - 1)
            solution[rand_bus] += [student]
            s.remove(student)
    p = path_to_outputs

    if nodes >= 25 and nodes <= 50:
        p += "small"
    elif nodes >= 250 and nodes < 500:
        p += "medium"
    elif nodes >= 500 and nodes <= 1000:
        p += "large"
    else:
        p += "other"

    graph, sets = gen_problem_from_solution(solution, nodes, bus_size)

    input_name = "{0}-{1}-{2}-{3}".format(nodes, buses, bus_size, len(sets))

    output_file = open(p + "/" + input_name + ".out", "w")
    for i in range(len(solution)):
        output_file.write(str(solution[i]) + "\n")
    output_file.close()
    
    write_problem(graph, nodes, len(sets), buses, bus_size, sets)


def gen_problem_from_solution(solution, nodes, bus_size, sets=None, weight=0.5):
    print(solution)
    buses = len(solution)
    # Edge generation
    graph = nx.Graph()
    for i in range(nodes):
        graph.add_node(str(i))

    for i in range(len(solution)):
        for j in range(len(solution[i])-1):
            for k in range(j+1, len(solution[i])):
                graph.add_edge(solution[i][j], solution[i][k])
        if i < buses-1:
            graph.add_edge(solution[i][random.randint(0,len(solution[i])-1)], solution[i+1][random.randint(0,len(solution[i+1])-1)])

    # Rowdy set generation
    if not sets:
        sets = 2000 if nodes >= 500 else (1000 if nodes >= 250 else 100)
    rowdy_sets = []
    while len(rowdy_sets) != sets:
        bus1, bus2 = random.randint(0, len(solution)-1), random.randint(0, len(solution)-1)
        person1, person2 = random.randint(0, len(solution[bus1])), random.randint(0, len(solution[bus2]))
        rowdy_sets += [[person1, person2]]
        bus1, bus2 = random.randint(0, len(solution)-1), random.randint(0, len(solution)-1)
        person1, person2 = random.randint(0, len(solution[bus1])), random.randint(0, len(solution[bus2]))
        rowdy_sets += [[person1, person2]]
    return graph, rowdy_sets

# gen_problem(num_nodes, num_buses, bus_size, num_rowdy_sets, [OPTIONAL]edge_likelihood)
# gen_problem(15, 3, 7, 2, 0.1)

#gen_problem(num_nodes, num_buses, bus_size, num_rowdy_sets, [OPTIONAL]edge_likelihood)
#gen_problem(500, 50, 15, 10, 0.001)


gen_solution(10, 4, 4)



