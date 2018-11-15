from solver import parse_input
import sys
import networkx as nx

def main(input_folder):
    graph, num_buses, size_bus, constraints = parse_input(input_folder)

    print("Number of nodes:")
    print("\t", nx.number_of_nodes(graph))
    print("Constraints:")
    for constraint in constraints:
        print("\t",constraint)    
    print("Bus Size:")
    print("\t", size_bus)
    print("Num Buses:")
    print("\t", num_buses)
    print("Edges:")
    for edge in graph.edges():
        print("\t", edge)



if __name__ == '__main__':
    main(sys.argv[1])


