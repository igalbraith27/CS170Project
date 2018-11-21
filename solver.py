import networkx as nx
import os
import sys
from sim_solver import SimSolver
import random
from output_scorer import get_score, score_output
from myfolder import folder

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
my_outputs = "./" + folder
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
    difficulty = nx.number_of_nodes(graph) + len(constraints)
    #print("Difficulty: {}".format(difficulty))
    # This should be an initial greedy strategy that constructs a starting state for the annealer.
    output = []
    for x in range(num_buses):
        output.append([None])
    names = list(graph.nodes)
    names_set = set(graph.nodes)

    # initial state, a randomly-ordered bunch of people on the bus
    def initialize_randomly():
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

    def weak_greedy():
        """Loops through buses, placing together a randomly chosen student
        and as many of their friends as possible. """
        available_buses = list(range(num_buses))
        while names_set:
            for i in available_buses:
                if len(output[i]) == size_bus:
                    available_buses.remove(i)
                    break
                elif not names_set:
                    break
                student = random.sample(names_set, 1)[0]
                friends = list(graph.adj[student])
                output[i].append(student)
                names_set.remove(student)
                if len(output[i]) == 2:
                    output[i] = [x for x in output[i] if x is not None]
                for friend in friends:
                    if len(output[i]) == size_bus:
                        available_buses.remove(i)
                        break
                    if friend in names_set:
                        output[i].append(friend)
                        names_set.remove(friend)

    weak_greedy()

    for i in range(len(output)):
        while len(output[i]) < size_bus:
            output[i].append(None)
        if len(output[i]) > size_bus:
            raise ValueError("We got too big")

    '''
    for i in range(num_buses):
        bus = []
        for s in range(size_bus):
            if size_bus*i + s < len(names):
                bus += names[size_bus*i + s]
        output += [bus]
    '''
    '''
    print("Constraints:")
    print("\t", constraints)
    print("Bus Size:")
    print("\t", size_bus)
    print("Num Buses:")
    print("\t", num_buses)
    print("Edges:")
    for edge in graph.edges():
        print("\t", edge)
    print("Bad input:")

    for lst in output:
        print("\t", lst)
    '''
    tsp = SimSolver(output, constraints, num_buses, size_bus, graph)
    #auto_schedule = tsp.auto(minutes=0.5)
    tsp.Tmax = 5
    tsp.Tmin = 0.001
    tsp.steps = 2000
    tsp.updates = 500

    #tsp.set_schedule(auto_schedule)
    #print("Tmax: {}".format(tsp.Tmax))
    #print("Tmin: {}".format(tsp.Tmin))
    #print("Steps: {}".format(tsp.steps))
    #print("Updates: {}".format(tsp.updates))

    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "deepcopy"
    state, e = tsp.anneal()

    
    for i in range(len(state)):
        state[i] = [x for x in state[i] if x is not None]
    #print()
    #print("%f score:" % e)
    #for lst in state:
        #print("\t", lst)
    return state



def main(folders=["small", "medium", "large"], graphName = None):
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = folders
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        #If the user is not specifying a particular graph to run on
        if not graphName:
            folders = os.listdir(category_dir)
        else:
            folders = [graphName]
        
        #Shuffles input folders so they don't run in order
        random.shuffle(folders)
        num_left = len(folders)
        count = 1
        old_scores = 0
        new_scores = 0
        for input_folder in folders:
            print("="*80)
            input_name = os.fsdecode(input_folder) 
            inputfoldername = (category_path + "/" + input_name)
            outputfoldername = output_category_path + "/" + input_name + ".out"

            # The next line ensures that the solver only solves the graphs that haven't yet been solved. We'll need to take it out once we have solved everything. 
            # if not os.path.isfile(outputfoldername):
            if not False:
                graph, num_buses, size_bus, constraints = parse_input(inputfoldername)
                print("Solving {} ({}/{})".format(input_name, count, num_left))
                solution = solve(graph, num_buses, size_bus, constraints)
                sol_score1 = get_score(graph, constraints, num_buses, size_bus, solution)
                sol_score = 1 - sol_score1[0]
                if sol_score >= 0:
                    if os.path.isfile(outputfoldername):
                        prev_score = 1 - score_output(inputfoldername, outputfoldername)[0]
                    else:
                        prev_score = 1
                    old_scores += prev_score
                    new_scores += sol_score
                    prev_score = prev_score if prev_score > 0 else 0.000000001
                    improvement = ((prev_score - sol_score)/prev_score)*100
                    print("Old score: {0:.2f}".format(prev_score).ljust(19) + "|".ljust(3) + "New score: {0:.2f}".format(sol_score).ljust(19) + "|".ljust(3) + "Improvement: {0:.2f}%".format(improvement).ljust(15))
                    print(sol_score1[1])
                    if improvement > 0:
                        writelocation = my_outputs + "/" + size + "/" + input_name + ".out"
                        output_file = open(writelocation, "w")     
                        for i in range(len(solution)):
                            output_file.write(str(solution[i]) + "\n")

                        output_file.close()
                else:
                    print(sol_score1[1])
                count +=1
        old_scores = old_scores if old_scores > 0 else 0.00000001
        print("-"*80)
        print("Total improvement this batch: {}%".format(((old_scores - new_scores)/old_scores)*100))
        print("-"*80)

            


if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 1:
        main()
    elif len_args == 2:
        main([sys.argv[1]])
    elif len_args == 3:
        main([sys.argv[1]], sys.argv[2])
    else:
        raise ValueError("Bad input format.")


