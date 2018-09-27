from functools import partial
import os, time, multiprocessing, anneal,cluster



def f(graph):
    sa = anneal.SimAnneal(graph, T=1000, stopping_iter = 5000)
    sa.anneal()
    return sa.best_solution

def main():
    graphs = cluster.getGraphs(5)
    start = time.process_time()
    pool = multiprocessing.Pool()
    func = partial(f)
    pool.map(func, graphs)
    pool.close()
    pool.join()
    print("Time taken = {0:.5f}".format(time.process_time() - start))

if __name__ == "__main__":
    main()
    
