import matplotlib.pyplot as plt
import numpy as np
import sqlite3


class Node_distances:
    def __init__(self, ids, ide, distance, time):
        self.ids = ids
        self.ide = ide
        self.distance = distance
        self.time = time
        self.neighbors = []

    def __str__(self):
        return('%d, %d, %d, %d', self.ids, self.ide, self.distance, self.time)

class Node_locations:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.neighbors = []

    def __str__(self):
        return('%d, %d, %d', self.id, self.lat, self.lon)

def getNodes():
    conn = sqlite3.connect("SEMANAi.db")
    c = conn.cursor()

    nodes = []
    rawCoords = []
    distances = []
    nd = []

    for coordinate in c.execute("SELECT * FROM LOCATIONS"):
        #print(coordinate)
        rawCoords.append([coordinate[2], coordinate[1]])
        nodes.append([coordinate[0], coordinate[1], coordinate[2]]) #ID, LAT, LON
    
    for coordinate in c.execute("SELECT * FROM DISTANCES"):
        #print(coordinate)
        nd.append(Node_distances(coordinate[0], coordinate[1], coordinate[2], coordinate[3]))
        distances.append([coordinate[0], coordinate[1], coordinate[2], coordinate[3]]) #IDS, IDE, DIS, DUR
    
    return nodes, rawCoords, distances, nd

def normalization(dis, time):

    Dis = np.ma.masked_equal(dis, 0.0, copy=False)
    Time = np.ma.masked_equal(time, 0.0, copy=False)
    newDistances = []
    newTimes = []

    for item in xrange(len(dis)):
        newDistances.append(((dis[item]-Dis.min())/float((Dis.max()-Dis.min())))*0.1)
        newTimes.append(((time[item]-Time.min())/float((Time.max()-Time.min())))*0.9)
        

    return newDistances, newTimes

   

nodes, raw, dis, nd = getNodes()
nd.pop(0)
d =[]
t = []
for item in xrange(len(nd)):
    d.append(nd[item].distance)
    t.append(nd[item].time)

newDistances, newTimes = normalization(d,t)
for item in xrange(len(nd)):
    print '\n', 'ID', item, 
    print '\nOld: Time: ', nd[item].time, '\t\tDistance: ', nd[item].distance
    print 'New: Time: ', newTimes[item],'\tDistance: ', newDistances[item], '\n'
#plt.scatter(*zip(*raw))
#plt.show()