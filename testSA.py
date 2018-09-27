import anneal
import matplotlib.pyplot as plt
import random
import cluster

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
    #coords = [[round(random.uniform(-1000,1000),4),round(random.uniform(-1000,1000),4)] for i in range(100)]
    graphs = cluster.getGraphs(5)
    print(graphs[0])
    sa = anneal.SimAnneal(graphs[0], stopping_iter = 5000)
    sa.anneal()
    (print(sa.best_solution))