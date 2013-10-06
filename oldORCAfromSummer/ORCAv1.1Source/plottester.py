import csv
import networkx as nx
import plot6
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import plottester2
import random
import vna2mpb
import numpy as np
from operator import itemgetter
GANG = "G322"
path = "C://users//x48661//Desktop//test//ORG-RES//GANG-"+GANG+"//"
nodes =[]
subs = []
coremem = "CORE-MEM-"
fullmap = "GANG-"+GANG+"-fullNet"
subgroup= "SUBGROUP-RELATIONS"
pairs = []
FLAG = 0
fig = plt.figure()
G = fig.add_subplot(111)
G = nx.Graph()
subgangs= []
subs = set()
x=[]
y=[]
print path+fullmap+'.vna'

reader = csv.reader(open(path+fullmap+'.vna','rb'),delimiter = '\t')
for row in reader:
    if FLAG ==1:
        pairs.append([row[0],row[1]])
        x.append(row[0])
        y.append(row[1])
    if row[0] == 'v1':
        FLAG=1
# read in edges
reader2 = csv.reader(open(path+"GANG-"+GANG+"-overallRollup.csv",'rb'),delimiter = ',')
flag2 = False
for row in reader2:
    if flag2:
        nodes.append(row)
    else:
        flag2= True
#read in full gangsters
for node in nodes:
    G.add_node(node[2])
#add in all gangsters to graph
reader3 = csv.reader(open(path+"CONNECTORS.GANG-"+GANG+".csv",'rb'),delimiter = ',')
Flag1= False
for row in reader3:
    if Flag1:
        for Prob, coreMember ,IR, lastName, firstName, nickName,Middle, stNum,  Dir, stName in nodes:
            if row[0]==IR:
                subgangs.append([row[0],row[2],row[3]])
                if row[2] not in subs:
                    subs.add(row[2])
                if row[3] != '':
                    if row[3] not in subs:
                        subs.add(row[3])
            else:
                pass      
    else:
        Flag1 = True
colors ={}
i = 0
for sub in subs:
    i = i +1
    colors.update({sub:i})
colorvalues = []
G.add_edges_from(pairs)
neicount = {}
for node in G.__iter__():
    count = 0
    tempcol= []
    subgangcolor = False
    tempcolor = 0
    for subgang in subgangs:
        tempnode = (node.split('('))
        if tempnode[0] == (subgang[0]):
            subgangcolor = True
            tempcolor = colors.get(subgang[1])
        else:
            pass
    if subgangcolor:
        random.seed(tempcolor)
        tempcol = [random.random(),random.random(),random.random()]
    else:
        tempcol = [1,1,1]
    colorvalues.append(tempcol)
    for n in G.neighbors(node):
        count = count +1
    neicount.update({node:count})
mapping = sorted(neicount.iteritems(),key=itemgetter(1), reverse = True)
values = [neicount.get(node,0.25) *25 for node in G.nodes()]
pos = nx.spring_layout(G)
plt.legend()
try1=[]
try2=[]
annotes=[]
for node, posvalue in pos.iteritems():
    annotes.append(node)
    try1.append(posvalue[0])
    try2.append(posvalue[1])
af= plottester2.AnnoteFinder(try1,try2,annotes)
nx.draw(G, pos,node_color= colorvalues, with_labels = False, node_size = values)
fig.canvas.mpl_connect('button_press_event',af)
plt.show()
