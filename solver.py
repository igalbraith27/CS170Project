import networkx as nx
import os
from sim_solver import SimSolver
import random

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def solve(graph, num_buses, size_bus, constraints):

    # This should be an initial greedy strategy that constructs a starting state for the annealer.
    output = []
    for x in range(num_buses):
        output.append([None])
    names = list(graph.nodes)
    names_set = set(graph.nodes)
    print(names)

    # initial state, a randomly-ordered bunch of people on the bus
    while names_set:
        for i in range(len(output)):
            if names_set:
                name = random.sample(names_set, 1)[0]
                output[i].append(name)
                names_set.remove(name)
                if len(output[i]) == 2:
                    output[i] = [x for x in output[i] if x is not None]
            else:
                break

    '''
    for i in range(num_buses):
        bus = []
        for s in range(size_bus):
            if size_bus*i + s < len(names):
                bus += names[size_bus*i + s]
        output += [bus]
    '''
    print(names)
    tsp = SimSolver(output, constraints, num_buses, size_bus, graph)
    tsp.steps = 100000
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    print()
    print("%i score:" % e)
    for lst in state:
        print("\t", lst)
    return state



def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder) 
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file

            for i in range(len(solution)):
                output_file.write(str(solution[i]))

            output_file.close()


if __name__ == '__main__':
    main()


