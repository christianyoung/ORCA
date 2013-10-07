#Needed for ltDecomp
import numpy as np
import networkx as nx

def dictToAr(inDict):
	i=0
	res = []
	for item in list(inDict.keys()):
		res.insert(i,inDict[item])
		i=i+1
	return res
	
def sdOfDict(inDict):
	return np.std(dictToAr(inDict))

def sdInAndOut(G):
	s1 = str(sdOfDict(nx.algorithms.centrality.in_degree_centrality(G)))
	s2 = str(sdOfDict(nx.algorithms.centrality.out_degree_centrality(G)))
	return s1+","+s2
	