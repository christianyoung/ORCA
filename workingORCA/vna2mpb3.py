import csv
import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import plot6
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg, NavigationToolbar
from matplotlib.backend_bases import key_press_handler
import os
import plottester2
import random
import numpy as np
from operator import itemgetter
import sys
from Tkinter import *

global af
global menuName
global root
global mainFrame
global entryWidget5

menuName = "Full Map"


def submit(delIR):
    global af
    af.findIR(delIR)
    #root_window.destroy()

##def create_find_frame():
##    global find
##    irs=StringVar()
##    
##    find = Frame(root)
##    find['borderwidth'] = 2
##    find.grid(column=0, row=0,padx=20, pady =5)
##    entryLabel5= Label(find)
##    entryLabel5.grid(column=0, row=1)
##    del_window_label = Label(find, wraplength = 300, text='Submit IR numbers separated by comma.')
##    del_window_label.grid(column=0, row=0, columnspan=3)
##    entryLabel5["text"] = "IR Numbers:"
##
##    entryWidget5 = Entry(find, textvariable =irs)
##    entryWidget5.grid(column=1, row=1)
##    entryWidget5["width"] = 50
##    Submit = Button(find, text = "Submit", command=  lambda: submit(irs.get()), width=10)
##    Submit.grid(column=1, row=2, pady=10, padx=10)
##
##def findOnTop():
##    global find
##    global mainFrame
##    mainFrame.forget()
##    root.wm_title("Find IR Numbers")
##    find.pack()
##
##def mainOnTop():
##    global find
##    global mainFrame
##    global menuName
##    find.forget()
##    root.wm_title(menuName)
##    mainFrame.pack()
    
def fullnet(fullpath,name,show):
    global af
    global entryWidget5


    menuName = name + " Fullmap"

    
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
    reader3 = csv.reader(open(fullpath+"CONNECTORS-"+name+".csv",'rb'),delimiter=',')
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
    
    #plt.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
    plt.xlim(min(try1),max(try1))
    plt.ylim(min(try1),max(try1))




    def on_key_event(event):
        print('you pressed %s'%event.key)
        key_press_handler(event, canvas, toolbar)

    
    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    


    if show == 0:
        root = Tk()
        root.wm_title(menuName)
        # a tk.DrawingArea
        mainFrame = Frame(root)
        topFrame = Frame(mainFrame)
        bottomFrame = Frame(mainFrame)

        
            
        canvas = FigureCanvasTkAgg(fig, master=topFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        fig.canvas.mpl_connect('button_press_event',af)
        canvas.mpl_connect('key_press_event', on_key_event)
        canvas.mpl_connect('button_press_event',af)
        handles =[]
        labels = []
        for key, value in colors.items():
            labels.append(key)
            random.seed(value)
            tempcol = [random.random(),random.random(),random.random()]
            p = plt.Rectangle((0,0),1,1,fc=tempcol)
            handles.append(p)
        fig.legend(handles,labels, loc = "right", prop = {'size':7}).draggable()
                
        toolbar = NavigationToolbar2TkAgg( canvas, root )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        
        entryLabel5= Label(bottomFrame)
        entryLabel5["text"] = "Find IR:"
        entryWidget5 = Entry(bottomFrame)
        entryWidget5["width"] = 30
        findButton = Button(bottomFrame, text = "Find", command=  lambda: submit(entryWidget5.get()))
        clearButton = Button(master=bottomFrame, text='Clear', command= af.clear)
        quitButton = Button(master=bottomFrame, text='Quit', command=_quit)
        
        entryLabel5.pack(side=LEFT)
        entryWidget5.pack(side=LEFT)
        findButton.pack(side=LEFT)
        clearButton.pack(side=LEFT)
        quitButton.pack(side=LEFT)
        topFrame.pack()
        bottomFrame.pack()
        mainFrame.pack()
        #create_find_frame()
        #find.forget()
        #mainOnTop()
        mainloop()
    if show == 1:
        fig.set_size_inches(8,8)
    
        plt.savefig(fullpath+name+"-fullnet.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)
        
    
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.



      
        
        
    
def coremem(fullpath,name,show):
    global af
    global menuName


    menuName = name + " Core Members"

    
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
    reader3 = csv.reader(open(fullpath+"CONNECTORS-"+name+".csv",'rb'),delimiter=',')
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

    nx.draw(G,pos,node_color=colorvalues, with_labels = False,node_size=values)
    fig.set_size_inches(5,5)
    

    plt.xlim(.35,.65)
    plt.ylim(.35,.65)


    def on_key_event(event):
        print('you pressed %s'%event.key)
        key_press_handler(event, canvas, toolbar)


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


    if show ==0:
        root = Tk()
        root.wm_title(menuName)
        # a tk.DrawingArea
        mainFrame = Frame(root)
        topFrame = Frame(mainFrame)
        bottomFrame = Frame(mainFrame)
        canvas = FigureCanvasTkAgg(fig, master=topFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        fig.canvas.mpl_connect('button_press_event',af)
        canvas.mpl_connect('key_press_event', on_key_event)
        canvas.mpl_connect('button_press_event',af)
        handles =[]
        labels = []
        for key, value in colors.items():
            labels.append(key)
            random.seed(value)
            tempcol = [random.random(),random.random(),random.random()]
            p = plt.Rectangle((0,0),1,1,fc=tempcol)
            handles.append(p)
        fig.legend(handles,labels, loc = "right", prop = {'size':7}).draggable()
        toolbar = NavigationToolbar2TkAgg( canvas, root )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        
        entryLabel5= Label(bottomFrame)
        entryLabel5["text"] = "Find IR:"
        entryWidget5 = Entry(bottomFrame)
        entryWidget5["width"] = 30
        findButton = Button(bottomFrame, text = "Find", command=  lambda: submit(entryWidget5.get()))
        clearButton = Button(master=bottomFrame, text='Clear', command= af.clear)
        quitButton = Button(master=bottomFrame, text='Quit', command=_quit)
        
        entryLabel5.pack(side=LEFT)
        entryWidget5.pack(side=LEFT)
        findButton.pack(side=LEFT)
        clearButton.pack(side=LEFT)
        quitButton.pack(side=LEFT)
        topFrame.pack()
        bottomFrame.pack()
        mainFrame.pack()
        #create_find_frame()
        #find.forget()
        #mainOnTop()
        mainloop()
    if show ==1:   
        plt.savefig(fullpath+name+"-coremem.png",bbox_inches=0,orientation='landscape',pad_inches=0.1,dpi=200)
    

    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.
    
        
        
def subgrouprelations(fullpath,name,show):
   # if (plt.fignum_exists(3)):
   #     pass
   # else:
    global af
    global menuName


    menuName = name + " Subgroup Relations"

    
    fig=plt.figure(3)
    plt.clf()
    adjuster =0.25
    nodes=[]
    pairs=[]
    
    FLAG=0
    G = fig.add_subplot(111)
    fig.suptitle(name + " Subgroup Relations")
    G = nx.Graph()
    reader = csv.reader(open(fullpath+"SUBGROUP-RELATIONS-"+name+".vna",'rb'),delimiter = '\t')
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

    plt.xlim(min(try1)-adjuster,max(try1)+adjuster)
    plt.ylim(min(try1)-adjuster,max(try1)+adjuster)



    def on_key_event(event):
        print('you pressed %s'%event.key)
        key_press_handler(event, canvas, toolbar)


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    


    if show ==0:
        root = Tk()
        root.wm_title(menuName)
        # a tk.DrawingArea
        mainFrame = Frame(root)
        topFrame = Frame(mainFrame)
        bottomFrame = Frame(mainFrame)
        canvas = FigureCanvasTkAgg(fig, master=topFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        fig.canvas.mpl_connect('button_press_event',af)
        canvas.mpl_connect('key_press_event', on_key_event)
        canvas.mpl_connect('button_press_event',af)
    
        toolbar = NavigationToolbar2TkAgg( canvas, root )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        
        entryLabel5= Label(bottomFrame)
        entryLabel5["text"] = "Find IR:"
        entryWidget5 = Entry(bottomFrame)
        entryWidget5["width"] = 30
        findButton = Button(bottomFrame, text = "Find", command=  lambda: submit(entryWidget5.get()))
        clearButton = Button(master=bottomFrame, text='Clear', command= af.clear)
        quitButton = Button(master=bottomFrame, text='Quit', command=_quit)
        
        entryLabel5.pack(side=LEFT)
        entryWidget5.pack(side=LEFT)
        findButton.pack(side=LEFT)
        clearButton.pack(side=LEFT)
        quitButton.pack(side=LEFT)
        topFrame.pack()
        bottomFrame.pack()
        mainFrame.pack()
        #create_find_frame()
        #find.forget()
        #mainOnTop()
        mainloop()
    if show ==1:
        fig.set_size_inches(5,5)
        plt.savefig(fullpath+name+"-subgrouprelations.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)




        
def subgroupmap(fullpath,show):
    #if (plt.fignum_exists(4)):
    #    pass
    #else:
        global af
        global menuName


        menuName = "SubGroup Map"

    
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

        plt.xlim(min(try1)-adjuster,max(try1)+adjuster)
        plt.ylim(min(try1)-adjuster,max(try1)+adjuster)



        def on_key_event(event):
            print('you pressed %s'%event.key)
            key_press_handler(event, canvas, toolbar)

        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        


        if show ==0:
            root = Tk()
            root.wm_title(menuName)
            # a tk.DrawingArea
            mainFrame = Frame(root)
            topFrame = Frame(mainFrame)
            bottomFrame = Frame(mainFrame)
            canvas = FigureCanvasTkAgg(fig, master=topFrame)
            canvas.show()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            
            fig.canvas.mpl_connect('button_press_event',af)
            canvas.mpl_connect('key_press_event', on_key_event)
            canvas.mpl_connect('button_press_event',af)
        
            toolbar = NavigationToolbar2TkAgg( canvas, root )
            toolbar.update()
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
            
            entryLabel5= Label(bottomFrame)
            entryLabel5["text"] = "Find IR:"
            entryWidget5 = Entry(bottomFrame)
            entryWidget5["width"] = 30
            findButton = Button(bottomFrame, text = "Find", command=  lambda: submit(entryWidget5.get()))
            clearButton = Button(master=bottomFrame, text='Clear', command= af.clear)
            quitButton = Button(master=bottomFrame, text='Quit', command=_quit)
            
            entryLabel5.pack(side=LEFT)
            entryWidget5.pack(side=LEFT)
            findButton.pack(side=LEFT)
            clearButton.pack(side=LEFT)
            quitButton.pack(side=LEFT)
            topFrame.pack()
            bottomFrame.pack()
            mainFrame.pack()
            #create_find_frame()
            #find.forget()
            #mainOnTop()
            mainloop()
            
        if show ==1:
            fig.set_size_inches(5,5)
            plt.savefig(fullpath+"-subgroupmap.png",bbox_inches='tight',orientation='landscape',pad_inches=0.1)


            



#fullnet("C:/Users/x48661/Desktop/ORCAJUNK/test/ORG-RES/GANG-G322/","GANG-G322",0)
#coremem("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G322/","GANG-G322",0)
#subgrouprelations("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G322/","GANG-G322",0)
#subgroupmap("C:/Users/x48661/Desktop/test/ORG-RES/GANG-G422\\"+"ORG-com-2",0)
