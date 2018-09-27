import math
import random
import visualize_tsp
import matplotlib.pyplot as plt
import cluster

class SimAnneal(object):
    def __init__(self, graph, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.graph = graph
        self.N = len(graph.vert_dict)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.dist_matrix = self.to_dist_matrix(graph)
        self.nodes = [i for i in range(self.N)]

        self.cur_solution = self.initial_solution()
        self.best_solution = list(self.cur_solution)

        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

        self.fitness_list = [self.cur_fitness]

    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        cur_node = random.choice(self.nodes)
        solution = [cur_node]

        free_list = list(self.nodes)
        free_list.remove(cur_node)

        while free_list:
            closest_dist = min([self.dist_matrix[cur_node][j] for j in free_list])
            cur_node = self.dist_matrix[cur_node].index(closest_dist)
            free_list.remove(cur_node)
            solution.append(cur_node)

        return solution

    def dist(self, node1, node2):
        """
        Precalculated weight
        """
        return node1.get_weight(node2)
    
    def to_dist_matrix(self, graph):
        """
        Returns nxn nested list from a list of length n
        Used as distance matrix: mat[i][j] is the distance between node i and j
        """
        n = len(self.graph.vert_dict)
        mat = [[self.dist(self.graph.get_vertex(i), self.graph.get_vertex(j)) for i in range(n)] for j in range(n)]
        return mat

    def fitness(self, sol):
        """ Objective value of a solution """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.N)]) +
                     self.dist_matrix[sol[0]][sol[self.N - 1]], 4)

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm
        """
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        print('Best fitness obtained: ', self.best_fitness)
        print('Improvement over greedy heuristic: ',
              round((self.initial_fitness - self.best_fitness) / (self.initial_fitness), 4))

    def visualize_routes(self):
        """
        Visualize the TSP route with matplotlib
        """
        #visualize_tsp.plotTSP([self.best_solution], self.coords)

    def plot_learning(self):
        """
        Plot the fitness through iterations
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel('Fitness')
        plt.xlabel('Iteration')
        plt.show()