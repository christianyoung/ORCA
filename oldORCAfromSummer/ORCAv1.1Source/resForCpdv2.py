#STEP 5

import os
import networkx as nx

def cleanupData(thePath, initFolder,delim):
	inputFile1="RECLIST.dsv"
	inputFile2=""
	oldEdgeList="OLD-EDGELIST.dsv"

	runResRoutine(thePath, initFolder,inputFile1,inputFile2,oldEdgeList,delim)

def cleanUpResExper2(rawResFolder, outResFolder,statFile):
	groupToCountOfUnk = {}
	groupToAssignedNZprob = {}
	groupToAssignedProbThirPlus = {}
	groupToAssignedProbForPlus = {}
	groupToAssignedProbFifPlus = {}
	groupToAssignedProbSixFPlus={}
	groupToAssignedProbSfPlus = {}
	groupToAssignedProbNinetyPlus = {}

	groupToAssignedProb5Plus={}
	groupToAssignedProb10Plus={}
	groupToAssignedProb15Plus={}
	groupToAssignedProb20Plus={}
	groupToAssignedProb25Plus={}
	if not os.path.exists(outResFolder): os.makedirs(outResFolder)
	
	for filename in os.listdir(rawResFolder):
		groupToCountOfUnk[filename]=0.0
		groupToAssignedNZprob[filename]=0.0
		groupToAssignedProbFifPlus[filename]=0.0
		groupToAssignedProbSixFPlus[filename]=0.0
		groupToAssignedProbSfPlus[filename]=0.0
		groupToAssignedProbNinetyPlus[filename]=0.0
		groupToAssignedProbThirPlus[filename] = 0.0
		groupToAssignedProbForPlus[filename] = 0.0
		
		groupToAssignedProb5Plus[filename]=0.0
		groupToAssignedProb10Plus[filename]=0.0
		groupToAssignedProb15Plus[filename]=0.0
		groupToAssignedProb20Plus[filename]=0.0
		groupToAssignedProb25Plus[filename]=0.0

		fullpath=os.path.join(rawResFolder,filename)
		zeroDict={}
		twoDict={}
		with open(fullpath,'r') as fh:
			for line in fh.readlines()[1:]:
				sp=line.split(',')
				t = int(sp[0])
				node = sp[1]
				bound = sp[2].strip('\n').strip('[').strip(']')
				bel = float(bound.split(':')[0])
				if t==0:
					zeroDict[node]=bel
					if float(bel) < 1.0:
						groupToCountOfUnk[filename] += 1.0
				if t==2:
					if bel > zeroDict[node]:
						twoDict[node]=bel
					belVal = float(bel)
					if belVal < 1.0:
						if belVal > 0.0:
							groupToAssignedNZprob[filename]+=1.0
						if belVal >= 0.05:
							groupToAssignedProb5Plus[filename] +=1.0
						if belVal >= 0.1:
							groupToAssignedProb10Plus[filename] +=1.0
						if belVal >= 0.15:
							groupToAssignedProb15Plus[filename] +=1.0
						if belVal >= 0.2:
							groupToAssignedProb20Plus[filename] +=1.0
						if belVal >= 0.25:
							groupToAssignedProb25Plus[filename] +=1.0
						if belVal >= 0.3:
							groupToAssignedProbThirPlus[filename] +=1.0
						if belVal >= 0.4:
							groupToAssignedProbForPlus[filename] +=1.0

						if belVal >= 0.5:
							groupToAssignedProbFifPlus[filename]+=1.0
						if belVal >= 0.6:
							groupToAssignedProbSixFPlus[filename]+=1.0
						if belVal >= 0.75:
							groupToAssignedProbSfPlus[filename]+=1.0
						if belVal >= 0.9:
							groupToAssignedProbNinetyPlus[filename]+=1.0
		with open(os.path.join(outResFolder+"RR."+filename),'w') as fh:
			fh.write("member,belief\n")
			for node in twoDict:
				  fh.write(node+","+str(twoDict[node])+"\n")

	with open(statFile,'w') as fh:
		fh.write("group,cntUnk,numAssignedNzPr,num05,num10,num15,num20,num25,num30,num40,num50,num60,num75,num90,percNz,percFif,perc65,percSf,percNinety\n")
		for filename in groupToCountOfUnk:
			firstPart = filename+','+str(groupToCountOfUnk[filename])+','+str(groupToAssignedNZprob[filename])+','+str(groupToAssignedProb5Plus[filename])+','+str(groupToAssignedProb10Plus[filename])+','+str(groupToAssignedProb15Plus[filename])+','+str(groupToAssignedProb20Plus[filename])+','+str(groupToAssignedProb25Plus[filename])+','+str(groupToAssignedProbThirPlus[filename])+','+str(groupToAssignedProbForPlus[filename])+','+str(groupToAssignedProbFifPlus[filename])+','+str(groupToAssignedProbSixFPlus[filename])+','+str(groupToAssignedProbSfPlus[filename])+','+str(groupToAssignedProbNinetyPlus[filename])+','
			secondPart = str(groupToAssignedNZprob[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbFifPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbSixFPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbSfPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbNinetyPlus[filename]/groupToCountOfUnk[filename])+'\n'
			fh.write(firstPart+secondPart)


	
def cleanUpResExper(rawResFolder, outResFolder,statFile):
	groupToCountOfUnk = {}
	groupToAssignedNZprob = {}
	groupToAssignedProbThirPlus = {}
	groupToAssignedProbForPlus = {}

	groupToAssignedProbFifPlus = {}
	groupToAssignedProbSixFPlus={}
	groupToAssignedProbSfPlus = {}
	groupToAssignedProbNinetyPlus = {}
	
	if not os.path.exists(outResFolder): os.makedirs(outResFolder)
	
	for filename in os.listdir(rawResFolder):
		groupToCountOfUnk[filename]=0.0
		groupToAssignedNZprob[filename]=0.0
		groupToAssignedProbFifPlus[filename]=0.0
		groupToAssignedProbSixFPlus[filename]=0.0
		groupToAssignedProbSfPlus[filename]=0.0
		groupToAssignedProbNinetyPlus[filename]=0.0
		groupToAssignedProbThirPlus[filename] = 0.0
		groupToAssignedProbForPlus[filename] = 0.0

		fullpath=os.path.join(rawResFolder,filename)
		zeroDict={}
		twoDict={}
		with open(fullpath,'r') as fh:
			for line in fh.readlines()[1:]:
				sp=line.split(',')
				t = int(sp[0])
				node = sp[1]
				bound = sp[2].strip('\n').strip('[').strip(']')
				bel = float(bound.split(':')[0])
				if t==0:
					zeroDict[node]=bel
					if float(bel) < 1.0:
						groupToCountOfUnk[filename] += 1.0
				if t==2:
					if bel > zeroDict[node]:
						twoDict[node]=bel
					belVal = float(bel)
					if belVal < 1.0:
						if belVal > 0.0:
							groupToAssignedNZprob[filename]+=1.0
						if belVal >= 0.3:
							groupToAssignedProbThirPlus[filename] +=1.0
						if belVal >= 0.4:
							groupToAssignedProbForPlus[filename] +=1.0

						if belVal >= 0.5:
							groupToAssignedProbFifPlus[filename]+=1.0
						if belVal >= 0.6:
							groupToAssignedProbSixFPlus[filename]+=1.0
						if belVal >= 0.75:
							groupToAssignedProbSfPlus[filename]+=1.0
						if belVal >= 0.9:
							groupToAssignedProbNinetyPlus[filename]+=1.0
		with open(os.path.join(outResFolder+"\\"+"RR."+filename),'w') as fh:
			fh.write("member,belief\n")
			for node in twoDict:
				  fh.write(node+","+str(twoDict[node])+"\n")

	with open(statFile,'w') as fh:
		fh.write("group,cntUnk,numAssignedNzPr,num30,num40,num50,num60,num75,num90,percNz,percFif,perc65,percSf,percNinety\n")
		for filename in groupToCountOfUnk:
			firstPart = filename+','+str(groupToCountOfUnk[filename])+','+str(groupToAssignedNZprob[filename])+','+str(groupToAssignedProbThirPlus[filename])+','+str(groupToAssignedProbForPlus[filename])+','+str(groupToAssignedProbFifPlus[filename])+','+str(groupToAssignedProbSixFPlus[filename])+','+str(groupToAssignedProbSfPlus[filename])+','+str(groupToAssignedProbNinetyPlus[filename])+','
			secondPart = str(groupToAssignedNZprob[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbFifPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbSixFPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbSfPlus[filename]/groupToCountOfUnk[filename])+','+str(groupToAssignedProbNinetyPlus[filename]/groupToCountOfUnk[filename])+'\n'
			fh.write(firstPart+secondPart)

				  
def cleanUpResCpd(rawResFolder, outResFolder,statFile,outFileCompile,facDir,belOut,edgeList,facGraphs,inFile1,inFile2,delim):
	if not os.path.exists(belOut): os.makedirs(belOut)
	if not os.path.exists(facGraphs): os.makedirs(facGraphs)
	if not os.path.exists(outResFolder): os.makedirs(outResFolder)
	
	
	for filename in os.listdir(rawResFolder):
		fullpath=os.path.join(rawResFolder,filename)
		zeroDict={}
		twoDict={}
		with open(fullpath,'r') as fh:
			for line in fh.readlines()[1:]:
				sp=line.split(',')
				t = int(sp[0])
				node = sp[1]
				bound = sp[2].strip('\n').strip('[').strip(']')
				bel = float(bound.split(':')[0])
				if t==0:
					zeroDict[node]=bel
				if t==2:
					if bel > zeroDict[node]:
						twoDict[node]=bel
		with open(os.path.join(outResFolder+"\\"+"RR."+filename),'w') as fh:
			fh.write("member,belief\n")
			for node in twoDict:
				  fh.write(node+","+str(twoDict[node])+"\n")
	memDict = {}
	fDict = {}
	byGang ={}
	byFaction ={}

	nodeToIr = {}
	for filename in os.listdir(outResFolder):
		with open(os.path.join(outResFolder,filename),'r') as fh:
			for line in fh.readlines()[1:]:
				sp =line.split(',')
				mem = sp[0]
				bel = sp[1].strip('\n')
				sp = filename.split('.')
				gang=sp[2]
				# if gang.find("GANG")>-1:
					# if mem in memDict:
						# memDict[mem].append((gang,bel))
					# else:
						# memDict[mem]=[(gang,bel)]
					# if gang in byGang:
						# byGang[gang].append(mem)
					# else:
						# byGang[gang]=[mem]
						
				# else:
				if mem in fDict:
					fDict[mem].append((gang,bel))
				else:
					fDict[mem]=[(gang,bel)]
				if gang in byFaction:
					byFaction[gang].append(mem)
				else:
					byFaction[gang]=[mem]
	orderTuples(memDict)
	orderTuples(fDict)
	alreadyWritten= set()
	with open(outFileCompile,'w') as fh:
		fh.write("org1,probOrg1,org2,probOrg2,")
		with open(inFile1, 'r') as fh2:
			fh.write(fh2.readline())
			for line in fh2.readlines():
		
				sp = line.split(delim)
				node = sp[0]
				if node.isdigit():        
					nodeToIr[node]=sp[0]
				#if node in memDict:
				#    fh.write(listToString(memDict[node])+line)
					if node in fDict:
						if not node in alreadyWritten:
							alreadyWritten.add(node)
							fh.write(listToString(fDict[node])+line)
		
		if not(inFile2==""):
			with open(inFile2, 'r') as fh2:
				for line in fh2.readlines():
					sp = line.split(delim)
				
					node = sp[0]
					if node.isdigit():
						nodeToIr[node]=sp[0]
				
				#if node in memDict:
				#    fh.write(listToString(memDict[node])+line)
						if node in fDict:
							if not node in alreadyWritten:
								alreadyWritten.add(node)

								fh.write(listToString(fDict[node])+line)

	facMemDic = {}
	facStrDic = {}


	for filename in os.listdir(facDir):
		facName = filename.split('.')[0]
		facMemDic[facName] = []
		facStrDic[facName] = {}
		with open(os.path.join(facDir,filename),'r') as fh:
			for num in fh.readlines():
				num=num.strip('\n')
				facMemDic[facName].append(num)
				facStrDic[facName][num]=num+"(1.0)"

	updatedFacs = []
	addedCount = {}
	hasFif = set()
	for fac in byFaction:
		addedCount[fac]=0
		for node in byFaction[fac]:
			ind = 0
			if len(fDict[node])>1:
				if fDict[node][1][0]==fac:
					ind = 1
			bel = str(fDict[node][ind][1])[0:4]

			label = node+"("+bel+")"
			if not node in facMemDic[fac]:
				if float(bel)>0.5:
					if not fac in hasFif:
						hasFif.add(fac)
				if not fac in updatedFacs:
					updatedFacs.append(fac)
				facMemDic[fac].append(node)
				facStrDic[fac][node]=label
				addedCount[fac]+=1
		if fac in updatedFacs:
			with open(os.path.join(belOut,"UPD."+fac+".csv"), 'w') as fh:
					  for node in facStrDic[fac]:
						  fh.write(node+","+facStrDic[fac][node]+"\n")

	subGphDict = {}
	with open(edgeList, 'rb') as fh:
			G = nx.read_edgelist(fh,delimiter=',')
			G.remove_edges_from(G.selfloop_edges())
	for fac in updatedFacs:
		
		subGphDict[fac]=nx.relabel_nodes(G.subgraph(facMemDic[fac]),facStrDic[fac])
		with open(os.path.join(facGraphs,"GPH-"+fac+".csv"),'w') as fh:
			for x,y in subGphDict[fac].edges():
				fh.write(x+","+y+"\n")

	with open(os.path.join(statFile),'w') as fh:
		fh.write("fac,mems,added\n")
		for fac in hasFif:
			fh.write(fac+','+str(len(subGphDict[fac]))+','+str(addedCount[fac])+'\n')


			
	print("done with data cleanup.")
  

def listToString(inList):
    res=inList[0][0]+","+inList[0][1]+","
    if len(inList)==1:
        res=res+"-,-"
    else:
        res=res+inList[1][0]+","+inList[1][1]
      
    return res+","

def orderTuples(theD):
    
    for mem in theD:
        if len(theD[mem])==2:
            first = theD[mem][0]
            second = theD[mem][1]
            if second[1]>first[1]:
                theD[mem]=[second,first]

def ineMk(pth):
	if not os.path.exists(pth): os.makedirs(pth)


def runResRoutine(thePath, initFolder,inputFile1,inputFile2,oldEdgeList,delim):
	fullPath = os.path.join(thePath,initFolder)
	fullpath = fullPath
	rawResFolder = os.path.join(fullPath, "OUT-INTERP")
	
	outResFolder=os.path.join(fullpath,"DISTILLED")
	ineMk(outResFolder)

	statFile = os.path.join(fullpath,"OUT-STAT-FILE.csv")
	outFileCompile = os.path.join(fullpath,"OUT-COMPILED-RES.csv")
	inFile1 = os.path.join(fullPath,inputFile1)
	if inputFile2 == "":
		inFile2= ""
	else:
		inFile2 = os.path.join(fullPath,inputFile2)
	
	facDir = os.path.join(fullPath,"FILES-"+initFolder)
	
	belOut=os.path.join(fullPath,"BEL-OUT")
	ineMk(belOut)

	newEdgeList = "NEW-by-IR-"+oldEdgeList+".csv"

	edgeList = os.path.join(thePath, os.path.join(initFolder,newEdgeList))

	
	facGraphs = os.path.join(fullPath,"ORG-GPHS")
	ineMk(facGraphs)

	cleanUpResCpd(rawResFolder, outResFolder,statFile,outFileCompile,facDir,belOut,edgeList,facGraphs,inFile1,inFile2,delim)
	cleanUpResExper(rawResFolder, outResFolder+"X",statFile+".EXP.csv")
	cleanUpResExper2(rawResFolder, outResFolder+"X",statFile+"2.EXP.csv")
