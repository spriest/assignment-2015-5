import sys

def initialize():
    #define global variables to be used throughout the program
    global inputfile
    global start_node
    global destination_node
    global relocate
    global blockFile
    global maxInt
    maxInt = sys.maxsize
    global Graph
    Graph = dict() # We use a dictionary to represent the adjacency list G(V,E)
    global costs
    costs = dict() #Store the cost for every node pair
    global blocked 
    blocked = set()
    global maxNode
    maxNode = -1 #Initialize pq(priorityQueue)

#read input values
    if len(sys.argv) < 4:
        print("Please follow this pattern: python ctp.py graph_file start_node destination_node [-r] [-b blocked_edges_file]")
        sys.exit()

    inputfile = sys.argv[1]
    start_node = int(sys.argv[2])
    destination_node = int(sys.argv[3])

    if '-r' in sys.argv:
        relocate = True
    else:
        relocate = False

    if '-b' in sys.argv:
        blockFile = sys.argv[sys.argv.index('-b') + 1]
    else:
        blockFile = None

def create_queue(maxNode):
    pq = []
    for i in range(maxNode + 1):
        #If pq.get() == -1 the node doesn't exist
        pq.append(-1)

    return pq

def insert(pq, i, d): pq[i] = d
def update(pq, i, d): pq[i] = d
def extractMin(pq):
    minVal = maxInt
    for node, val in enumerate(pq):
        if val != -1 and val < minVal:
            minVal = val
            minNode = node

    pq[minNode] = -1 #Delete node
    return minNode

def size(pq):
    count = 0;
    for val in pq:
        if val != -1:
            count += 1

    return count
    
def dijkstra(graph,start_node, destination_node, costs, blocked):

    global maxNode
    pred = dict()
    dist = dict()

    for node in graph:
        pred[node] = None # Define all predecessors as none
        dist[node] = maxInt #Initialize distances to max values in order to apply relaxation

    dist[start_node] = 0     

    pq = create_queue(maxNode)
    insert(pq, start_node, dist[start_node])

    while size(pq) != 0:
        u = extractMin(pq)

        
        if u == destination_node: #Destination reached
            break

        for v in graph[u]:
            if dist[v] > dist[u] + costs[(u, v)]:
                dist[v] = dist[u] + costs[(u, v)]
                pred[v] = u

                if v in pq:
                    update(pq, v, dist[v])
                else:
                    insert(pq, v, dist[v])

    #Go backwords to define your predecessors
    path = []
    u = destination_node
    while pred[u] != None:
        path.insert(0, u)
        u = pred[u]
    path.insert(0, u)

    return path, dist[destination_node]

def readBlockedNodes(): # Read blocked nodes from file
    if blockFile is not None:
        bf = open(blockFile, 'r')
        for line in bf:
            l1,l2 = line.split()
            n1 = int(l1)
            n2 = int(l2)

            blocked.add((n1, n2))
            blocked.add((n2, n1))

        bf.close()

def implementGraph():
    global maxNode
    myFile = open(inputfile, 'r')
    for line in myFile:
        l1, l2, l3 = line.split()
        n1 = int(l1)
        n2 = int(l2)
        cost = int(l3)

        if n1 not in Graph:
            Graph[n1] = [n2]
        else:
            Graph[n1].append(n2)
            if n1 > maxNode: maxNode = n1
        costs[(n1, n2)] = cost

        if n2 not in Graph:
            Graph[n2] = [n1]
        else:
            Graph[n2].append(n1)
            if n2 > maxNode: maxNode = n2
        costs[(n2, n1)] = cost

    myFile.close()

def shortestPath():
    global start_node
    found = False
    pathResult = []
    distance = 0
    while not found:
        # Run Dijkstra to find the shortest path in the gragh
        path, dist = dijkstra(Graph,start_node, destination_node,costs,blocked)

        found = True
        part_dist = 0 # Add the costs until you find a blocked node
        pathLenght = len(path) - 1

        for i in range(pathLenght):
            if (path[i], path[i + 1]) not in blocked:
                part_dist += costs[(path[i], path[i + 1])]
            else:
                #In case you find a blocked edge delete it from graph
                for j in range(len(Graph[path[i]])):
                    if Graph[path[i]][j] == path[i + 1]:
                        del Graph[path[i]][j]
                        break
                #In case we use relocation we count only the path we covered until now
                if not(relocate):
                    pathResult += path[:i]
                    distance += part_dist
                    start_node = path[i] 
                    
                else:
                    returnPath = path[1:i + 1]
                    returnPath.reverse()
                    pathResult += path[:i] + returnPath
                    distance += part_dist * 2
                found = False
                break

    pathResult += path 
    distance += dist

    print(pathResult)
    print(distance)

initialize() #Initialize all program variables
readBlockedNodes() 
implementGraph() #Create a graph by reading an input file
shortestPath()#Choose the appropriate way to print the shortest path