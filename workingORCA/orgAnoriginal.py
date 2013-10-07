import os
import networkx as nx
#import pylab
import community as cty
import ltDecomp3 as ltd

def removeFileExtensions(s):
        while (len(s) - string.rfind(s,'.')) < 5:
            s = os.path.splitext(s)[0]
        return s

def analyze(thePath,initFolder,delim):
	inputFile1="RECLIST.dsv"
	inputFile2=""
	oldEdgeList="OLD-EDGELIST.dsv"


	analyzeAllOrgs(thePath,initFolder,oldEdgeList,inputFile1,inputFile2,delim)         


def addToI2S(thePath, filename,irToStr,delim):
		with open(os.path.join(thePath,filename),'r') as fh:
				title = ",".join(fh.readline().strip("\n").split(delim))
				for line in fh.readlines():
						sp=line.split(delim)
						node = sp[0]
						if node.isdigit() or node.find('CC')>-1 or node.find('OID')>-1:
								irToStr[node]=",".join(line.strip('\n').split(delim))
		return title

def irToInfo(ir,irToStr,delim):
		ir = ir.strip('+').split('(')[0]
		info =irToStr[ir].split(',')
		return (info[3],info[4],info[0]+','+info[3]+','+info[4]+','+info[5]+','+info[6]+','+info[16]+','+info[17]+','+info[18])

def retPnum(ir,pd):
		ir = ir.strip('+').split('(')[0]
		return pd[ir]
		
def retHead():
		return "IR,Last Name,First Name,Nickname,Middle,St. Num,Dir.,St.Name"

def retLine(ir,irToStr,pd,coreList,coverSet,G,delim):
		ir = ir.strip('+')
		ir2=ir.split('(')[0]
		
		p = str(retPnum(ir2,pd))+','
		cm = ","
		
		if ir in coreList:
				if ir in coverSet:
						cm=" ++YES AND COVERS,"
				else:
						cm=" +YES,"
		theTupe=irToInfo(ir,irToStr,delim)
		return (theTupe[0],theTupe[1],p+cm+theTupe[2]+'\n')

def crFile(irToStr,pd,coreList,coverSet,G,outFileFullPath,delim):
		tl = []
		for ir in G:
				tl.append(retLine(ir,irToStr,pd,coreList,coverSet,G,delim))
		tl.sort()
		with open(outFileFullPath,'w') as fh:
				fh.write("Prob.,Core Member,"+retHead()+'\n')
				for item in tl:
						fh.write(item[2])
				  

def outputFacFile(thePath, filename,title,coreNodes,coreCovers,modNum,G,comDict,nodeListDict,probDict,irToStr):
		tupeList = []
		tot=0
		certain =0 
		ninetyToOne =0
		seventyFiveToNinety =0
		fifToSeventyFive=0
		twentyFiveToFif =0
		lowProb=0
		for node in G:
				irn=node.split('(')[0]
				c = comDict[node]
				#print node,c,filename

				size = len(nodeListDict[c])
				prob = float(probDict[irn])
				isCore = " "
				if c in coreNodes:
						if node in coreNodes[c]: # or node.split("(")[0] in coreNodes[c]:
								if node in coreCovers[c]:# or node.split("(")[0] in coreCovers[c]:
										isCore="YES AND COVERS"
								else:
										isCore="YES"
				text = irToStr[irn]
				tupeList.append((size,c,prob,isCore,text))
				tot+=1
				if prob == 1.0:
						certain +=1
				elif prob >= 0.9:
						ninetyToOne +=1
				elif prob >= 0.75:
						seventyFiveToNinety +=1
				elif prob >= 0.5:
						fifToSeventyFive +=1
				elif prob >= 0.25:
						twentyFiveToFif +=1
				else:
						lowProb += 1
						
		tupeList.sort(reverse=True)
		
#        with open(os.path.join(thePath,filename),'w') as fh:
#                fh.write("Sub-Faction Number, Probability of Faction Membership, Core Member,"+title+"\n")
#                for tupe in tupeList:
#                        fh.write(str(tupe[1])+','+str(tupe[2])+','+str(tupe[3])+','+str(tupe[4])+'\n')
		with open(os.path.join(thePath,"STATS-"+filename),'w') as fh:
				fh.write("DEGREE OF MEMBERSHIP:\n")
				fh.write("Certain (admitted), "+str(certain)+'\n')
				fh.write("Over 0.9 but under 1.0, "+str(ninetyToOne)+'\n')
				fh.write("Over 0.75 but under 0.9, "+str(seventyFiveToNinety)+'\n')
				fh.write("Over 0.5 but under 0.75, "+str(fifToSeventyFive)+'\n')
				fh.write("Over 0.25 but under 0.5, "+str(twentyFiveToFif)+'\n')
				fh.write("Under 0.25:, "+str(lowProb)+'\n')
				fh.write("----\n")
				fh.write("TOTAL, "+str(tot)+'\n')
				fh.write("\n\n=====================\n\n\n")
				modString = ""
				if modNum < 0.2:
					  modString = "(organization has POORLY-DEFINED subgroup structure)"  
				elif modNum < 0.4 and modNum >=0.2:
					  modString = "(organization has ILL-DEFINED subgroup structure)"  
				elif modNum >= 0.4 and modNum < 0.6:
					  modString = "(organization has a WELL-DEFINED subgroup structure)"  
				elif modNum >= 0.6:
					  modString = "(organization has VERY WELL-DEFINED subgroup structure)"  
				fh.write("NETWORK SUB-GROUP STRUCTURE EVALUATION:\n")
				fh.write("Network modularity,"+str(modNum)+"\n")
				fh.write(modString+"\n")

		return tot, certain, ninetyToOne, seventyFiveToNinety, fifToSeventyFive, twentyFiveToFif, lowProb

def doesCover(listOfConcern, G):
		res = set()
		usedG = G.subgraph(listOfConcern)
		checkSize = len(usedG)
		for node in listOfConcern:
				if (1+len(usedG.neighbors(node)))==checkSize:
						res.add(node)
		return res
		   
def greedyPick(listOfConcern, G, probDict):
		#print "gr pick"
		usedG = G.subgraph(listOfConcern)
		usedSet = set(listOfConcern)
		resultSet = set()
		left = len(usedG)
		while left >0:
				print "loop: "+str(left)
				curBest = "@"
				curBestScore = 0
				bestCovered = set()
				for node in usedSet:
						covered = set(usedG.neighbors(node))
						covered.add(node)
						covered = covered.intersection(usedSet)
						beats = False
						if len(covered) > curBestScore:
								beats = True
						elif len(covered) == curBestScore:
								if probDict[node] < probDict[curBest]:
										beats=True
										#print "tie breaker"
								
						if beats:
								curBestScore=len(covered)
								bestCovered = covered.copy()
								curBest = node
				resultSet.add(curBest)
				left = left-len(bestCovered)
				usedSet = usedSet.difference(bestCovered)
		return resultSet
						
def ineMk(pth):
		if not os.path.exists(pth): os.makedirs(pth)


def orgAnMain(thePath,graphFile,vertFile,theName,outFolder,fullNetName,inFile1,inFile2,ssOut,projName,allOrgFolder,orgFolder,orgToSubOrg,subOrgToMem,memsToSub,orgToAllMem,ndpth,delim):
		maxNonDivSize = 25
		rootDir = os.path.join(thePath,projName)

		irToStr = {}

		firstLine=addToI2S(rootDir,inFile1,irToStr,delim)
		if not(inFile2 == ""):
			 firstLine = addToI2S(rootDir,inFile2,irToStr,delim)
		initStr = firstLine
		orgToAllMem[theName]=[]
		divUp = True
		
		ineMk(thePath)
		thePath=os.path.join(rootDir,allOrgFolder)
		ineMk(thePath)
		thePath=os.path.join(thePath,orgFolder)
		ineMk(thePath)
		ineMk(os.path.join(thePath,outFolder))
		probDict = {}
		outpath = os.path.join(thePath, outFolder)

		minComMem =5
		pd2 = {}
		with open(os.path.join(rootDir,vertFile),'r') as fh:
				for line in fh.readlines():
						sp=line.split(',')
						vert = sp[1].split('(')[0]
						orgToAllMem[theName].append(sp[1].strip('\n'))
						prob = float(sp[1].split('(')[1].strip('\n').strip(')'))
						probDict[vert]=prob
						pd2[sp[1].strip('\n')]=prob

		with open(os.path.join(rootDir,graphFile),'rb') as fh:
				G = nx.read_edgelist(fh, delimiter=',')
				G.remove_edges_from(G.selfloop_edges())
		if len(G) <= maxNonDivSize:
				divUp = False
				orgToSubOrg[theName]=[theName]
				subOrgToMem[theName]=set()
				for node in G:
						subOrgToMem[theName].add(node)
						#if not node in memsToSub:
						#        memsToSub[node.split('(')[0]]=[theName]
						if not node.split('(')[0] in memsToSub:
								memsToSub[node.split('(')[0]]=[theName]
						else:
								if not theName in memsToSub[node.split('(')[0]]:
									memsToSub[node.split('(')[0]].append(theName)
									#print "more than 1:",node, memsToSub[node.split('(')[0]]
						
		#nx.write_pajek(G,os.path.join(outpath,fullNetName))
		GtoND(G,os.path.join(outpath,fullNetName)+".nd",ndpth,irToStr,initStr)
		comDict = cty.best_partition(G)
		modNum = cty.modularity(comDict,G)
		nodeListDict = {}
		for vert in comDict:
				com = comDict[vert]
				if not com in nodeListDict:
						nodeListDict[com]=[]
				nodeListDict[com].append(vert)


		overallCoreDict = nx.core_number(G)
		maxCoreG = 0
		overallCoreNodes = []
		overallCoreNodesAndNeigh =[]
		for node in G:
				if overallCoreDict[node] > maxCoreG:
						 maxCoreG=overallCoreDict[node]

		for node in G:
				if overallCoreDict[node]==maxCoreG:
						if not node in overallCoreNodes:
								overallCoreNodes.append(node)
								overallCoreNodesAndNeigh.append(node)
								for neigh in G.neighbors(node):
										if not neigh in overallCoreNodesAndNeigh:
												overallCoreNodesAndNeigh.append(neigh)
		maxLen = 15
		coreMemGraph = nx.Graph()
		if (len(G) < maxLen) or (not divUp):
				coreMemGraph = G.copy()
		else:
				coreMemGraph = G.subgraph(overallCoreNodesAndNeigh)

		doesCoverMainCore = doesCover(overallCoreNodes, G)
		renameDict={}
		for node in overallCoreNodes:
				newname = ""
				if node in doesCoverMainCore:
						newname ="++"+str(node)
				else:
						newname="+"+str(node)
				renameDict[node]=newname
		
		coreMemGraph=nx.relabel_nodes(coreMemGraph,renameDict)
		#nx.write_pajek(coreMemGraph,os.path.join(outpath,"CORE-MEM-.net"))
		GtoND(coreMemGraph,os.path.join(outpath,"CORE-MEM-.net")+".nd",ndpth,irToStr,initStr)

		outFileFullPath=os.path.join(outpath,"CORE-MEM-ROLLUP.csv")
		crFile(irToStr,probDict,overallCoreNodes,doesCoverMainCore,coreMemGraph,outFileFullPath,delim)

		subDict = {}
		coreNodes = {}
		shellDict = {}
		coreCovers = {}
		c=1
		inSub = []

		if divUp:
				comSizeList = []
				for com in nodeListDict:
					comSizeList.append((len(nodeListDict[com]),com))
				comSizeList.sort(reverse=True)
				for csz,com in comSizeList:
						if len(nodeListDict[com])>= minComMem:
								subDict[c]=G.subgraph(nodeListDict[com])
								newName = theName+"-SUB-"+str(c)
								orgToSubOrg[theName].append(newName)
								subOrgToMem[newName]=set()
								for node in subDict[c]:
										inSub.append(node)
										subOrgToMem[newName].add(node)
										#if not node in memsToSub:
										#        memsToSub[node.split('(')[0]]=newName
										if not node.split('(')[0] in memsToSub:
												memsToSub[node.split('(')[0]]=[newName]
										else:
											if not newName in memsToSub[node.split('(')[0]]:									
													memsToSub[node.split('(')[0]].append(newName)
                                									#print "more than 1:",node, memsToSub[node.split('(')[0]]
													

								shellDict[c]=nx.core_number(subDict[c])
								maxCore = 0
								for node in shellDict[c]:
										if shellDict[c][node]> maxCore:
												maxCore = shellDict[c][node]
								renameDict = {}
								coreNodes[c] = []
								for node in shellDict[c]:
										if shellDict[c][node] == maxCore:
												coreNodes[c].append(node)
								#coreCovers[c]=greedyPick(coreNodes[c],subDict[c],pd2)
								coreCovers[c]=doesCover(coreNodes[c],subDict[c])
								for node in coreNodes[c]:
										if node in coreCovers[c]:            
												renameDict[node]="++"+str(node)
										else:
												renameDict[node]="+"+str(node)
										
								subDict[c]=nx.relabel_nodes(subDict[c],renameDict)
								#nx.write_pajek(subDict[c],os.path.join(outpath,"ORG-com-"+str(c)+".net"))
								GtoND(subDict[c],os.path.join(outpath,"ORG-com-"+str(c)+".net")+".nd",ndpth,irToStr,initStr)
								outFileFullPath=os.path.join(outpath,"ORG-com-"+str(c)+"-ROLLUP.csv")
								crFile(irToStr,probDict,coreNodes[c],coreCovers[c],subDict[c],outFileFullPath,delim)
								c+=1
				newName = theName+"-SUB-OTHERS"
				orgToSubOrg[theName].append(newName)
				subOrgToMem[newName]=set()

				for node in G:
						if not (node in inSub):
							subOrgToMem[newName].add(node)
							# if not node in memsToSub:
							#         memsToSub[node.split('(')[0]]=newName
							if not node.split('(')[0] in memsToSub:
                                                                        #print "<",node,">"
                                                                        #print "<",node.split('(')[0],">"
                                                                        #print "---"
									memsToSub[node.split('(')[0]]=[newName]
							else:
									if not newName in memsToSub[node.split('(')[0]]:
										memsToSub[node.split('(')[0]].append(newName)	
               									#print "more than 1:",node, memsToSub[node.split('(')[0]]
									 

		nums = outputFacFile(outpath,ssOut,firstLine,coreNodes,coreCovers,modNum,G,comDict,nodeListDict,probDict,irToStr)
		crFile(irToStr,probDict,overallCoreNodes,doesCoverMainCore,G,os.path.join(outpath,ssOut),delim)
		print "done with analysis of ", theName
		return irToStr

def graphSubOrgs(subOrgToMem, memsToSub,overallGraphFileLocation, overallGraphFile,ndpth,irToStr):
		graphPath = os.path.join(overallGraphFileLocation, overallGraphFile)
		neighComsOfNode = {}
		with open(graphPath,'rb') as fh:
				G = nx.read_edgelist(fh,delimiter=',')
				G.remove_edges_from(G.selfloop_edges())
		ResG=nx.Graph()
		edgeDict = {}
		for sub in subOrgToMem:
				ResG.add_node(sub)
				edgeDict[sub]={}
		for sub in edgeDict:
				for node in subOrgToMem[sub]:
						neighComsOfNode[node]=[]

						for neigh in G.neighbors(node.split('(')[0]):
								if neigh in memsToSub:
									for neighCom in memsToSub[neigh]:
										if not (neighCom in neighComsOfNode[node]) and not (neighCom in memsToSub[node.split('(')[0]]):
												neighComsOfNode[node].append(neighCom)
										
										if not (neighCom in memsToSub[node.split('(')[0]]):
												if not(neighCom in edgeDict[sub]):
														edgeDict[sub][neighCom]=0
												edgeDict[sub][neighCom]+=1
						#for inGroup in memsToSub[node]:
					#		if inGroup in neighComsOfNode[node]:
					#			neighComsOfNode[node].remove(inGroup)
										
		for sub in edgeDict:
				for neighSub in edgeDict[sub]:
						if not( (((sub,neighSub) in ResG.edges() ) or ((neighSub,sub) in ResG.edges() ) )):
								ResG.add_edge(sub,neighSub, weight = edgeDict[sub][neighSub])
		cnNodeTupeList = []
		for node in neighComsOfNode:
				newTupe = (len(neighComsOfNode[node])+len(memsToSub[node.split('(')[0]]),node)
				cnNodeTupeList.append(newTupe)
		cnNodeTupeList.sort(reverse=True)
		cnFullPath = os.path.join(overallGraphFileLocation, "CN-OVERALL.csv")
		with open(cnFullPath, 'w') as fh:
				fh.write("IR,Num. Rel. Sub-Groups,Member Sub-Groups,,,,,,Connected Sub-Group(s)\n")
				for tupe in cnNodeTupeList:
						curNode = tupe[1].split('(')[0]			
						fh.write(str(curNode)+','+str(tupe[0])+',')#+str(memsToSub[curNode])+',')
						for inGroup in memsToSub[curNode]:
							fh.write(str(inGroup)+',')
                                                for i in range(1,7-len(memsToSub[curNode])):
							fh.write(",")
													
						for gang in neighComsOfNode[tupe[1]]:
								fh.write(str(gang)+',')
						fh.write('\n')
		subRelGphPth=os.path.join(overallGraphFileLocation, "SUB-REL-OVERALL.net")
		#nx.write_pajek(ResG,subRelGphPth)
		GtoND2(ResG,subRelGphPth+".nd",ndpth)#,irToStr)
		return ResG,neighComsOfNode
		
def subGroupRelGraph(groupName,ResG,orgToSubOrg,thePath,subOrgToOrg,nextStep,ncon,orgToALlMem,memsToSub,ndpth,irToStr):

		vertexList = []
		minLinks = 3
		dest3 = os.path.join(os.path.join(os.path.join(thePath,"ORG-RES"),groupName),"BULLETS."+groupName+".csv")
		used = set()
		bullets = open(dest3,'w')
		for item in orgToSubOrg[groupName]:
				vertexList.append(item)
		for sub in orgToSubOrg[groupName]:
				bullets.write(sub+" is strongly connected ("+str(minLinks)+"+ links) to:\n")
				conCount =0 
				for neigh in ResG.neighbors(sub):
						wt=  ResG.get_edge_data(sub, neigh, {"weight":0}).get("weight", 1)
						if wt >minLinks-1:
							 conCount += 1					
							 bullets.write(",,"+neigh+"  ("+str(wt)+" connections) \n")
						if not (neigh in vertexList):
								vertexList.append(neigh)
						if nextStep:
								for affil in orgToSubOrg[subOrgToOrg[neigh]]:
										if not (affil in vertexList):
												vertexList.append(affil)
				if conCount == 0:
					bullets.write(",,(relatively isolated - all other groups are connected with less than "+str(minLinks)+" links)\n")
				bullets.write("\n")
		bullets.close()

		SubNet = ResG.subgraph(vertexList)
		dest = os.path.join(os.path.join(os.path.join(thePath,"ORG-RES"),groupName),"SUBGROUP-RELATIONS."+groupName+".net")
		
		#nx.write_pajek(SubNet,dest)
		GtoND2(SubNet,dest+".nd",ndpth)#,irToStr)
		dest2 = os.path.join(os.path.join(os.path.join(thePath,"ORG-RES"),groupName),"CONNECTORS."+groupName+".csv")
		relList = []
		for node in orgToALlMem[groupName]:
				if node in ncon:
						sz = len(ncon[node])+len(memsToSub[node.split('(')[0]])
						if sz > 1:
								theTupe = (sz,node,ncon[node])
								relList.append(theTupe)
		relList.sort(reverse=True)
		with open(dest2,'w') as fh:
				fh.write("IR,Num. Groups,Member Sub-Groups,,,,,,Conn. Sub-Groups\n")
				for tupe in relList:
						curNode = 	tupe[1].split('(')[0]			
						fh.write(str(curNode)+','+str(tupe[0])+',')
						for inGroup in memsToSub[curNode]:
							fh.write(str(inGroup)+',')
                                                for i in range(1,7-len(memsToSub[curNode])):
							fh.write(",")

						for gang in tupe[2]:
								fh.write(str(gang)+',')
						fh.write('\n')

		return SubNet
											  
def GtoND(G,fulloutpath,ndpth,irToStr,initStr):
	fulloutpath = removeFileExtensions(fulloutpath)+".vna"
	beginPart=removeFileExtensions(fulloutpath)
	fullSeedOutPath =  beginPart+"-SEED.csv"
	if len(G)>1 and len(G.edges())>=1:
		labelList =beginPart.split('\\')
		labelList2 = labelList[len(labelList)-1].split('-')
		label = labelList2[len(labelList2)-2]
		ltd.ltdForCpd(G,label,fullSeedOutPath)

	with open(fulloutpath, 'w') as fh:
		fh.write("*Node data\n")
		fh.write("ID\tCORE\tCOVERS,"+initStr)#INFO\n")
		for node in G:
			label=node.replace("*","+")
			covers = "NO"
			core = "NO"
			if label.find("++")>-1:
				covers = "YES-COV"
			if label.find("+")>-1:
				core = "YES-CORE"
			fh.write(label+"\t"+core+"\t"+covers+"\t"+irToStr[label.split('(')[0].strip('+')]+"\n")
		fh.write("*Tie data\n")
		fh.write("v1\tv2\n")
		for edge in G.edges():
			fh.write(edge[0].replace("*","+")+"\t"+edge[1].replace("*","+")+"\n")
			fh.write(edge[1].replace("*","+")+"\t"+edge[0].replace("*","+")+"\n")
			
	with open(fulloutpath+"BATCH.txt", 'w') as fh:
		fh.write("Loadvna "+fulloutpath+"\n")
		fh.write("COLORNODESBYATTR CORE\n")
		fh.write("COLORNODESBYATTR COVERS\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")

		fh.write("Savejpg "+fulloutpath+".jpg\n")
		fh.write("Close\n")

	with open(fulloutpath+"BATCH-jo.txt", 'w') as fh:
		fh.write("Loadvna "+fulloutpath+"\n")
		fh.write("COLORNODESBYATTR CORE\n")
		fh.write("COLORNODESBYATTR COVERS\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")
		
		fh.write("Savejpg "+fulloutpath+".jpg\n")

def GtoND2(G,fulloutpath,ndpth):
	beginPart=removeFileExtensions(fulloutpath)
#	fullSeedOutPath =  beginPart+"-SEED.csv"
#	if len(G)>1 and len(G.edges())>=1:
#		ltd.ltdForCpd(G,beginPart,fullSeedOutPath)
	fulloutpath = beginPart+".vna"
	with open(fulloutpath, 'w') as fh:
		fh.write("*Node data\n")
		fh.write("ID\tCORE\tCOVERS,INFO\n")
		for node in G:
			label=node.replace("*","+")
			covers = "NO"
			core = "NO"
			if label.find("++")>-1:
				covers = "YES-COV"
			if label.find("+")>-1:
				core = "YES-CORE"
			fh.write(label+"\t"+core+"\t"+covers+"\t"+"\n")
		fh.write("*Tie data\n")
		fh.write("v1\tv2\n")
		for edge in G.edges():
			fh.write(edge[0].replace("*","+")+"\t"+edge[1].replace("*","+")+"\n")
			fh.write(edge[1].replace("*","+")+"\t"+edge[0].replace("*","+")+"\n")
			
	with open(fulloutpath+"BATCH.txt", 'w') as fh:
		fh.write("Loadvna "+fulloutpath+"\n")
		fh.write("COLORNODESBYATTR CORE\n")
		fh.write("COLORNODESBYATTR COVERS\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")
		fh.write("Runlayout\n")

		fh.write("Savejpg "+fulloutpath+".jpg\n")
		fh.write("Close\n")

	with open(fulloutpath+"BATCH-jo.txt", 'w') as fh:
		fh.write("Loadvna "+fulloutpath+"\n")
		fh.write("COLORNODESBYATTR CORE\n")
		fh.write("COLORNODESBYATTR COVERS\n")
		fh.write("Runlayout\n")
		

		
	#os.system(ndpth+" BATCH "+fulloutpath+"BATCH.txt")
	
	

def analyzeAllOrgs(thePath, initFolder,oldEdgeList,inFile1,inFile2,delim):
		#rootDir = thePath
		#thePath = os.path.join(thePath, initFolder)
		overallGraphFile= "NEW-by-IR-"+oldEdgeList+".csv"

		orgToSubOrg = {}
		subOrgToMem = {}
		orgToAllMem = {}
		irToStr = {}
		memsToSub={}
		projName= initFolder
		allOrgFolder = "ORG-RES"
		#inFile1 ="arrest-dat1.csv"
		#inFile2 ="arrest-dat2.csv"
		ndpth = os.path.join(thePath,"netdraw.exe")
		for filename in os.listdir(os.path.join(thePath,os.path.join(initFolder,"ORG-GPHS"))):
				orgFolder = filename[4:][:-4]
				orgToSubOrg[orgFolder]=[]
				graphFile = os.path.join("ORG-GPHS",filename)
				vertFile=os.path.join("BEL-OUT","UPD."+filename[4:])
				theName= orgFolder
				outFolder = ""
				fullNetName = orgFolder+"-fullNet.net"
				ssOut = orgFolder+"-overallRollup.csv"
				irToStr = orgAnMain(thePath,graphFile,vertFile,theName,outFolder,fullNetName,inFile1,inFile2,ssOut,projName,allOrgFolder,orgFolder,orgToSubOrg,subOrgToMem,memsToSub,orgToAllMem,ndpth,delim)
		ResG,ncon=graphSubOrgs(subOrgToMem, memsToSub,os.path.join(thePath,initFolder), overallGraphFile,ndpth,irToStr)
		subOrgToOrg={}
		for org in orgToSubOrg:
				for sub in orgToSubOrg[org]:
						subOrgToOrg[sub]=org
		for groupName in orgToSubOrg:
				subGroupRelGraph(groupName,ResG,orgToSubOrg,os.path.join(thePath,initFolder),subOrgToOrg,False,ncon,orgToAllMem,memsToSub,ndpth,irToStr)
		G= nx.read_edgelist(os.path.join(thePath,os.path.join(initFolder,overallGraphFile)),delimiter=',')
		G.remove_edges_from(G.selfloop_edges())
		print len(G)
		print len(G.edges())
		
