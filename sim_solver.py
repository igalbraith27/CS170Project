from __future__ import print_function
import random
from simanneal import Annealer

"""The annealer class for our NP Complete Problem for CS170. """


class SimSolver(Annealer):
    def __init__(self, state, adjacency_matrix, constraints, num_buses, size_bus, graph):
        """The constructor for our annealer.

        Keyword arguments:
        state -- should be a list of lists describing assignment of people to buses.
        adjacency_matrix -- should be a completed adjacency matrix given set-up.
        constraints -- should be a list of lists describing invalid groups.
        num_buses -- should be the integer k buses we have.
        size_bus -- should be the integer t size of the buses.
        graph -- the instance of our problem as a networkX graph.
        """
        self.adjacency_matrix = adjacency_matrix
        self.constraints = constraints
        self.num_buses = num_buses
        self.size_bus = size_bus
        self.graph = graph
        super(SimSolver, self).__init__(state)

    def move(self):
        """Swaps two people on two random buses."""
        bus1 = random.randint(0, len(self.state) - 1)
        bus2 = random.randint(0, len(self.state) - 1)
        person1 = random.randint(0, len(self.state[bus1]) - 1)
        person2 = random.randint(0, len(self.state[bus2]) - 1)
        self.state[person1], self.state[person2] = self.state[person2], self.state[person1]

    def energy(self):
        """Calculates the score of a given state."""

        # Ensuring we use correct number of buses. Should never be a problem.
        if len(self.state) != self.num_buses:
            return -1

        # Making sure no bus is empty or above capacity.
        for i in range(len(self.state)):
            if len(self.state[i]) > self.size_bus:
                return -1
            if len(self.state[i]) <= 0:
                return -1

        bus_assignments = {}

        # make sure each student is in exactly one bus
        attendance = {student: False for student in self.graph.nodes()}
        for i in range(len(self.state)):
            # Checking if all students exist.
            if not all([student in self.graph for student in self.state[i]]):
                return -1
            for student in self.state[i]:
                # if a student appears more than once
                if attendance[student] == True:
                    print(self.state[i])
                    return -1

                attendance[student] = True
                bus_assignments[student] = i

        # make sure each student is accounted for
        if not all(attendance.values()):
            return -1
        total_edges = self.graph.number_of_edges()
        graph_copy = self.graph.copy()
        # Remove nodes for rowdy groups which were not broken up
        for i in range(len(self.constraints)):
            busses = set()
            for student in self.constraints[i]:
                busses.add(bus_assignments[student])
            if len(busses) <= 1:
                for student in self.constraints[i]:
                    if student in graph_copy:
                        graph_copy.remove_node(student)

        # score output
        score = 0
        for edge in graph_copy.edges():
            if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
                score += 1
        score = score / total_edges
        return score


if __name__ == '__main__':

    # latitude and longitude for the twenty largest U.S. cities
    cities = {
        'New York City': (40.72, 74.00),
        'Los Angeles': (34.05, 118.25),
        'Chicago': (41.88, 87.63),
        'Houston': (29.77, 95.38),
        'Phoenix': (33.45, 112.07),
        'Philadelphia': (39.95, 75.17),
        'San Antonio': (29.53, 98.47),
        'Dallas': (32.78, 96.80),
        'San Diego': (32.78, 117.15),
        'San Jose': (37.30, 121.87),
        'Detroit': (42.33, 83.05),
        'San Francisco': (37.78, 122.42),
        'Jacksonville': (30.32, 81.70),
        'Indianapolis': (39.78, 86.15),
        'Austin': (30.27, 97.77),
        'Columbus': (39.98, 82.98),
        'Fort Worth': (32.75, 97.33),
        'Charlotte': (35.23, 80.85),
        'Memphis': (35.12, 89.97),
        'Baltimore': (39.28, 76.62)
    }

    # initial state, a randomly-ordered itinerary
    init_state = list(cities.keys())
    random.shuffle(init_state)

    # create a distance matrix
    distance_matrix = {}
    for ka, va in cities.items():
        distance_matrix[ka] = {}
        for kb, vb in cities.items():
            if kb == ka:
                distance_matrix[ka][kb] = 0.0
            else:
                pass
                #distance_matrix[ka][kb] = distance(va, vb)

    tsp = SimSolver(init_state, distance_matrix)
    tsp.steps = 100000
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    while state[0] != 'New York City':
        state = state[1:] + state[:1]  # rotate NYC to start

    print()
    print("%i mile route:" % e)
    for city in state:
        print("\t", city)
