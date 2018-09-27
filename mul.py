from functools import partial
import os, time, multiprocessing



def f(name):

    print('Process:', os.getpid())
    print('Hello from: ', name)

def main():

    arr = ['bob','carl','gerry','ivan','daniel']
    pool = multiprocessing.Pool()
    func = partial(f)
    pool.map(func, arr)
    pool.close()
    pool.join()

if __name__ == "__main__":
    start = time.time()
    main()
    print("Time taken = {0:.5f}".format(time.time() - start))
