import copy
import math
import time
import snap
import random

K = 100


# A simple graph used for testing
def testGraph():
    testGraph = snap.TUNGraph.New()
    for i in range(1, 7):
        testGraph.AddNode(i)
    edges = [(1, 2), (1, 3), (1, 5), (1, 4), (2, 4), (3, 6), (4, 5), (4, 6), (5, 6)]
    for edge in edges:
        testGraph.AddEdge(edge[0], edge[1])
    return testGraph


def generateGraph():
    # generate a random graph
    #G = snap.GenRndGnm(snap.TUNGraph, 1000, 2000)

    # G = testGraph()

    G = snap.LoadEdgeList(snap.TUNGraph, "CA-GrQc.txt", 0, 1)

    # Create Dictionary to assign the cost of each node
    GCost1 = {}
    GCost2 = {}
    for node in G.Nodes():
        GCost1[node.GetId()] = costFunctionRnd()
        GCost2[node.GetId()] = costFunctionDegree(node.GetDeg())

    return G, GCost1, GCost2


# total cost of Seed set
def costSeedSet(S, cost):
    totalCost = 0
    for si in S:
        totalCost += cost[si]

    return totalCost


# cost function random, generate a random cost from 1 to 10
def costFunctionRnd():
    p = random.randint(1, 30)
    return p


# cost function, degree of node u/2
def costFunctionDegree(degree):
    if degree != 0:
        return degree / 2
    else:
        return 1


# First algorithm
def function1(S):
    sum = 0
    for v in graph.Nodes():
        # |Nv ∩ S|
        nv = 0
        for n in v.GetOutEdges():
            if n in S:
                nv += 1
        # deg(v)/2
        deg = math.ceil(v.GetDeg() / 2)
        # min(nv,deg)
        sum += nv if nv < deg else deg
    return sum


# Second algorithm
def function2(S):
    sum = 0
    for v in graph.Nodes():
        # get |Nv ∩ S|
        nv = len(set(S) & set(v.GetOutEdges()))

        # sum max(dv/2-i+1, 0)
        for i in range(1, nv + 1):
            if math.ceil(v.GetDeg() / 2) - i + 1 > 0:
                sum += math.ceil(v.GetDeg() / 2) - i + 1
    return sum


# Find Seed Set, Greedy solution. Recall function1 and function2
def CostSeedsGreedy(cost, function):
    Sd = []
    costSd = 0
    while costSd <= K and len(Sd) < graph.GetNodes():
        u = [0, -1]
        # get u, get argvmax v ∈ V-Sd
        fSd = function(Sd)
        for node in graph.Nodes():
            if node.GetId() not in Sd:
                Sd.append(node.GetId())
                maxNode = (function(Sd) - fSd) / cost[node.GetId()]
                Sd.remove(node.GetId())

                if u[1] < maxNode:
                    u[0] = node.GetId()
                    u[1] = maxNode

        costSd += cost[u[0]]

        if costSd <= K:
            Sd.append(u[0])

    return Sd


# Influence diffusion
def InfluenceDiffusionAlgorithm(S, r):
    Sd = copy.deepcopy(S)
    Sprev = copy.deepcopy(S)

    for iteration in range(0, r):
        for node in graph.Nodes():
            # v ∈ V-Inf[S, r−1]
            if node.GetId() not in Sprev:
                degAc = 0  # number of active neighbors

                # N(v) ∩ Inf[S, r−1]
                for nv in node.GetOutEdges():
                    if nv in Sprev:
                        degAc += 1

                if degAc >= math.ceil(node.GetDeg() / 2):  # TODO check round
                    Sd.append(node.GetId())
        Sprev = copy.deepcopy(Sd)
    return Sd


# Launch test and save the results on files
def launchTest(GC, testname):
    S1, S2, S3 = [], [], []
    Sd1, Sd2, Sd3 = [], [], []
    for k in Ks:
        K = k
        S = CostSeedsGreedy(GC, function1)
        Sd = InfluenceDiffusionAlgorithm(S, 100)
        S1.append(S)
        Sd1.append(Sd)

        S = CostSeedsGreedy(GC, function2)
        Sd = InfluenceDiffusionAlgorithm(S, 100)
        S2.append(S)
        Sd2.append(Sd)

        S3.append(S)
        Sd3.append(Sd)

    fileInfluensed = open(f"Results/resultInfluensed{testname}.csv", mode='a')
    fileSeedSet = open(f"Results/sizeSeedSet{testname}.csv", mode='a')
    for i in range(0, len(Ks)):
        fileInfluensed.write(f"\n{Ks[i]},{len(Sd1[i])},{len(Sd2[i])},{len(Sd3[i])}")
        fileSeedSet.write(f"\n{Ks[i]},{len(S1[i])},{len(S2[i])},{len(S3[i])}")
    fileInfluensed.close()
    fileSeedSet.close()


graph, GC1, GC2 = generateGraph()

# Algorithm 1
#function = function1
#startTime = time.perf_counter()
#S = CostSeedsGreedy(GC2, function)
#print("tempo per S = ", time.perf_counter() - startTime)
#startTime = time.perf_counter()
#Sd = InfluenceDiffusionAlgorithm(S, 100)
#print("tempo spread S = ", time.perf_counter() - startTime)
#print("Random\nnodi in Seed set: ", S)
#print("nodi in S: ", Sd)
#print("numero di nodi in S: ", len(Sd))
#cost = costSeedSet(S, GC2)
#print(f"total cost of seedset {cost}")


Ks = [10, 5]

launchTest(GC1, "CostRandom")
launchTest(GC2, "CostDegree")
