from __future__ import print_function
import random
from simanneal import Annealer

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

    def move(self):
        """Swaps two people on two random buses."""
        bus1 = random.randint(0, len(self.state) - 1)
        bus2 = random.randint(0, len(self.state) - 1)
        person1 = random.randint(0, len(self.state[bus1]) - 1)
        person2 = random.randint(0, len(self.state[bus2]) - 1)
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
        self.state[bus1][person1], self.state[bus2][person2] = self.state[bus2][person2], self.state[bus1][person1]
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
        
        #self.change = oldfriendcount - newfriendcount


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
        """if self.current_energy:
            net_change = (self.current_energy - score)*self.graph.number_of_edges()
            print(net_change)
        if self.current_energy != None:
            alt_score = self.new_energy()
            print(score == alt_score)
        self.current_energy = score"""
        return score

    def new_energy(self):
        if self.change == 0:
            return self.current_energy
        
        o = self.current_energy
        total_friendships = self.graph.number_of_edges()
        c = self.change
        self.change = 0
        return o + c/total_friendships

