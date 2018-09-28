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
    sa = anneal.SimAnneal(graph, T=250000, stopping_iter = 100000)
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
    newBs = [None]*5
    for w in range(5):
        for x in range(5):
            my_ids = [idx for idx, val in bs.bs]
            if (my_ids[x] == w):
                newBs[w] = bs.bs[x]
    newBs = [x[1] for x in newBs]           
    print("Best solutions ordered: ", newBs)
    
    #Plot each path
    coordsX = [[] for i in range(5)]
    coordsY = [[] for i in range(5)]
    weights = [0 for i in range(5)]
    colors = ["red", "blue", "green", "yellow", "orange"]
    for i in range(len(graphs)):
        for j in range(len(graphs[i].vert_dict)):
            v = graphs[i].get_vertex(newBs[i][j])
            coordsX[i].append(v.lon)
            coordsY[i].append(v.lat)
            if(j != (len(graphs[i].vert_dict) - 1)):
                weights[i] += v.get_weight(graphs[i].get_vertex(j+1))
        
        plt.scatter(coordsY[i], coordsX[i], color=colors[i])
        plt.plot(coordsY[i], coordsX[i], color=colors[i])

    for i in range(len(weights)):
        print(weights[i] * 100)
    plt.scatter(-103.4158208, 20.708207, color = "black")
    plt.scatter(-103.399223, 20.771859, color = "purple")
    plt.scatter(-103.281663, 20.703316, color = "purple")
    plt.scatter(-103.247455, 20.620652, color = "purple")
    plt.scatter(-103.313528, 20.573827, color = "purple")
    plt.scatter(-103.485171, 20.513207, color = "purple")
    plt.show()
    
if __name__ == "__main__":
    main()


