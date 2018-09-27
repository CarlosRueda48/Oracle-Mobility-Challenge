# Get distances from starting points to centroids
distances = []
for i in range(len(startNodes)):
    for j in range(len(kmean.cluster_centers_)):
        distances.append(math.sqrt((startNodes[i][0] - kmean.cluster_centers_[j][0])**2 + (startNodes[i][1] - kmean.cluster_centers_[j][1])**2))

closest = [[distances[0], 1], [distances[5], 1], [distances[10], 1], [distances[15], 1], [distances[20], 1]]

for i in range(4):
    if distances[i + 1] < closest[0][0]:
        closest[0][0] = distances[i + 1]
        closest[0][1] = i + 2

for i in range(5, 9):
    if distances[i + 1] < closest[1][0]:
        closest[1][0] = distances[i + 1]
        closest[1][1] = i + 2 - 5

for i in range(10, 14):
    if distances[i + 1] < closest[2][0]:
        closest[2][0] = distances[i + 1]
        closest[2][1] = i + 2 - 10

for i in range(15, 19):
    if distances[i + 1] < closest[3][0]:
        closest[3][0] = distances[i + 1]
        closest[3][1] = i + 2 - 15

for i in range(20, 24):
    if distances[i + 1] < closest[4][0]:
        closest[4][0] = distances[i + 1]
        closest[4][1] = i + 2 - 20

for i in range(4):
    for j in range(4, i, -1):
        if closest[i][1] == closest[j][1]:
            print("Alert! There are 2 starting points for the same cluster!")
            print(closest[i][1])
            print(closest[j][1])
