from Graph import *
from simanneal import Annealer
import random

class TSP(Annealer):
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TSP, self).__init__(state)  

    def move(self):
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy()

    def energy(self):
        cost = 0
        for i, _ in enumerate(self.state[:-1]):
            cost += Edge(self.state[i], self.state[i+1]).weight
        
        return cost + Edge(self.state[-1], self.state[0]).weight


if __name__ == "__main__":
    nodelist = readTSP("a280.tsp")

    random.shuffle(nodelist)

     # create a distance matrix as in examples on the module repo
    distance_matrix = {}
    for node in nodelist:
        distance_matrix[node.id] = {}
        for node2 in nodelist:
            distance_matrix[node.id][node2.id] = Edge(node, node2).weight

    annealer = TSP(nodelist, distance_matrix)
    annealer.set_schedule(annealer.auto(minutes=0.2))

    annealer.copy_strategy = "slice"
    state, cost = annealer.anneal()

    print(state)
    print(cost)
