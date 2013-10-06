import csv
import networkx as nx
import plot6
import matplotlib.pyplot as plt

def draw(filename):
	FLAG = 0
	x = []
	y = []
	reader = csv.reader(open(filename+'.vna', 'rb'),delimiter='\t') #dialect='excel-tab')

	for row in reader:
		if FLAG == 1:
			x.append(row[0])
			y.append(row[1])
		if row[0] == 'v1':
			FLAG = 1
		
	with open(filename+'.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		for i in range(len(x)):
			writer.writerow([x[i]] + [y[i]])

	G = nx.read_edgelist(filename+'.csv', delimiter=",",create_using = nx.Graph(), nodetype = str)	

	plot6.Save(G,filename)
