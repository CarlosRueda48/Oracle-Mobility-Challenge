import anneal
import matplotlib.pyplot as plt
import random
import cluster
import time

coords = []
with open('coord.txt','r') as f:
    i = 0
    for line in f.readlines():
        line = [float(x.replace('\n','')) for x in line.split(' ')]
        coords.append([])
        for j in range(1,3):
            coords[i].append(line[j])
        i += 1


if __name__ == '__main__':
    graphs = cluster.getGraphs(5)
    optimizedPaths = []
    start_time = time.process_time()
    for i in range (len(graphs)):
        print("Finding optimized path for graph", i)
        sa = anneal.SimAnneal(graphs[i], T=25000, stopping_iter = 100000)
        sa.anneal()
        optimizedPaths.append(sa.best_solution)
    print(optimizedPaths)
    print("Annealing took %s seconds." % (time.process_time() - start_time))
