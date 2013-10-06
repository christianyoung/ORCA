import csv
import networkx as nx
import plot6
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import plottester2
import random
import numpy as np
from operator import itemgetter









def fullnet(fullpath,name,show):
    
    adjuster =1.0
    nodes=[]
    subs=[]
    pairs=[]
    FLAG=0
    x=[]
    y=[]
    subgangs=[]
    subs= set()
    
    #if (plt.fignum_exists(1)):
    #    pass
    #else:
    fig=plt.figure(1,)
    plt.clf()
    fig.suptitle(name + " Fullmap")
    G = fig.add_subplot(111)
    G = nx.Graph()
    
    reader = csv.reader(open(fullpath+name+"-fullNet.vna",'rb'),delimiter = '\t')
    for row in reader:
        if FLAG ==1:
            pairs.append([row[0],row[1]])
            x.append(row[0])
            y.append(row[1])
        if row[0] == 'v1':
            FLAG =1
    reader2= csv.reader(open(fullpath+name+"-overallRollup.csv",'rb'),delimiter =',')
    flag2 = False
    for row in reader2:
        if flag2:
            nodes.append(row)
        else:
            flag2=True
    for node in nodes:
        G.add_node(node[2])
    reader3 = csv.reader(open(fullpath+"CONNECTORS."+name+".csv",'rb'),delimiter=',')
    Flag1= False
    for row in reader3:
        if Flag1:
            for Prob, coreMember, IR, lastName,firstName,nickName,Middle,stNum,Dir, stName in nodes:
                if row[0] ==IR:
                    subgangs.append([row[0],row[2],row[3]])
                    if row[2] not in subs:
                      subs.add(row[2])
                    if row[3] != '':
                        if row[3] not in subs:
                            subs.add(row[3])

                else:
                    pass
        else:
            Flag1=True
    colors={}
    i=0
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
    pos = nx.circular_layout(G)
    pos = nx.spring_layout(G,dim=2,pos=pos)
    try1=[]
    try2=[]
    
    annotes=[]
    for node, posvalue in pos.iteritems():
        annotes.append(node)



        try1.append(posvalue[0])
        try2.append(posvalue[1])
    af= plottester2.AnnoteFinder(try1,try2,annotes)
    nx.draw(G,pos,node_color=colorvalues, with_labels = False, node_size=values)
    fig.canvas.mpl_connect('button_press_event',af)
    #plt.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
    plt.xlim(min(try1),max(try1))
    plt.ylim(min(try1),max(try1))

    if show == 0:

        
        plt.show()
    if show == 1:
        fig.set_size_inches(8,8)
      
        
        
        plt.savefig(fullpath+name+"-fullnet.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)
def coremem(fullpath,name,show):
    
    adjuster =1.0
    nodes=[]
    subs=[]
    pairs=[]
    FLAG=0
    x=[]
    y=[]
    shapes=[]
    subgangs=[]
    subs= set()
    #if (plt.fignum_exists(2)):
    # Figure is still opened
    #    pass
    #else:
    fig=plt.figure(2)
    plt.clf()
    fig.suptitle(name + " Core Members")
    H = fig.add_subplot(111)
    G = nx.Graph()
    
    yess =set()
    covers=set()

    reader = csv.reader(open(fullpath+"CORE-MEM-.vna",'rb'),delimiter = '\t')
    for row in reader:

        if FLAG ==1:
            if row[0].startswith("++"):
                tempx= row[0].lstrip('+')
                covers.add(tempx)
            else:
                if row[0].startswith("+"):
                    tempx = row[0].lstrip('+')
                    yess.add(tempx)
                else:
                    tempx=row[0]
            if row[1].startswith("++"):
                tempy = row[1].lstrip('+')
                covers.add(tempy)
            else:
                if row[1].startswith("+"):
                    tempy = row[1].lstrip('+')
                    yess.add(tempy)
                else:
                    tempy = row[1]
            pairs.append([tempx,tempy])
            
        if row[0] == 'v1':
            FLAG =1
    
    reader2= csv.reader(open(fullpath+"CORE-MEM-ROLLUP.csv",'rb'),delimiter =',')
    flag2 = False
    for row in reader2:
        if flag2:
            nodes.append(row)
        else:
            flag2=True
    for node in nodes:
        G.add_node(node[2])
    reader3 = csv.reader(open(fullpath+"CONNECTORS."+name+".csv",'rb'),delimiter=',')
    Flag1= False
    for row in reader3:
        if Flag1:
            for Prob, coreMember, IR, lastName,firstName,nickName,Middle,stNum,Dir, stName in nodes:
                if row[0] ==IR:
                    subgangs.append([row[0],row[2],row[3]])
                    if row[2] not in subs:
                      subs.add(row[2])
                    if row[3] != '':
                        if row[3] not in subs:
                            subs.add(row[3])

                else:
                    pass
        else:
            Flag1=True
    colors={}
    i=0
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
    


    pos = nx.circular_layout(G)
    pos = nx.spring_layout(G,dim=2,pos=pos)
    
    try1=[]
    try2=[]
    annotes=[]
    for node, posvalue in pos.iteritems():
        if node in covers:
            tempnode= "++"+node
        else:
            if node in yess:
               tempnode="+"+node
            else:
                tempnode= node
        
        annotes.append(tempnode)

        try1.append(posvalue[0])
        try2.append(posvalue[1])
    
    af= plottester2.AnnoteFinder(try1,try2,annotes)
    fig.canvas.mpl_connect('button_press_event',af)
    nx.draw(G,pos,node_color=colorvalues, with_labels = False,node_size=values)
    fig.set_size_inches(5,5)
    

    plt.xlim(.35,.65)
    plt.ylim(.35,.65)
    
    if show ==0:
        plt.show()
    if show ==1:   
        
        plt.savefig(fullpath+name+"-coremem.png",bbox_inches=0,orientation='landscape',pad_inches=0.1,dpi=200)
def subgrouprelations(fullpath,name,show):
   # if (plt.fignum_exists(3)):
   #     pass
   # else:
    
    fig=plt.figure(3)
    plt.clf()
    adjuster =0.25
    nodes=[]
    pairs=[]
    
    FLAG=0
    G = fig.add_subplot(111)
    fig.suptitle(name + " Subgroup Relations")
    G = nx.Graph()
    reader = csv.reader(open(fullpath+"SUBGROUP-RELATIONS.vna",'rb'),delimiter = '\t')
    for row in reader:
        if FLAG >1:
            pairs.append([row[0],row[1]])
        else:
            if FLAG>0:
                if row[0] == 'v1' :
                    FLAG = 2
                else:
                    nodes.append(row[0])
            else:
                if row[0] =='ID':
                    FLAG = 1


               
    for node in nodes:
        
        G.add_node(node)
    G.add_edges_from(pairs)
    neicount = {}
    for node in G.__iter__():
        count = 0
        for n in G.neighbors(node):
            count = count +1
        neicount.update({node:count})
    mapping = sorted(neicount.iteritems(),key=itemgetter(1), reverse = True)
    values = [neicount.get(node,0.25) *25 for node in G.nodes()]
    pos = nx.circular_layout(G)
    pos = nx.spring_layout(G,dim=2,pos=pos)
    
    try1=[]
    try2=[]
    annotes=[]
    for node, posvalue in pos.iteritems():
        
        annotes.append(node)
        try1.append(posvalue[0])
        try2.append(posvalue[1])
    af= plottester2.AnnoteFinder(try1,try2,annotes)
    nx.draw(G,pos,node_color='white', with_labels = False,node_size=values)
    fig.canvas.mpl_connect('button_press_event',af)
    plt.xlim(min(try1)-adjuster,max(try1)+adjuster)
    plt.ylim(min(try1)-adjuster,max(try1)+adjuster)


    if show ==0:
        plt.show()
        
    if show ==1:
        fig.set_size_inches(5,5)
        plt.savefig(fullpath+name+"-subgrouprelations.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)


def subgroupmap(fullpath,show):
    #if (plt.fignum_exists(4)):
    #    pass
    #else:
        
        adjuster =.15
        fig=plt.figure(4)
        plt.clf()
        nodes=[]
        pairs=[]
        FLAG=0
        core = set()
        covers=set()
        G = fig.add_subplot(111)
        fig.suptitle("SubGroup Map")
        
        G = nx.Graph()
        reader = csv.reader(open(fullpath+".vna",'rb'),delimiter = '\t')
        for row in reader:
            if FLAG >1:
                pairs.append([row[0].lstrip('+'),row[1].lstrip('+')])
            else:
                if FLAG>0:
                    if row[0] == 'v1' :
                        FLAG = 2
                    else:
                        if row[0].startswith('++'):
                            covers.add(row[0].lstrip('+'))
                        else:
                            if row[0].startswith('+'):         
                                core.add(row[0].lstrip('+'))
                        nodes.append(row)
                else:
                    if row[0] =='ID':
                        FLAG = 1


                    
        for node in nodes:
            G.add_node(node[0].lstrip('+'))
        G.add_edges_from(pairs)
        neicount = {}
        for node in G.__iter__():
            count = 0
            for n in G.neighbors(node):
                count = count +1
            neicount.update({node:count})
        mapping = sorted(neicount.iteritems(),key=itemgetter(1), reverse = True)
        values = [neicount.get(node,0.25) *25 for node in G.nodes()]
        pos = nx.circular_layout(G)
        pos = nx.spring_layout(G,dim=2,pos=pos)
        try1=[]
        try2=[]
        annotes=[]
        for node, posvalue in pos.iteritems():
            
            annotes.append(node)
            try1.append(posvalue[0])
            try2.append(posvalue[1])
        af= plottester2.AnnoteFinder(try1,try2,annotes)
        nx.draw(G,pos,node_color='white', with_labels = False,node_size=values)
        fig.canvas.mpl_connect('button_press_event',af)
        plt.xlim(min(try1)-adjuster,max(try1)+adjuster)
        plt.ylim(min(try1)-adjuster,max(try1)+adjuster)


        if show ==0:
            plt.show()
            
        if show ==1:
            fig.set_size_inches(5,5)
            plt.savefig(fullpath+"-subgroupmap.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)

#fullnet("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G322/","GANG-G322",0)
#coremem("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G322/","GANG-G322",0)
#subgrouprelations("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G322/","GANG-G322",0)
#subgroupmap("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G422\\"+"ORG-com-2",0)
