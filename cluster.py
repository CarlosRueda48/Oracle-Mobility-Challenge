from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import db, graph, time

def cluster(n, points):
    return KMeans(n_clusters=n).fit(np.array(points))
    
def ZScore(x, avg, stdv):
    return (x - avg) / stdv

def getGraphs(n):
    # Get all nodes
    raw = db.GetNodes()
    # Oracle Campus Node
    oracleNode = raw[100]
    # Starting point nodes
    startCoords = raw[101:]
    # Remove oracle campus and starting point nodes from the rest
    raw = raw[:50]
    clustering_start_time = time.process_time()
    # Cluster data through k-means
    kmean = cluster(n, raw)
    # Print time it took to cluster the data
    print("Clustering took %s seconds." % (time.process_time() - clustering_start_time))
    graph_start_time = time.process_time()
    # Get edges with normalized weights
    edges = db.Normalise()
    # Create a graph for each cluster
    graphList = [graph.Graph() for i in range(n)]
    graphCounter = [0 for i in range(n)]

    # Create all vertices for each graph
    for i in range(len(raw)):
        graphList[kmean.labels_[i]].add_vertex(raw[i][0], raw[i][1], graphCounter[kmean.labels_[i]])
        graphCounter[kmean.labels_[i]] += 1

    # Create all edges for each graph
    for g in graphList:
        for i in range(len(edges[0])):
            # If both of the edge's vertices exist in the graph, then add that edge to the graph
            if((g.get_vertex(edges[0][i]) != None) and (g.get_vertex(edges[1][i]) != None)):
                g.add_edge(edges[0][i], edges[1][i], edges[2][i])

    for g in graphList:
        print("Vertices for graph:")
        for vert in g.vert_dict:
            print(g.vert_dict[vert])
    
    
    # Print time it took to create the complete graphs
    print("Creating graphs and assigning initial points took %s seconds." % (time.process_time() - graph_start_time))

    # Plot the clustered nodes
    labeledNodes = [[],[],[],[],[]]
    for i in range(0, len(raw)):
        if(kmean.labels_[i] == 0):
            labeledNodes[0].append(raw[i])
        elif(kmean.labels_[i] == 1):
            labeledNodes[1].append(raw[i])
        elif(kmean.labels_[i] == 2):
            labeledNodes[2].append(raw[i])
        elif(kmean.labels_[i] == 3):
            labeledNodes[3].append(raw[i])
        elif(kmean.labels_[i] == 4):
            labeledNodes[4].append(raw[i])

    plt.scatter(*zip(*labeledNodes[0]), color="red")
    plt.scatter(*zip(*labeledNodes[1]), color="blue")
    plt.scatter(*zip(*labeledNodes[2]), color ="green")
    plt.scatter(*zip(*labeledNodes[3]), color="yellow")
    plt.scatter(*zip(*labeledNodes[4]), color ="orange")
    plt.scatter(-103.4158208, 20.708207, color = "black")
    plt.scatter(-103.399223, 20.771859, color = "purple")
    plt.scatter(-103.281663, 20.703316, color = "purple")
    plt.scatter(-103.247455, 20.620652, color = "purple")
    plt.scatter(-103.313528, 20.573827, color = "purple")
    plt.scatter(-103.485171, 20.513207, color = "purple")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.show()


    return graphList
