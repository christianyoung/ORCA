#STEP 4
#ML-FP: MANCaLog Fixed Point Operator v2
#(cpd) next step is resForCpd.py

import networkx as nx
import os

def cpdFp(thePath,initFolder):
        oldEdgeList="OLD-EDGELIST.dsv"

        runFpForCpd(thePath,initFolder,oldEdgeList)
        print "completed all fp runs for cpd."

class mlFp :
        unmod = {}
        I={}
        diffusDict = {}
        originalGph = nx.Graph()
        inputRuleFile = ""
        inputDiffuseFile = ""
        outInterpFile = ""
                        
        outputProgramFile = ""
                        

        inputGraphFile = ""
        

        ruledir=""
        sourcedir=""
        inputAttributeFile = ""
        verbose = False
        minVerbose = True
        veryVebose = False
        formulaDict ={}
        #self.attribDict has nodes as keys and sets of labels as values
        #self.attribKey is used when opening the file
        #self.allLabels is the set of all non-fluent labels
        attribDict = {}
        attribKey={}
        allLabels = set()


        #List of removed rules
        rulesRemoved = []

        #Program: list of rule tuples
        P = []

        #Records current qual sets
        curQualDict = {}

        #Dictionary where the keys are non-fluent formula strings and values are
        #nodes who satisfy that formula given the current self.attribDict.
        formulaDict = {}

        #This maps fluent label bounds (as tuples) to dictionaries (indexed by time point)
        #and maps to sets of vertices that satisfy that bound at that time.
        fluentBoundDict = {}

        #Dictionary that takes gnode-formulas as values and maps to dictionaries
        #that map nodes to sets of nodes.  The sets of nodes are the in-coming
        #neighbors of the key vertex that satisfy the gnode-formula
        eligSets = {}

        #Time is numbered starting at 0.  self.numDats is one more than tmax.
        numDats = 3


        
        def runTheFp(self,gangName):

                
                #runBoundFixer(0.033,6,0.3,0)
                self.runFixedPoint(0.4)
                if self.minVerbose:
                        print "done with fixed point for ",gangName


        def loadProgram(self, programFile):
                #global self.P
                #global self.eligSets
                with open(programFile, 'r') as fh:
                        for line in fh.readlines()[1:]:
                                if self.veryVebose:
                                        print line
                                self.readRulePart(line)
                                
                for rule in self.P:
                        self.updateEligSets(rule)
                #rint "!!",self.P

        #Resets interpretation
        def resetInterp(self):
                #global I
                #global unmod
                self.I = {}
                self.unmod={}

                for t in range(0, self.numDats):
                        self.I[t]={}
                        self.unmod[t]={}
                        for v in self.originalGph.nodes():
                                self.unmod[t][v]=True
                                if v in self.diffusDict:
                                        if t >= self.diffusDict[v]:
                                                self.I[t][v] = (1.0,1.0)
                                                self.unmod[t][v]=False
                                        else:
                                                if t==0:
                                                        self.I[t][v] = (0.0,0.0)
                                                        self.unmod[t][v]=False
                                                else:
                                                        self.I[t][v] = (0.0,1.0)
                                elif t==0:
                                        self.I[t][v]=(0.0,0.0)
                                        self.unmod[t][v]=False
                                else:
                                        self.I[t][v]=(0.0,1.0)



        #Creates the self.eligSets datastructure
        def updateEligSets(self,rule):
                #global self.eligSets
                f = rule[0]
                gnode = rule[1]
                if not (gnode in self.eligSets):
                        self.eligSets[gnode] = {}
                gnodeSet = self.formulaDict[gnode]
                for v in self.formulaDict[f]:
                        if not(v in self.eligSets[gnode]):
                                self.eligSets[gnode][v] = set()
                                for vPrime in self.originalGph.neighbors(v):#predecessors(v):
                                        if vPrime in gnodeSet:
                                                self.eligSets[gnode][v].add(vPrime)


        def updateFluentBoundDict(self):
                #global self.fluentBoundDict
                for bnd in self.fluentBoundDict:
                        self.fluentBoundDict[bnd]={}
                        for t in self.I:
                                self.fluentBoundDict[bnd][t]=set()
                for t in self.I:
                        for v in self.I[t]:
                                bndPrime = self.I[t][v]
                                for bnd in self.fluentBoundDict:
                                        if self.isBoundContained(bnd,bndPrime):    
                                                self.fluentBoundDict[bnd][t].add(v)
                                                

        def formulaStringToSet(self,formulaString):
                res = set()
                fsList = formulaString.split('&')
                for item in fsList:
                        res.add(item.strip())
                return res

        def intervalStringToTuple(self,intervalString):
                ivlList=intervalString.split(':')
                first = float(ivlList[0][1:])
                second = float(ivlList[1][:-1])
                return (first,second)

        def checkFormulaAndAdd(self,f):
                #global self.formulaDict
                if not(f in self.formulaDict):
                        fLabelSet = self.formulaStringToSet(f)
                        nodeSet = set()
                        for node in self.attribDict:
                                if fLabelSet.issubset(self.attribDict[node]):
                                        nodeSet.add(node)
                        self.formulaDict[f]=nodeSet
                
        #Steps back the lower part of inbound for a rule (returns new rule)
        def stepBackRule(self,r, amount):
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup = r
                low, hi = inbound
                newlow = max(0.0,float(low)-float(amount))
                newbound = (newlow, hi)
                return (f,gnode,newbound,deltaT,signals,outbound,rawRatio,totSup,posSup)

        #Steps back lower part of inbound for all rules in the program
        def stepBackAll(self,amount):
                #global self.P
                newP = []
                for r in self.P:
                        newRule = self.stepBackRule(r,amount)
                        newP.append(newRule)
                        self.reprocessRule(newRule)
                self.P = newP



        #Reads a single line of the rule file
        def readRulePart(self,line):
                #global self.formulaDict
                #global self.fluentBoundDict
                spLine = line.split(',')
                f = spLine[0].strip()
                self.checkFormulaAndAdd(f)    
                gnode = spLine[1].strip()
                self.checkFormulaAndAdd(gnode)
                gnodeLabelSet = self.formulaStringToSet(spLine[1])
                inbound = self.intervalStringToTuple(spLine[2])
                if not(inbound in self.fluentBoundDict):
                        self.fluentBoundDict[inbound]={}
                        
                deltaT = int(spLine[3])
                signals = int(spLine[4])
                outbound = self.intervalStringToTuple(spLine[5])
                rawRatio = float(spLine[6])
                totSup = int(spLine[7])
                posSup = int(spLine[8])
                
                
                r = (f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup)
                self.P.append(r)
                #print ">>>",r
                return r

        #Reprocess rule if the inbound has changed.
        def reprocessRule(self,r):
                #global self.fluentBoundDict
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup = r
                if not(inbound in self.fluentBoundDict):
                        self.fluentBoundDict[inbound]={}


                

        #Takes rule and outputs it to string
        def ruleToString(self,r):
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup =r
                inl,inh =inbound
                outl,outh=outbound
                res=str(f)+","+str(gnode)+",["+str(inl)+":"+str(inh)+"],"+str(deltaT)+","+str(signals)+",["+str(outl)+":"+str(outh)+"],"+str(rawRatio)+","+str(totSup)+","+str(posSup)+"\n"
                return res

        #Wirtes exisitng program to file
        def programToFile(self,fileName):
                with open(fileName, 'w') as fh:
                        fh.write("f,gnode,inbound,deltaT,signals,outbound,rawRatio,totalSupportInstances,positiveSupportInstances\n")
                        for r in self.P:
                                fh.write(ruleToString(r))


        #Implements the Elig function from the paper
        def elig(self,v,gnode):
                return self.eligSets[gnode][v]

        #Checks bound containment
        def isBoundContained(self,outsideBound, insideBound):
                res = True
                if outsideBound[0]>insideBound[0]:
                        res=False
                if outsideBound[1]<insideBound[1]:
                        res=False
                return res
         

        #Implements qual, takes an "elig" set as an argument and a bound
        def qual(self,v,gnode,t, bnd):
                tupe = (v,gnode,t,bnd)
                if not (tupe in self.curQualDict):
                        
                        self.curQualDict[tupe]=self.eligSets[gnode][v].intersection(self.fluentBoundDict[bnd][t])
                        
                        
                return self.curQualDict[tupe]

        def bound(self,r,v,t):
                res = (0.0,1.0)
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup = r
                qu = self.qual(v,gnode,t,inbound)
                #el = elig(v,gnode)
                #and (j==len(el)):
                
                if (signals==len(qu)):
                        return outbound
                else:
                        return res

        def tts(self,v,r):
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup = r
                if v in self.formulaDict[f]:
                        return range(deltaT,self.numDats)
                else:
                        return range(0,0)

        def resultingBound(self,origBound, bound2):
                changeNote = False
                a,b = origBound
                ap,bp = bound2
                an = max(a,ap)
                bn = min(b,bp)
                if an != a:
                        changeNote = True
                if bn != b:
                        changeNote=True
                        
                return ((an,bn),changeNote)

        def isGoodBound(self,bound):
                res = True
                low,hi = bound
                if hi<low:
                        res = False
                if hi < 0:
                        res = False
                if low < 0:
                        res = False
                return res

        def processRuleForVertexAndTime(self,r,v,t):
                #global I
                #global unmod
                removeFlag = False
                f,gnode,inbound,deltaT,signals,outbound,rawRatio,totSup,posSup = r
                
                curBound = self.I[t][v]
                
                boundToIntersect = self.bound(r,v,t-deltaT)
                newBound = self.resultingBound(curBound,boundToIntersect)
                if self.verbose:
                        if boundToIntersect[0] >0:
                                print "processing rule:,",self.ruleToString(r)
                                print "for node ",v," at time ",t
                                print "old bound: ",curBound
                                print "bound to intersect: ",boundToIntersect
                if self.isGoodBound(newBound[0]):
                        self.I[t][v]=newBound[0]
                        if self.verbose and self.I[t][v][0]>0:
                                print "the new bound for I(",t,")(",v,") is: ",self.I[t][v]
                else:
                        if self.minVerbose:
                                print "*** Removing Rule: ",ruleToString(r)," (causes inconsistency)"
                                print "    old bound:",curBound
                                print "    bound assigned by new rule:",boundToIntersect
                        removeFlag = True
                if newBound[1]:
                        self.unmod[t][v]=False
                        if self.verbose:
                                print "a change has occured"
                #if self.verbose:
                        #print "---"
                        #print " "

                return (newBound[1], removeFlag)

        def processRule(self,r):
                changeNote = False
                removeRule = False
                for v in self.originalGph.nodes():
                        for t in self.tts(v,r):
                                resNote = self.processRuleForVertexAndTime(r,v,t)
#                               if self.I[t][v][0] >0 and self.I[t][v][0]<1:
#                                       print ">>>>> ",self.I[t][v]
#                                       print asdasfdasdf

##                print "!!!!!"
##              for t in self.I:
##                      for v in self.I[t]:
##                              if self.I[t][v]>0 and self.I[t][v]<1:
##
##                                      print ">>>> ",self.I[t][v]
##              print "!!!!!"

##              print asdkhasdjkfkse

                                
                                if resNote[0]:

                                        changeNote=True
                                if resNote[1]:
                                        removeRule = True
                return (changeNote,removeRule)

        def gammaOneIter(self):
                if self.verbose:
                        print " "
                        print "Starting a new application of gamma."
                #global self.curQualDict
                #global self.rulesRemoved
                #global self.P
                changeNote = False
                rulesRemovedFlage = False
                
                for r in self.P:
                        if self.veryVebose:
                                print "Processing rule:",r
                        resNote = self.processRule(r)
                        if resNote[0]:
                                changeNote=True
                        if resNote[1]:
                                rulesRemovedFlage = True
                                self.rulesRemoved.append(r)
                                self.P.remove(r)

                if changeNote:
                        self.updateFluentBoundDict()
                self.curQualDict = {}
                return (changeNote,self.rulesRemoved)

        def convergeGamma(self):
                if self.minVerbose:
                        print "Starting fixed point convergence."
                self.updateFluentBoundDict()
                keepGoing = True
                rulesOut=False
                count = 0
                while keepGoing and not(rulesOut):
                        theIter =  self.gammaOneIter()
                        keepGoing = theIter[0]
                        rulesOut = theIter[1]
                        count += 1
                        if self.minVerbose:
                                print "Finished iteration ",count
                if rulesOut:
                        if self.minVerbose:
                                print "*** PREMATURE STOPPAGE: RULES REMOVED. ***"

        def outputInterp(self,outfile):
                with open(outfile, 'w') as fh:
                        fh.write("t,v,bnd\n")
                        for t in self.I:
                          for v in self.I[t]:
                                  fh.write(str(t)+","+str(v)+",["+str(self.I[t][v][0])+":"+str(self.I[t][v][1])+"]\n")

                                  
        def procUnmod(self):
                res = []
                for t in self.unmod:
                        for v in self.unmod[t]:
                                if self.unmod[t][v]:
                                        tupe = (t,v)
                                        res.append(tupe)
                return res

        def countAvg(self,t,thresh):
                res = 0
                for v in self.I[t]:
                        av = 0.5*(self.I[t][v][0]+self.I[t][v][1])
                        if av >= thresh:
                                res += 1
                return res

        def countLeast(self,t,thresh):
                res = 0
                for v in self.I[t]:
                        if self.I[t][v][0] >= thresh:
                                res += 1
                return res
                
        def countGreatest(self,t,thresh):
                res = 0
                for v in self.I[t]:
                        if self.I[t][v][1] >= thresh:
                                res += 1
                return res

        def sumAvg(self,t):
                res = 0
                for v in self.I[t]:
                        av = 0.5*(self.I[t][v][0]+self.I[t][v][1])
                        res += av
                return res

        def sumLeast(self,t):
                #print self.I
                res = 0
                for v in self.I[t]:
                        res += self.I[t][v][0] 
                return res
                
        def sumGreatest(self,t):
                res = 0
                for v in self.I[t]:
                        res += self.I[t][v][1] 
                return res

        #Checks if goal is met in convergegnce of the fixed point
        #Goal amount is the amount of the goal
        #Option specifies goal type, thresh is only nused for "count" goals
        #OPtion is 1-3 for count avg,least,greatest and 4-6 for sum of the same.
        def goalmet(self,goalAmount,goalType,thresh):
                res = False
                goalTime = self.numDats-1
                self.resetInterp()
                self.convergeGamma()
                actualAmount = 0
                if goalType == 1:
                        actualAmount = countAvg(goalTime,thresh)
                elif goalType == 2:
                        actualAmount = countLeast(goalTime,thresh)
                elif goalType == 3:
                        actualAmount = countGreatest(goalTime,thresh)
                elif goalType == 4:
                        actualAmount = sumAvg(goalTime)
                elif goalType == 5:
                        actualAmount = sumLeast(goalTime)
                else:
                        actualAmount = sumGreatest(goalTime)
                if actualAmount >= goalAmount:
                        res = True
                return (res,goalAmount-actualAmount)

        #Iteratively resets lower bound on all rules until an aggregate goal
        #is met.
        def findLower(self,stepBackAmount,goalAmount,goalType,thresh,lowestPoss):
                meetsGoal = False
                diff = 0
                maxCount = 1+int((1-lowestPoss)/stepBackAmount)
                count = 0
                while not(meetsGoal) and (count < maxCount):
                        count += 1
                        meetsGoal,diff = goalmet(goalAmount,goalType,thresh)
                        if not(meetsGoal):
                                stepBackAll(stepBackAmount)
                return (diff,count)
                        
                        


        def dispRes(self,thresh):
                if self.minVerbose:
                        perc = thresh*100
                        percStr = "("+str(perc)+"%)"
                        print "Aggregates at tmax:"
                        print "----------------------------"
                        print "   Count avg ",percStr," : ",self.countAvg(self.numDats-1,thresh)
                        print "   Count least ",percStr," : ",self.countLeast(self.numDats-1,thresh)
                        print "   Count greatest ",percStr," : ",self.countGreatest(self.numDats-1,thresh)
                        #print "   Sum avg : ",self.sumAvg(self.numDats-1)
                        print "   Sum least : ",self.sumLeast(self.numDats-1)
                        print "   Sum greatest : ",self.sumGreatest(self.numDats-1)
                        print " "
                print "done with this fp run."
                print "======================================================="
                print ""


        def runFixedPoint(self,thresh):
                self.loadProgram(self.inputRuleFile)
                if self.minVerbose:
                        print "Program loaded."
                self.resetInterp()
                self.convergeGamma()
                #print I
                self.outputInterp(self.outInterpFile)

                self.unmodList = self.procUnmod()

                self.dispRes(thresh)
##              print "!!!!!"
##              for t in self.I:
##                      for v in self.I[t]:
##                              if self.I[t][v][0]>0 and self.I[t][v][0]<1:
##
##                                      print ">>>> ",self.I[t][v]
##              print alsdjsalkd


                
        def runBoundFixer(self,stepBackAmount, goalAmount,thresh,lowestPoss):
                self.loadProgram(inputRuleFile)
                self.findLower(stepBackAmount,goalAmount,2,thresh,lowestPoss)
                self.programToFile(outputProgramFile)
                self.dispRes(thresh)


        
        def __init__(self,inputGraphFile, ruledir, sourcedir,gof,inputAttribFile,outInterpPath,outPgmPath,numDats):
                self.numDats = numDats
                self.inputGraphFile = inputGraphFile
                self.ruledir = ruledir
                self.sourcedir=sourcedir
                count = 0
                
                for filename in os.listdir(self.ruledir):
                        rulepath=os.path.join(self.ruledir,filename)
                        
                        #Below should be changed for your rule files
                        sp = filename.split(".")
                        gang = sp[2]
                        
                        #CHANGE THIS LINE FOR INDIV INTERP FILES
                        self.inputAttributeFile=inputAttribFile#os.path.join(inputAttribFile,"INTERP."+gang+".csv")
                        
                        #THIS IS FOR INDIVDUAL SOURCE FILES
                        sourcepath=os.path.join(self.sourcedir,"FP."+gang+".csv.csv")
                        
                        self.inputRuleFile = rulepath
                        self.inputDiffuseFile = sourcepath
                        self.outInterpFile = os.path.join(outInterpPath,"FP."+gang+".csv")
                        self.formulaDict ={}
                        #attribDict has nodes as keys and sets of labels as values
                        #attribKey is used when opening the file
                        #allLabels is the set of all non-fluent labels
                        self.attribDict = {}
                        self.attribKey={}
                        self.allLabels = set()


                            #List of removed rules
                        self.rulesRemoved = []

                            #Program: list of rule tuples
                        self.P = []

                            #Records current qual sets
                        self.curQualDict = {}

                            #Dictionary where the keys are non-fluent formula strings and values are
                            #nodes who satisfy that formula given the current attribDict.
                        self.formulaDict = {}

                            #This maps fluent label bounds (as tuples) to dictionaries (indexed by time point)
                            #and maps to sets of vertices that satisfy that bound at that time.
                        self.fluentBoundDict = {}

                            #Dictionary that takes gnode-formulas as values and maps to dictionaries
                            #that map nodes to sets of nodes.  The sets of nodes are the in-coming
                            #neighbors of the key vertex that satisfy the gnode-formula
                        self.eligSets = {}

                        #Time is numbered starting at 0.  numDays is one more than tmax.
                        self.numDays = numDats


                                        
                        self.outputProgramFile = os.path.join(outPgmPath,"OUTRULES."+gang+".csv")
                        if self.minVerbose:
                                print "Loading network"

                        #Imports the underlying network
                        with open(self.inputGraphFile, 'rb') as fh:
                                self.originalGph = nx.read_edgelist(fh,delimiter=',')#,create_using=nx.DiGraph())
                                self.originalGph.remove_edges_from(self.originalGph.selfloop_edges())

                        #Imports fluent facts

##      orginal that gives error when running data from district 3&4
##                      self.diffusDict = {}
##                      with open(self.inputDiffuseFile, 'r') as fh:
##                              for line in fh.readlines()[1:]:
##                                      ls = line.split(",")
##                                      self.diffusDict[ls[0]]=int(ls[1])


##      my modifications let see if this works
                        self.diffusDict = {}
                        try:
                                with open(self.inputDiffuseFile, 'r') as fh:
                                        for line in fh.readlines()[1:]:
                                                ls = line.split(",")
                                                self.diffusDict[ls[0]]=int(ls[1])
                        except IOError:
                                with open(self.inputDiffuseFile, 'w') as fh:
                                        fh.write('')
                                        fh.close()
                                        print 'We created the', self.inputDiffuseFile, 'file.'
                                print "Oops!!! This file", self.inputDiffuseFile, "isn't created yet."
                        #Sets up the interpretation.
                        #Here it just maps time points and vertices
                        #to intervals as we consider only one fluent label
                        self.I = {}
                        self.unmod={}

                        if self.minVerbose:
                                print "Initial files loaded"
                        

                        #Imports the attribute file.
                        with open(self.inputAttributeFile, 'r') as fh:
                                theLines = fh.readlines()
                                i = 0
                                theKeys = theLines[0].split(",")[1:]
                                for item in theKeys:
                                        item=item.strip()
                                        self.attribKey[i]=item
                                        self.allLabels.add(item)
                                        i = i+1
                                
                                for line in theLines[1:]:
                                        ls = line.split(",")
                                        if ls[0] in self.originalGph:
                                                self.attribDict[ls[0]]=set()
                                                for item in enumerate(ls[1:]):
                                                        index = item[0]
                                                        if item[1].strip().find("1")>-1:
                                                                self.attribDict[ls[0]].add(self.attribKey[index])




                        if self.minVerbose:
                                print "Running fixed point."

                        self.runTheFp(gang)
                        count +=1
                        print "PROCESSED NUMBER: "+str(count)+", "+gang

def ineMk(pth):
        if not os.path.exists(pth): os.makedirs(pth)

                
def runFpForCpd(thePath,initFolder,oldEdgeList):
        newEdgeList = "NEW-by-IR-"+oldEdgeList+".csv"
        fullPath = os.path.join(thePath, initFolder)
        inputGraphFile = os.path.join(thePath, os.path.join(initFolder,newEdgeList))#Full path of the edgelist
        ruledir=os.path.join(fullPath,"RULES")#Path where all rules are kept

        sourcedir = os.path.join(fullPath,"SOURCE")#Full path for source files
        #inputAttributeFile = os.path.join(fullPath,"INTERP") #Full path for INTERPS (uncomment this line for non-CPD data)
        inputAttributeFile = os.path.join(fullPath,"ATTRIB"+initFolder+".csv")#Comment out this one (for CPD only)
        
        outInterpPath = os.path.join(fullPath,"OUT-INTERP")#Output path for OUTPUT-interps
        ineMk(outInterpPath)
        outRules = os.path.join(fullPath,"OUT-RULES")#Output path for output-rules (likely will produce nothing)
        ineMk(outRules)
        numDats=3

        fp = mlFp(inputGraphFile, ruledir, sourcedir,initFolder,inputAttributeFile,outInterpPath,outRules,numDats)
