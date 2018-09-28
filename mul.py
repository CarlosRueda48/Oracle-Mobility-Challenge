import time, threading, anneal, cluster

class best_Solutions(object):

    def __init__(self, bs = []):
        self.lock = threading.Lock()
        self.bs = bs
    def add(self, solution):
        #print('Waiting for a lock')
        self.lock.acquire()
        try:
            #print('Acquired a lock')
            self.bs.append(solution)
        finally:
            #print('Released a lock')
            self.lock.release()

def worker(graph, bs):
    sa = anneal.SimAnneal(graph, T=1000, stopping_iter = 5000)
    sa.anneal()
    bs.add(sa.best_solution)

def main():

    bs = best_Solutions()
    graphs = cluster.getGraphs(5)
    start = time.process_time()
    for i in range(5):
        t = threading.Thread(target=worker, args=(graphs[i],bs,))
        t.start()

    #print('Waiting for worker threads')
    master_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not master_thread:
            t.join()

    print("Time taken = {0:.5f}".format(time.process_time() - start))
    print("Best solutions: ", bs.bs)
    
if __name__ == "__main__":
    main()


