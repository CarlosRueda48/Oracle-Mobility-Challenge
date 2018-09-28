from functools import partial
import os, time, multiprocessing, anneal,cluster

def f(graph):
    sa = anneal.SimAnneal(graph, T=1000, stopping_iter = 5000)
    sa.anneal()
    return sa.best_solution

def main():
    graphs = cluster.getGraphs(5)
    start = time.process_time()
    manager = multiprocessing.Manager()
    L = manager.list(5)
    solutions = []
    for i in range(5):
        p = multiprocessing.Process(target=f, args=(graphs))
        p.start()
        solutions.append(p)
    for s in solutions:
        p.join()
    print("Time taken to anneal = {0:.5f}".format(time.process_time() - start))

if __name__ == "__main__":
    main()
    
