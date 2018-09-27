from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import db, graph, time

def cluster(n, points):
    return KMeans(n_clusters=n).fit(np.array(points))
    
def ZScore(x, avg, stdv):
    return (x - avg) / stdv

# Receives two tuples and returns euclidian distance
def dist(x, y):
    return(np.sqrt(np.power((x[0] - y[0]), 2) + np.power((x[1] - y[1]), 2)))

# Get all nodes
raw = db.GetNodes()
# Oracle Campus Node
oracleNode = raw[100]
# Starting point nodes
startNodes = raw[101:]
# Remove oracle campus and starting point nodes from the rest
raw = raw[:50]
clustering_start_time = time.time()
kmean = cluster(5, raw)
# Print time it took to cluster the data
print("Clustering took %s seconds." % (time.time() - clustering_start_time))
graph_start_time = time.time()
# Get edges with normalized weights
edges = db.Normalise()
# Create a graph for each cluster
graphList = [graph.Graph() for i in range(5)]

# Create all vertices for each graph
for i in range(len(raw)):
    graphList[kmean.labels_[i]].add_vertex( raw[i][0], raw[i][1], i)
# Create all edges for each graph
for graph in graphList:
    for i in range(len(edges[0])):
        # If both of the edge's vertices exist in the graph, then add that edge to the graph
        if((graph.get_vertex(edges[0][i]) != None) and (graph.get_vertex(edges[1][i]) != None)
        and graph.get_vertex(edges[0][i]) != graph.get_vertex(edges[1][i])):
            graph.add_edge(edges[0][i], edges[1][i], edges[2][i])

for graph in graphList:
    print("Vertices for graph:")
    for vert in graph.vert_dict:
        print(graph.vert_dict[vert])

for startNode in startNodes:
    closest = kmean.cluster_centers_[0]
    for i in range(len(kmean.cluster_centers_)):
        if(dist(startNode, closest) > dist(startNode, kmean.cluster_centers_[i])):
            closest = kmean.cluster_centers_[i] 

# Print time it took to create the complete graphs
print("Creating graphs and assigning initial points took %s seconds." % (time.time() - graph_start_time))

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
