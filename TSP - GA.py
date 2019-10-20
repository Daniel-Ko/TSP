from Graph import *
import random, operator
import numpy as np
from deap import algorithms, base, creator, tools
import matplotlib.pyplot as plt

nodelist = readTSP("a280.tsp")
weights = []

for node in nodelist:
    for other in nodelist:
        if node == other:
            continue
        weights.append(Edge(node, other).weight)

## Min.
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()


## permutation setup for individual,
toolbox.register(
    "indices", 
    np.random.permutation, 
    len(nodelist)
)

toolbox.register(
    "individual", 
    tools.initIterate, 
    creator.Individual, 
    toolbox.indices
)
## population setup,
toolbox.register(
    "population", 
    tools.initRepeat, 
    list, 
    toolbox.individual
)

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

def eval_tour(individual):
    path = []
    cost = 0
    for i, nodei in enumerate(individual[:-1]):
        path.append(Edge(nodelist[nodei], nodelist[individual[i+1]]))
        cost += path[-1].weight
    
    path.append(Edge(path[-1].n2, nodelist[individual[0]]))

    return (cost + path[-1].weight,)


toolbox.register("evaluate", eval_tour)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(n=100)


fit_stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
fit_stats.register('mean', np.mean)
fit_stats.register('min', np.min)

result, logbook = algorithms.eaSimple(
    pop, toolbox,
    cxpb=0.8, 
    mutpb=0.2,
    ngen=400, 
    verbose=False,
    stats=fit_stats
)

solution = tools.selBest(result, k=1)[0]
print(solution)
print('Cost of final tour solution: ', eval_tour(solution)[0])

plt.figure(figsize=(13, 5))

plots = plt.plot(logbook.select('min'),'c-', logbook.select('mean'), 'b-')
plt.legend(plots, ('Minimum fitness', 'Mean fitness'), frameon=True)
plt.ylabel('Cost'); plt.xlabel('Iterations');
plt.show()
