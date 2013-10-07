import numpy
import networkx as nx
import bh
import time
import math
import copy
import ltProp
import psUtils
import community

infty= 1000000000000000000


def createBoolDict(graph):
	res = {}
	for item in graph.nodes_iter():
		res[item] = True
	return res
	
def heapToSet(heap):
        res = set()
        
        for x in heap:
                res.add(x)
                
        return res


def decNode(node, valArry, pointerArray, heap):
        if not (valArry[node]==infty):
                valArry[node]=valArry[node]-1
                if valArry[node] < 0:
                        valArry[node]= infty
                        pointerArray[node].delete()
                        pointerArray[node]=heap.insert(valArry[node],node)
                else:
                        pointerArray[node].decrease(valArry[node])

def decOutNeigh(mainNode, valArry, pointerArray, heap, graph, nodeBoolDict):
        for node in graph.successors_iter(mainNode):
			if nodeBoolDict[node]:
					decNode(node,valArry, pointerArray, heap)

def pickMinAndRem(valArry, pointerArray, heap, graph, nodeBoolDict):
        lastOne = False
        topNode = heap.min()
        topVal = valArry[topNode]
        #print("node: "+topNode)
        #print("topVal: "+str(topVal))
        if not (topVal == infty):
                heap.extract_min()

                decOutNeigh(topNode, valArry, pointerArray, heap, graph, nodeBoolDict)
                nodeBoolDict[topNode]=False

        else:
                lastOne=True
        return lastOne

def biHeapToAr(heap):
        res = []
        i=0
        for x in heap:
                res.insert(i,x)
                i = i+1
        return res

def mainLoop(valArry, pointerArray, heap, graph, nodeBoolDict):
        stopFlag = False
        while not(stopFlag):
                stopFlag = pickMinAndRem(valArry, pointerArray, heap, graph, nodeBoolDict)
        return heapToSet(heap)

def ltdForCpd(theNet,dsName,outFullPath):
	theNet = theNet.to_directed()
	thresh = 0.5
	#dsName = "cpdDataset"
	resSet = set()
	intFlag = False
	origNet = theNet
	chkFlag = False
	seedSet= ltDecompose(theNet, thresh, dsName, resSet, intFlag, origNet, chkFlag)
	percSize = str(100.*float(len(seedSet))/float(len(theNet)))
	with open(outFullPath, 'w') as fh:
		fh.write("Influence set "+dsName+"\n\n")
		fh.write("Influence set size: "+percSize+"% of total population.\n\n")
		fh.write("Members:\n")
		for ir in seedSet:
			fh.write(str(ir)+"\n")
		
def ltDecompose(theNet, thresh, dsName, resSet, intFlag, origNet, chkFlag):
	print("   Executing setup tasks... ")
	nodeBoolDict = createBoolDict(theNet)
	t1=time.clock()
	numNodes = str(theNet.__len__())
	numEdges = str(theNet.size())
	nFact = float(theNet.number_of_nodes()-1)
	kDict = nx.algorithms.centrality.in_degree_centrality(theNet)
	vertList=list(kDict.keys())
	pointerDict = {}
	valDict ={}
	h = bh.heap()
	for item in vertList:
		kDict[item]=round(kDict[item]*nFact)
		cur = kDict[item]
		if intFlag:
			if kDict[item] > thresh:
				kDict[item]=thresh
		else:
			if not(thresh == 1.0):
				kDict[item]=math.ceil(kDict[item]*thresh)
		keyVal = cur-kDict[item]
		pointerDict[item]=h.insert(keyVal,item)
		kDict[item]=keyVal
	t2 = time.clock()
	setTime = t2-t1
	print("    -> setup tasks complete ("+str(setTime)+" sec).")
	print("   Running decomp alg... ")
	sTime = time.clock()
	resSet=mainLoop(kDict, pointerDict, h, theNet, nodeBoolDict)
	eTime = time.clock()
	numer = float(len(resSet))
	percRes=str(100*numer/float(nFact+1))
	algTime=eTime-sTime
	timeRes=str(algTime)
	totTime=str(algTime+setTime)
	print("    -> decomp alg complete ("+timeRes+" sec).")
	print("    -> perc of overall: "+percRes+" %")
	if intFlag:
		resStr = dsName+",valThresh,"+str(thresh)+","+percRes+","+numNodes+","+numEdges+","+timeRes+","+totTime
	else:
		resStr = dsName+",percThresh,"+str(thresh)+","+percRes+","+numNodes+","+numEdges+","+timeRes+","+totTime
	if chkFlag:
		#propVal=ltProp.ltPropIter(origNet, resSet, intFlag, thresh)
		propVal = 1
		resStr=resStr+","+propVal
	#return resStr+"\n"
	return resSet

def ltDecomposeNoSet(theNet, thresh, dsName, intFlag):
    dummy=set()
    return ltDecompose(theNet, thresh, dsName, dummy, intFlag, theNet, False)
	

def ltDecomposeNoSetWithCheck(theNet, thresh, dsName, intFlag, origNet):
	dummy=set()
	return ltDecompose(theNet, thresh, dsName, dummy, intFlag, origNet, True)

	
def loadNw(dsName,path,cd,wccOnly,revEdges,undir):
	print("   Opening "+dsName+" and loading graph... ")
	t1=time.clock()
	fh=open(path+dsName,'rb')
	if undir:
		if cd:
			prodNet=nx.read_edgelist(fh,delimiter=',')
		else:
			prodNet=nx.read_edgelist(fh)
		prodNet = prodNet.to_directed()
	else:
		if cd:
			prodNet=nx.read_edgelist(fh,delimiter=',',create_using=nx.DiGraph())
		else:
			prodNet=nx.read_edgelist(fh,create_using=nx.DiGraph())
               
	fh.close()
	if wccOnly:
		prodNet=nx.algorithms.weakly_connected.weakly_connected_component_subgraphs(prodNet)[0]
	
	prodNet.remove_edges_from(prodNet.selfloop_edges())
	
	if revEdges:
		prodNet.reverse(False)
	
	numNodes = str(prodNet.__len__())
	numEdges = str(prodNet.size())
	t2=time.clock()
	print("    -> graph loaded: "+numNodes+" nodes, "+numEdges+" edges ("+str(t2-t1)+" sec).")
	return prodNet        

def loadNwU(dsName,path,cd,wccOnly,revEdges,undir):
	print("   Opening "+dsName+" and loading graph... ")
	t1=time.clock()
	fh=open(path+dsName,'rb')
	if undir:
		if cd:
			prodNet=nx.read_edgelist(fh,delimiter=',')
		else:
			prodNet=nx.read_edgelist(fh)
		#prodNet = prodNet.to_directed()
	else:
		if cd:
			prodNet=nx.read_edgelist(fh,delimiter=',',create_using=nx.DiGraph())
		else:
			prodNet=nx.read_edgelist(fh,create_using=nx.DiGraph())
               
	fh.close()
	if wccOnly:
		prodNet=nx.algorithms.weakly_connected.weakly_connected_component_subgraphs(prodNet)[0]
	
	prodNet.remove_edges_from(prodNet.selfloop_edges())
	
	if revEdges:
		prodNet.reverse(False)
	
	numNodes = str(prodNet.__len__())
	numEdges = str(prodNet.size())
	t2=time.clock()
	print("    -> graph loaded: "+numNodes+" nodes, "+numEdges+" edges ("+str(t2-t1)+" sec).")
	return prodNet        
	
def ltDecomposeLd(thresh, dsName, intFlag, path, cd, wccOnly, revEdges, undir):
    prodNet = loadNw(dsName,path,cd,wccOnly,revEdges,undir)
    return ltDecomposeNoSet(prodNet,thresh,dsName,intFlag)

def ltDecomposeTestBatTh(dsName, path, outfile, cd):
	ltDecomposeTestBat(dsName,path,outfile,cd,False,False,True)

def ltDecomposeTestBatThFif(dsName, path, outfile, cd):
	ltDecomposeTestFifty(dsName,path,outfile,cd,False,False,True)

	
def ltDecomposeTestBat(dsName, path, outfile, cd, wccOnly, revEdges, undir):
	origNet = loadNw(dsName,path,cd,wccOnly,revEdges,undir)
	prodNet=origNet
	
	#prodNet = copy.deepcopy(origNet)
	#print("dc")
	intFlag = True
	#thresh = 2.0
	outfile=open(path+outfile+".csv", 'w')
	#print("TWO TEST")
	#outfile.write("TWO TEST:\n")
	#outfile.write("Dataset,ThreshType,ThreshVal,PercSize,NumNodes,NumEdges,TimeAlg,TimeAlgAndSetup,Check\n")
	#outfile.write(ltDecomposeNoSetWithCheck(prodNet,thresh,dsName,intFlag,origNet))
	outfile.write("\n\nTHRESH TESTS:\n")
	outfile.write("Dataset,ThreshType,ThreshVal,PercSize,NumNodes,NumEdges,TimeAlg,TimeAlgAndSetup,Check\n")
	intFlag = False
	for i in range(1,12):
		thresh = float(i+1)/float(20)
		print("THRESH TEST "+str(i)+": "+str(thresh))
		outfile.write(ltDecomposeNoSetWithCheck(prodNet,thresh,dsName,intFlag,origNet))
	outfile.close()
	print("Done.")    

def ltDecomposeTestFifty(dsName, path, outfile, cd, wccOnly, revEdges, undir):
	origNet = loadNw(dsName,path,cd,wccOnly,revEdges,undir)
	prodNet=origNet
	
	#prodNet = copy.deepcopy(origNet)
	#print("dc")
	intFlag = True
	#thresh = 2.0
	outfile=open(path+outfile+".csv", 'w')
	#print("TWO TEST")
	#outfile.write("TWO TEST:\n")
	#outfile.write("Dataset,ThreshType,ThreshVal,PercSize,NumNodes,NumEdges,TimeAlg,TimeAlgAndSetup,Check\n")
	#outfile.write(ltDecomposeNoSetWithCheck(prodNet,thresh,dsName,intFlag,origNet))
	outfile.write("\n\nTHRESH TESTS:\n")
	outfile.write("Dataset,ThreshType,ThreshVal,PercSize,NumNodes,NumEdges,TimeAlg,TimeAlgAndSetup,Check\n")
	intFlag = False
	#or i in range(1,12):
	thresh = 0.50
	# thresh = float(i+1)/float(20)
	print("THRESH TEST "+str(i)+": "+str(thresh))
	outfile.write(ltDecomposeNoSetWithCheck(prodNet,thresh,dsName,intFlag,origNet))
	outfile.close()
	print("Done.")    


	
	
def ltDecomposeTestBatFull(dsName, path, outfile, cd, wccOnly, revEdges, undir, diaF, fillF):
	origNet = loadNw(dsName,path,cd,wccOnly,revEdges,undir)
	prodNet=origNet
	#prodNet = copy.deepcopy(origNet)
	#print("dc")
	outfile=open(path+outfile+".csv", 'w')
	intFlag = False
	print("NW-WIDE MEASURES:\n")
	
	nodeStr=str(origNet.number_of_nodes())
	edgeStr=str(origNet.number_of_edges())
	avgDeg = str(float(origNet.number_of_edges())/float(origNet.number_of_nodes()))
	dens = str(nx.density(origNet))
	avgCl="--"
	#avgCl = str(nx.average_clustering(origNet))
	
	if diaF:
		print("  Starting dia calc")
		diameter = str(nx.diameter(origNet))
		print("  --> done w. dia calc")
	else:
		diameter="---"
	
	#outfile.write("Dataset,NumNodes,NumEdges,avgDeg,dens,avgCl,diameter\n")
	#outfile.write(dsName+","+nodeStr+","+edgeStr+","+avgDeg+","+dens+","+avgCl+","+diameter+"\n")
	#if fillF:
	#	print("FULL THRESH TEST\n")
		#outfile.write("Dataset,ThreshType,ThreshVal,PercSize,NumNodes,NumEdges,TimeAlg,TimeAlgAndSetup,Check\n")
		#thresh=1.0	
		#outfile.write(ltDecomposeNoSetWithCheck(prodNet,thresh,dsName,intFlag,origNet))
		
	outfile.close()
	print("Done.")    
