import time, threading, anneal, cluster, operator
import matplotlib.pyplot as plt

class best_Solutions(object):

    def __init__(self, bs = []):
        self.lock = threading.Lock()
        self.bs = bs
    def add(self, solution, i):
        #print('Waiting for a lock')
        self.lock.acquire()
        try:
            #print('Acquired a lock')
            self.bs.append([i,solution])
        finally:
            #print('Released a lock')
            self.lock.release()

def worker(graph, bs, ident):
    sa = anneal.SimAnneal(graph, T=1000, stopping_iter = 5000)
    sa.anneal()
    bs.add(sa.best_solution, ident)

def main():

    bs = best_Solutions()
    graphs = cluster.getGraphs(5)
    start = time.process_time()
    for i in range(5):
        t = threading.Thread(target=worker, args=(graphs[i],bs, i))
        t.start()

    #print('Waiting for worker threads')
    master_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not master_thread:
            t.join()

    print("Time taken = {0:.5f}".format(time.process_time() - start))
    print("Best solutions: ", bs.bs)
    newBs = [None]*5
    for w in range(5):
        for x in range(5):
            my_ids = [idx for idx, val in bs.bs]
            if (my_ids[x] == w):
                newBs[w] = bs.bs[x]
    newBs = [x[1] for x in newBs]           
    print("Best solutions ordered: ", newBs)
    
    coordsX = [[] for i in range(5)]
    coordsY = [[] for i in range(5)]
    weights = [0 for i in range(5)]

    for i in range(len(graphs)):
        for j in range(len(graphs[i].vert_dict)):
            v = graphs[i].get_vertex(j)
            coordsX[i].append(v.lon)
            coordsY[i].append(v.lat)
            if(j != (len(graphs[i].vert_dict) - 1)):
                weights[i] += v.get_weight(graphs[i].get_vertex(j+1))
        
        plt.scatter(coordsY[i], coordsX[i])
        plt.plot(coordsY[i], coordsX[i])

    print(weights)
    plt.show()
    
if __name__ == "__main__":
    main()


