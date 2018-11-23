from __future__ import print_function
import random
from simanneal import Annealer
import copy


"""The annealer class for our NP Complete Problem for CS170. """


class SimSolver(Annealer):
    def __init__(self, state, constraints, num_buses, size_bus, graph):
        """The constructor for our annealer.

        Keyword arguments:
        state -- should be a list of lists describing assignment of people to buses.
        constraints -- should be a list of lists describing invalid groups.
        num_buses -- should be the integer k buses we have.
        size_bus -- should be the integer t size of the buses.
        graph -- the instance of our problem as a networkX graph.
        """
        self.constraints = constraints
        self.num_buses = num_buses
        self.size_bus = size_bus
        self.graph = graph
        self.change = 0
        self.current_energy = None
        super(SimSolver, self).__init__(state)
        self.rowdy = self.get_rowdy()


    def get_rowdy(self):
        rowdy_groups = []
        constraints = self.constraints
        for bus in self.state:
            for rowdy in constraints:
                intersection = list(set(rowdy) & set(bus))
                if intersection == rowdy:
                    rowdy_groups.append(rowdy)
                    constraints.remove(rowdy) 
        return rowdy_groups
        
    def move(self):
        """Swaps two people on two random buses."""
        def find_random_people():
            bus1 = random.randint(0, len(self.state) - 1)
            bus2 = random.randint(0, len(self.state) - 1)
            while bus2 == bus1:
                bus2 = random.randint(0, len(self.state) - 1)
            person1 = random.randint(0, len(self.state[bus1]) - 1)
            person2 = random.randint(0, len(self.state[bus2]) - 1)
            return bus1, bus2, person1, person2
        """oldfriendcount = 0
        newfriendcount = 0
        p1 = self.state[bus1][person1]

        if p1:
            friends1 = self.graph.neighbors(p1)
            for person in self.state[bus1]:
                if person in friends1:
                    oldfriendcount +=1
        p2 = self.state[bus2][person2]
        if p2:
            friends2 = self.graph.neighbors(p2)
            for person in self.state[bus2]:
                if person in friends2:
                    oldfriendcount +=1"""
        
        bus1, bus2, person1, person2 = find_random_people()
        stateCopy = copy.deepcopy(self.state)
        stateCopy[bus1][person1], stateCopy[bus2][person2] = stateCopy[bus2][person2], stateCopy[bus1][person1]
        
        while self.check_if_empty(stateCopy):
            print("Detected empty bus. Fixing...")
            stateCopy = copy.deepcopy(self.state)
            bus1, bus2, person1, person2 = find_random_people()
            stateCopy = copy.deepcopy(self.state)
            stateCopy[bus1][person1], stateCopy[bus2][person2] = stateCopy[bus2][person2], stateCopy[bus1][person1]
        
        self.state = stateCopy

        """p1 = self.state[bus1][person1]
        if p1:
            friends1 = self.graph.neighbors(p1)
            for person in self.state[bus1]:
                if person in friends1:
                    newfriendcount +=1
        p2 = self.state[bus2][person2]
        if p2:
            friends2 = self.graph.neighbors(p2)
            for person in self.state[bus2]:
                if person in friends2:
                    newfriendcount +=1"""
        
        #self.change =  newfriendcount - oldfriendcount

    def check_if_empty(self, tempState):
        for i in range(len(tempState)):
            if len(tempState[i]) <= 0:
                return True
        return False

    def energy(self):
        """Calculates the score of a given state."""

        def check_correctness():

            # Ensuring we use correct number of buses. Should never be a problem.
            if len(self.state) != self.num_buses:
                raise ValueError("State has incorrect number of buses. State buses = {}, number of buses should be {}.".format(len(self.state),self.num_buses))
            # Making sure no bus is empty or above capacity.
            for i in range(len(self.state)):
                if len(self.state[i]) > self.size_bus:
                    raise ValueError("Bus(es) over capacity. Current state: " + str(self.state))
                if len(self.state[i]) <= 0:
                    raise ValueError("Bus(es) empty. Current state: " + str(self.state))
        
        # Making sure no bus is empty
        for i in range(len(self.state)):
            newState = []
            newState = [x for x in self.state[i] if x is not None]
            if len(newState) <= 0:
                return 1000000

        #check_correctness()
        bus_assignments = {}

        # Make sure each student is in exactly one bus
        attendance = {student: False for student in self.graph.nodes()}
        for i in range(len(self.state)):
            # Checking if all students exist.
            # FIXME: ERROR HERE
            if not all([student in self.graph for student in self.state[i]]):
                if self.state[i] == None:
                    continue
                # return -1
            for student in self.state[i]:
                #Check if a student appears more than once
                #if attendance[student] == True:
                 #   print(self.state[i])
                   # return -1

                attendance[student] = True
                bus_assignments[student] = i

        # make sure each student is accounted for
        # if not all(attendance.values()):
          #  return -1
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
        score = 1 - score
        score *= 100
        # print(score)
        #if score == 0:
            #raise ValueError('A very specific bad thing happened.')
        if self.current_energy != None:
            alt_score = self.new_energy()
            print(score == alt_score)
        self.current_energy = score
        return score

    def new_energy(self):
        if self.change == 0:
            return self.current_energy
        
        old = self.current_energy
        total_friendships = self.graph.number_of_edges()
        delta = self.change
        self.change = 0
        new_rowdy = self.get_rowdy()
        if self.rowdy != new_rowdy:
            add_edges = 0
            for rowdy in self.rowdy:
                for student in rowdy:
                    friends = self.graph.neighbors(student)
                    bus = -1
                    for b in self.state:
                       if student in b:
                           bus = b 
                           break
                    add_edges += len(list(set(friends) & set(self.state[bus]))) 
            remove_edges = 0
            for rowdy in new_rowdy:
                for student in rowdy:
                    friends = self.graph.neighbors(student)
                    bus = -1
                    for b in self.state:
                        if student in b:
                            bus = b 
                            break
                    remove_edges += len(list(set(friends) & set(self.state[bus]))) 

            self.rowdy = new_rowdy
            return old + delta/total_friendships + add_edges/total_friendships - remove_edges/total_friendships

        return old + delta/total_friendships

