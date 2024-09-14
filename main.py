import copy
import math
import snap
import random
import math

# A simple graph used for testing
def testGraph():
    testGraph = snap.TUNGraph.New()
    for i in range(1, 7):
        testGraph.AddNode(i)
    edges = [(1, 2), (1, 3), (1, 5), (1, 4), (2, 4), (3, 6), (4, 5), (4, 6), (5, 6)]
    for edge in edges:
        testGraph.AddEdge(edge[0], edge[1])
    return testGraph

# A random graph
def randomGraph():
    G = snap.GenRndGnm(snap.TUNGraph, 1000, 2000)
    return G

# Create a graph from a file
def graphFromFile():
    G = snap.LoadEdgeList(snap.TUNGraph, "CA-GrQc.txt", 0, 1)
    return G

# The choosen graph
def generateNodeCosts(graph):
    # Create Dictionary to assign the cost of each node
    GCost1 = {}
    GCost2 = {}
    for node in graph.Nodes():
        GCost1[node.GetId()] = costFunctionRnd()
        GCost2[node.GetId()] = costFunctionDegree(node.GetDeg())

    return GCost1, GCost2

# Get Degree Centrality of each node in the graph, iterating over all nodes and getting the degree
def getDegreeCentrality(graph):
    nodes = snap.TIntFltH()
    for node in graph.Nodes():
        nodes[node.GetId()] = graph.GetDegreeCentr(node.GetId())
    return nodes

# Get Betweenness Centrality of each node in the graph
def getBetweennessCentrality(graph):
    nodes = snap.TIntFltH()
    edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(graph, nodes, edges, 1.0)
    return nodes

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

# Function 1 for Algorithm 1
def function1(graph, S):
    sum = 0
    for v in graph.Nodes():
        # |Nv ∩ S|
        intersectionCardinality = len(set(S) & set(v.GetOutEdges()))
        # deg(v)/2
        deg = math.ceil(v.GetDeg() / 2)
        # min(nv,deg)
        sum += min([intersectionCardinality, deg])
    return sum


# Function 2 for Algorithm 1
def function2(graph, S):
    sum = 0
    for v in graph.Nodes():
        # get |Nv ∩ S|
        nv = len(set(S) & set(v.GetOutEdges()))

        # sum max(dv/2-i+1, 0)
        for i in range(1, nv + 1):
            sum += max([math.ceil(v.GetDeg() / 2) - i + 1, 0])
    return sum

# Algorithm 1
# Find Seed Set, Greedy solution. Recall function1 and function2
def CostSeedsGreedy(graph, cost, budget, function):
    Sd = []
    costSd = 0
    while costSd <= budget and len(Sd) < graph.GetNodes():
        u = [0, -1]
        # get u, get argvmax v ∈ V-Sd
        fSd = function(graph, Sd)
        for node in filter(lambda node: node.GetId() not in Sd, graph.Nodes()):
            Sd.append(node.GetId())
            fSd_temp = function(graph, Sd)
            maxNode = (fSd_temp - fSd) / cost[node.GetId()]
            Sd.remove(node.GetId())
            
            if u[1] < maxNode:
                u[0] = node.GetId()
                u[1] = maxNode

        costSd += cost[u[0]]
        if costSd <= budget:
            Sd.append(u[0])

    return Sd

# Algorithm 3 (Our algorithm)
def ourAlgorithm(graph, cost: dict, budget, choosen_centrality_measure, use_ratios: bool = False):

    # List of nodes deleting nodes with cost > budget
    available_nodes = [node.GetId() for node in graph.Nodes() if cost[node.GetId()] <= budget]

    if use_ratios:
        # Sort the nodes by the ratio of the chosen centrality measure to the cost
        available_nodes.sort(key=lambda node: choosen_centrality_measure[node.GetId()] / cost[node.GetId()], reverse=True)
    else:
        # Sort the nodes by the chosen centrality measure
        available_nodes.sort(key=lambda x: choosen_centrality_measure[x], reverse=True)
    
    # Generate Seed Set, iteratively
    seed_set: list = []
    total_cost = 0
    
    for node_id in available_nodes:
        node_cost = cost[node_id]
        if total_cost + node_cost <= budget:
            seed_set.append(node_id)
            total_cost += node_cost
        else:
            break  # Stop when budget is exceeded
    
    return seed_set


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
def launchTest(graph, graph_costs, choosen_centrality_measure_set, testname):
    S1, S2, S3 = [], [], []
    Sd1, Sd2, Sd3 = [], [], []
    for budget in budgets_to_try:
        print(f"\nTest '{testname}' with budget {budget}:")
        print("\nGenerating Seed Set with Algorithm1, Function 1..")
        S = CostSeedsGreedy(graph, graph_costs, budget, function1)
        print("Algorithm1, Function 1 done. Next..")
        print("Calculating Influence Diffusion..")
        Sd = InfluenceDiffusionAlgorithm(S, nIterations)
        S1.append(S)
        Sd1.append(Sd)
        print("Influence Diffusion done. Next..")

        print("\nGenerating Seed Set with Algorithm1, Function 2..")
        S = CostSeedsGreedy(graph, graph_costs, budget, function2)
        print("Algorithm1, Function 2 done. Next..")
        print("Calculating Influence Diffusion..")
        Sd = InfluenceDiffusionAlgorithm(S, nIterations)
        S2.append(S)
        Sd2.append(Sd)
        print("Influence Diffusion done. Next..")

        print("\nGenerating Seed Set with Our Algorithm..")
        S = ourAlgorithm(graph, graph_costs, budget, choosen_centrality_measure_set)
        print("Our Algorithm done. Next..")
        print("Calculating Influence Diffusion..")
        Sd = InfluenceDiffusionAlgorithm(S, nIterations)
        S3.append(S)
        Sd3.append(Sd)
        print("Influence Diffusion done. Next..")

    fileInfluenced = open(f"Results/resultInfluensed{testname}.csv", mode='a')
    fileSeedSet = open(f"Results/sizeSeedSet{testname}.csv", mode='a')
    for i in range(0, len(budgets_to_try)):
        fileInfluenced.write(f"\n{budgets_to_try[i]},{len(Sd1[i])},{len(Sd2[i])},{len(Sd3[i])}")
        fileSeedSet.write(f"\n{budgets_to_try[i]},{len(S1[i])},{len(S2[i])},{len(S3[i])}")
    fileInfluenced.close()
    fileSeedSet.close()


# Useful constants
budgets_to_try = [10, 5]
nIterations = 100

if __name__ == "__main__":
    print("Loading graph..")
    graph = randomGraph()
    print("Done. Next..\n")
    
    print("Calculating costs..")
    random_costs, degree_costs = generateNodeCosts(graph)
    print("Done. Next..\n")

    print("Calculating Centrality..")
    # choosen_centrality_measure = getBetweennessCentrality(graph)
    choosen_centrality_measure_set = getDegreeCentrality(graph)
    print("Done. Next..\n")

    print("Launching tests..")
    # launchTest(graph, random_costs, "CostRandom")
    launchTest(graph, degree_costs, choosen_centrality_measure_set, "CostDegree")
    print("Done. Results saved in Results folder.")
