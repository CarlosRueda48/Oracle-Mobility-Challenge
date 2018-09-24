import sqlite3, matplotlib.pyplot as plt

class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self. lon = lon
        self.neighbors = []

    def __str__(self):
        return('%d, %d, %d', self.id, self.lat, self.lon)

def GetNodes():
    conn = sqlite3.connect("SEMANAi.db")
    c = conn.cursor()

    nodes = []
    rawCoords = []

    for coordinate in c.execute("SELECT * FROM LOCATIONS"):
        print(coordinate)
        rawCoords.append([coordinate[2], coordinate[1]])
        nodes.append(Node(coordinate[0], coordinate[1], coordinate[2]))
    
    return nodes, rawCoords

nodes, raw = getNodes()
plt.scatter(*zip(*raw))
plt.show()

