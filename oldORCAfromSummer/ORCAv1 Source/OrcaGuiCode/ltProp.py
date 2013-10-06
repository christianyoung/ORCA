#Needed for ltDecomp
import math
import numpy
import networkx as nx
import csv
import bh
import time


def actNeigh(mainNode, graph, theSet):
        res = 0
        for node in graph.predecessors_iter(mainNode):
                if (node in theSet):
                        res = res +1
        return float(res)

def meetThresh(mainNode, graph, theSet, newSet, nodeDict):
        thresh = float(nodeDict[mainNode])
        flag = False
        if actNeigh(mainNode, graph, theSet) >= thresh:
                newSet.add(mainNode)
                flag = True
        return flag

def meetThresh(mainNode, graph, theSet, nodeDict):
        thresh = float(nodeDict[mainNode])
        flag = False
        if actNeigh(mainNode, graph, theSet) >= thresh:
                theSet.add(mainNode)
                flag = True
        return flag

def ltCalcInnerLoopNc(graph, theSet, nodeDict):
	#print("starting inner loop")
	change = False
	curFlag = False
	#newSet = theSet.copy()
	for node in graph.nodes_iter(data=False):
		if (node not in theSet):
			curFlag = meetThresh(node, graph, theSet, nodeDict)
			if curFlag:
				change=True
	#theSet = newSet.copy()
	return change

		
def ltCalcInnerLoop(graph, theSet, nodeDict):
	#print("starting inner loop")
	change = False
	curFlag = False
	newSet = theSet.copy()
	for node in graph.nodes_iter(data=False):
		if (node not in theSet):
			curFlag = meetThresh(node, graph, theSet, newSet, nodeDict)
			if curFlag:
				change=True
	theSet = newSet.copy()
	return change

def ltCalcOuterLoopStr(graph, theSet, nodeDict):
	change = True
	i= 0
	while change:
			change = ltCalcInnerLoopNc(graph, theSet, nodeDict)
			i = i+1
	numOfNodes = float(len(nodeDict))
	frac = str(float(len(theSet))/numOfNodes)
	res =frac+", "+str(i)
	return res
		
def ltCalcOuterLoop(graph, theSet, nodeDict):
        change = True
        while change:
                change = ltCalcInnerLoop(graph, theSet, nodeDict)
        return float(len(theSet))

def ltProp(graph, theSet, intFlag, thresh):
	print("   Running propogation (init size: "+str(len(theSet))+")...")
	kDict = nx.algorithms.centrality.in_degree_centrality(graph)
	nFact = float(graph.number_of_nodes()-1)
	vertList=list(kDict.keys())
	for item in vertList:
		kDict[item]=round(kDict[item]*nFact)
		if intFlag:
			if kDict[item] > thresh:
				kDict[item]=thresh
		else:
			if not(thresh == 1.0):
				kDict[item]=math.ceil(kDict[item]*thresh)
	
	res = ltCalcOuterLoopNc(graph, theSet, kDict)/float(nFact+1)
	print("    -> complete :"+str(res)+")")
	return res

def ltPropIter(graph, theSet, intFlag, thresh):
	print("   Running propogation (init size: "+str(len(theSet))+")...")
	kDict = nx.algorithms.centrality.in_degree_centrality(graph)
	nFact = float(graph.number_of_nodes()-1)
	vertList=list(kDict.keys())
	for item in vertList:
		kDict[item]=round(kDict[item]*nFact)
		if intFlag:
			if kDict[item] > thresh:
				kDict[item]=thresh
		else:
			if not(thresh == 1.0):
				kDict[item]=math.ceil(kDict[item]*thresh)
	
	res = ltCalcOuterLoopStr(graph, theSet, kDict)
	print("    -> complete (FRAC,ITER: "+res+")")
	return res


