import networkx as nx
from networkx import *
import pprint

edgelistfile = "test.csv"


def path(start,end):
    node1 = start
    node2 = end


    def findAllPaths(graph,start,end,maxLen):
        start = str(start)
        end = str(end)
        path = dict()
        paths = []
        queue = [(start,end,path)]
        nodeCount = dict()
        depth = 0
        nodeCount[depth] = 1
        while queue and depth + 1 < maxLen:
            start,end,path = queue.pop()
            nodeCount[depth] += -1
            path = path + [start]
            if start == end:
                paths.append(path)
            for node in set(graph[start]).difference(path):
                queue.append((node,end,path))
                try:
                    nodeCount[depth+1] += 1
                except:
                    nodeCount[depth+1] = 1
            if nodeCount[depth] == 0:
                depth += 1
            print ""
            print depth
            print nodeCount[depth]
            print""
        return paths

    def shortestPath(graph,start,end):
        try:
            sPath = shortest_path(myGraph,str(start),str(end))
            print "The shortest path has "+str(len(sPath)-1)+" degrees of separation.\n"
            print sPath
        except:
            print "No Path Found!"



    #Loads the network
    print "loading...",
    myGraph = nx.Graph()
    count = 0
    for line in open(edgelistfile, 'r'):
            count += 1
            one,two = line.split(',')
            myGraph.add_edge(one.strip(),two.strip())
    print "done, size: ",len(myGraph)

    print ""
    ##paths = findAllPaths(myGraph,node1,node2,6)
    ##for path in paths:
    ##    print path
    print ""
    print ""
    print "strat: "+str(node1)
    print "end: " +str(end)
    print "path: "+str(shortestPath(myGraph,node1,node2))
    print ""
    print ""
