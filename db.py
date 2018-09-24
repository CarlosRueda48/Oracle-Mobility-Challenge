import sqlite3

class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self. lon = lon
        self.neighbors = []

    def __str__(self):
        return('%d, %d, %d', self.id, self.lat, self.lon)

conn = sqlite3.connect("SEMANAi.db")
c = conn.cursor()

nodes = []

for coordinate in c.execute("SELECT * FROM LOCATIONS"):
    print(coordinate)
    nodes.append(Node(coordinate[0], coordinate[1], coordinate[2]))

