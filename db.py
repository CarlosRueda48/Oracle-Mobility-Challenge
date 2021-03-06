import sqlite3, matplotlib.pyplot as plt

def GetNodes():
    conn = sqlite3.connect("SEMANAi.db")
    c = conn.cursor()

    rawCoords = []

    for coordinate in c.execute("SELECT * FROM LOCATIONS"):
        # Index 2 goes first to get x (longitude) and y (latitude) in the correct order
        rawCoords.append([coordinate[2], coordinate[1]])
    conn.close()
    return rawCoords

def Normalise():
    weight = [[], [], []]
    temp1 = []
    temp2 = []
    conn = sqlite3.connect("SEMANAi.db")
    c = conn.cursor()
    #Extract start and end nodes, distance and duration from database
    for parameter in c.execute("SELECT * FROM DISTANCES"):
        weight[0].append(parameter[0])
        weight[1].append(parameter[1])
        temp1.append(parameter[2])
        temp2.append(parameter[3])
    conn.close()
    #Normalise 
    for i, z in enumerate(temp1):
        temp1[i] = (z - min(temp1)) / (max(temp1) - min(temp1)) * 0.1

    for i, z in enumerate(temp2):
        temp2[i] = (z - min(temp2)) / (max(temp2) - min(temp2)) * 0.9

    for i in range(len(temp1)):
        weight[2].append(temp1[i] + temp2[i])
        

    return weight

def NormalizeToMatrix(n):
    weight = [[] for i in range(n)]
    temp1 = []
    temp2 = []
    conn = sqlite3.connect("SEMANAi.db")
    c = conn.cursor()
    #Extract start and end nodes, distance and duration from database
    for parameter in c.execute("SELECT * FROM DISTANCES"):
        weight[0].append(parameter[0])
        weight[1].append(parameter[1])
        temp1.append(parameter[2])
        temp2.append(parameter[3])
    conn.close()
    #Normalise 
    for i, z in enumerate(temp1):
        temp1[i] = (z - min(temp1)) / (max(temp1) - min(temp1)) * 0.1

    for i, z in enumerate(temp2):
        temp2[i] = (z - min(temp2)) / (max(temp2) - min(temp2)) * 0.9

    for i in range(len(temp1)):
        weight[2].append(temp1[i] + temp2[i])
        

    return weight