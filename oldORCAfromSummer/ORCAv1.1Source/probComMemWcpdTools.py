import os
import networkx as nx
import shutil

def runConversion(thePath,initFolder,gangOrFac,delim):
	inputFile1="RECLIST.dsv"
	inputFile2=""
	oldEdgeList="OLD-EDGELIST.dsv"
	gangInputFile="ORGLIST.dsv"

	convertInfoAndRunNewLearner(thePath,initFolder,oldEdgeList,inputFile1,inputFile2,gangInputFile,gangOrFac,delim)    



def combine(inList,folder,outfilename):
	outf = open(os.path.join(folder,outfilename),'w')
	flag = True
	for filename in inList:
		fullpath = os.path.join(folder,filename)
		with open(fullpath,'r') as fh:
			first = fh.readline()
			if flag:
				outf.write(first)
				flag = False
			for line in fh.readlines():
				outf.write(line)
	outf.close()

def combine2(inFolder,outfullpathfilename):
	outf = open(outfullpathfilename,'w')
	flag = True
	for filename in os.listdir(inFolder):
		fullpath = os.path.join(inFolder,filename)
		with open(fullpath,'r') as fh:
			first = fh.readline()
			if flag:
				outf.write(first)
				flag = False
			for line in fh.readlines():
				outf.write(line)
	outf.close()
	
def combineOrg(inFolder,outfullpathfilename):
	outf = open(outfullpathfilename,'w')
	flag = True
	for filename in os.listdir(inFolder):
		fullpath = os.path.join(inFolder,filename)
		with open(fullpath,'r') as fh:
			first = "\t\t"+fh.readline()
			if flag:
				outf.write(first)
				flag = False
			for line in fh.readlines():
				sp=line.split('\t')
				first = sp[0]
				pos1 = len(sp)-2
				pos2 = pos1+1
				first = sp[pos1].strip('\n')
				second = sp[pos2].strip('\n')
				if first.strip(' ').isdigit():
					first = " "
				if second.strip(' ').isdigit():
					second = " "
				toAdd = True
				if first == " " and second == " ":
					toAdd=False
				if toAdd:
					#if sp[0].strip(' ').isdigit():
					outf.write(first+'\t'+second+'\t'+line)
					#else:
					#	outf.write(line)

	outf.close()
	

	
def delim(fn):
    if fn.find(".csv")>-1 or fn.find(".CSV")>-1:
        return ','
    else:
        return '\t'


def getNum(lineList):
    idNum = ""
    cid = ""
    CARD_NO,CONTACT_CARD_ID,NON_OFFENDER_ID,LAST_NME,FIRST_NME,MIDDLE_NME,NICKNAME,BIRTH_DATE,AGE,SEX,HEIGHT,WEIGHT,CONTACT_DATE,STREET_NO,CDIR,STREET_NME,CITY,ST,ZIP_CD,BEAT,RES_STREET_NO,RDIR,RES_STREET_NME,RES_CITY,RST,RES_ZIP_CD,RES_BEAT,IDENTIFICATION_NO,IDENTIFICATION_DESCR,GANG,FACTION_NAME=lineList
    cid = "CC-"+CONTACT_CARD_ID
    if IDENTIFICATION_NO == "" or IDENTIFICATION_NO.find("CLEAR")>-1 or IDENTIFICATION_NO.find("LEAD")>-1:
        idNum = "CC-"+CONTACT_CARD_ID
    else:
        idNum = IDENTIFICATION_NO
        if IDENTIFICATION_NO.find("IR") > -1:
            oldNum= idNum
            idNum = ""
            for char in oldNum:
                if char.isdigit():
                    idNum = idNum+char
        else:
            idNum = "OID-"+idNum

    return idNum, cid
        
def procCont(ccPth,outFileList,outFileOrg):
    ofl = open(outFileList, 'w')
    ofl.write("idNum	cid	NON_OFFENDER_ID	LAST_NME	FIRST_NME	MIDDLE_NME	NICKNAME	NA(CC)	NA(CC)	BIRTH_DATE	AGE	SEX	NA(CC)	CONTACT_DATE	RES_BEAT	NA(CC)	STREET_NO	CDIR	STREET_NME	CITY	ST	ZIP_CD	ID TYPE	GANG	FACTION\n")
    ofo = open(outFileOrg, 'w')
    ofo.write("GANG\tFAC\tidNum\tcid\n")
    for fileName in os.listdir(ccPth):
        fullPathFileName = os.path.join(ccPth,fileName)
        with open(fullPathFileName, 'r') as fh:
            for line in fh.readlines()[1:]:
                lineList = line.split(delim(fullPathFileName))
                CARD_NO,CONTACT_CARD_ID,NON_OFFENDER_ID,LAST_NME,FIRST_NME,MIDDLE_NME,NICKNAME,BIRTH_DATE,AGE,SEX,HEIGHT,WEIGHT,CONTACT_DATE,STREET_NO,CDIR,STREET_NME,CITY,ST,ZIP_CD,BEAT,RES_STREET_NO,RDIR,RES_STREET_NME,RES_CITY,RST,RES_ZIP_CD,RES_BEAT,IDENTIFICATION_NO,IDENTIFICATION_DESCR,GANG,FACTION_NAME=lineList
                idNum,cid= getNum(lineList)
                theTupe = idNum,cid,NON_OFFENDER_ID,LAST_NME,FIRST_NME,MIDDLE_NME,NICKNAME,"NA(CC)","NA(CC)",BIRTH_DATE,AGE,SEX,"NA(CC)",CONTACT_DATE,RES_BEAT,"NA(CC)",STREET_NO,CDIR,STREET_NME,CITY,ST,ZIP_CD,"ID TYPE-"+IDENTIFICATION_DESCR,GANG.strip("\n"),FACTION_NAME.strip("\n")
                orgTupe = GANG.strip("\n"),FACTION_NAME.strip("\n"),idNum,cid
                ofl.write("\t".join(theTupe)+"\n")
                if not(GANG == "") or (FACTION_NAME==""):
                    ofo.write("\t".join(orgTupe)+"\n")
                    

    ofl.close()
    ofo.close()

def convRelList(fullPathRelFile):
    of = open(fullPathRelFile.split('.')[0]+"-OUT.dsv", 'w')

    with open(fullPathRelFile, 'r') as fh:
        of.write(fh.readline())
        for line in fh.readlines():
            sp = line.split("\t")
            of.write("\t".join(("CC-"+sp[0],"CC-"+sp[1])))
    of.close()

def initDirs(thePath,initFolder, arRecLoc,arEdgeLoc,ccRecLoc,ccEdgeLoc):


        comDir = "FILES-"+initFolder
        pth2 = os.path.join(thePath,initFolder)
        if not os.path.exists(pth2): os.makedirs(pth2)

        pth1 = os.path.join(pth2,comDir)

        if not os.path.exists(pth1): os.makedirs(pth1)
        if not os.path.exists(pth1+'c'): os.makedirs(pth1+'c')
        if not os.path.exists(pth1+'cr'): os.makedirs(pth1+'cr')
#        for filename in os.listdir(thePath):
#                if filename[-3:]=="csv" or filename[-3:]=="dsv":
#                        fromFile = os.path.join(thePath,filename)
#                        toFile =os.path.join(pth2,filename)
#                        shutil.copy2(fromFile,toFile)

        combine2(arRecLoc,os.path.join(pth2,"AR-RECLIST.dsv"))
        combine2(arEdgeLoc,os.path.join(pth2,"AR-EDGELIST.dsv"))
        combineOrg(arRecLoc,os.path.join(pth2,"AR-ORGLIST.dsv"))
        combine2(ccEdgeLoc,os.path.join(pth2,"CC-EDGELIST.dsv"))
        procCont(ccRecLoc,os.path.join(pth2,"CC-RECLIST.dsv"),os.path.join(pth2,"CC-ORGLIST.dsv"))


        convRelList(os.path.join(pth2,"CC-EDGELIST.dsv"))
		
        inRecList = ["AR-RECLIST.dsv","CC-RECLIST.dsv"]
        inEdgeList = ["AR-EDGELIST.dsv","CC-EDGELIST-OUT.dsv"]
        inOrgList = ["AR-ORGLIST.dsv","CC-ORGLIST.dsv"]
		
						
        combine(inRecList,pth2,"RECLIST.dsv")
        combine(inEdgeList,pth2,"OLD-EDGELIST.dsv")
        combine(inOrgList,pth2,"ORGLIST.dsv")

        

def addToA2I(pathName,fileName,arrestToIr,delim):
    with open(os.path.join(pathName,fileName), 'r') as fh:
        for line in fh.readlines()[1:]:
            sp = line.split(delim)
            ir = sp[0].strip(' ')
            ar = sp[1].strip(' ')
            if ir.isdigit() or ir.find("CC")>-1 or ir.find("OID")>-1:
                arrestToIr[ar]=ir
                #print ">",ar,"<"

def crNewEdgeList(pathName,oldEdgeList,newEdgeList,arrestToIr,delim):
    bad = 0
    with open(os.path.join(pathName,oldEdgeList),'r') as fh:
        with open(os.path.join(pathName,newEdgeList),'w') as outf:
            for line in fh.readlines():
                sp = line.split(delim)
                node1 = sp[0]
                node2 = sp[1].strip('\n')
                if (node1 in arrestToIr) and (node2 in arrestToIr) and not(node1==node2):
                    outf.write(arrestToIr[node1]+","+arrestToIr[node2]+"\n")
                else:
                    bad+=1
                    #if not(node1 in arrestToIr):
					#    print node1
    G=nx.read_edgelist(os.path.join(pathName,newEdgeList), delimiter=",")
    G.remove_edges_from(G.selfloop_edges())
    print "bad: ",bad
    print "nodes: ",len(G)
    print "edges: ",len(G.edges())
    return G

def sendDocOfSetsToFolder(pathName,folderName,dic):
    fullpath = os.path.join(pathName,folderName)
    for item in dic:
        itemPath = os.path.join(fullpath,item+".csv")
        with open(itemPath,'w') as fh:
            for entry in dic[item]:
                fh.write(entry+"\n")
def ridSpaces(instr):
    res = ""
    for l in instr:
        if not l==" " and not l==r'/' and not l=='&' and not l=='(' and not l==')' and not l==r'"' and not l==',':
            res+= l
    if res.find(r"/")>-1:
	    print ">>>",res
    return res
def getGangAndFacDicts(pathName,fileName,G,gangOrFac,delim):
    gangDic = {}
    facDic = {}
    byGang = {}
    byFac = {}
    with open(os.path.join(pathName,fileName), 'r') as fh:
        for line in fh.readlines()[1:]:
            sp = line.split(delim)
            gang = "GANG-"+ridSpaces(sp[0])
            if gangOrFac == 1:
				fac = "FAC-"+ridSpaces(sp[gangOrFac])
            else:
				fac = "GANG-"+ridSpaces(sp[gangOrFac])
			
            i =2
            flag = False
            if not(delim=='\t') or True:
                #print "non - tab dec"
                while not flag:
                    if sp[i].isdigit() or sp[i].find("CC")>-1 or sp[i].find("OID")>-1:
                        flag=True
                    else:
                        i+=1
            ir = sp[i]
            if len(sp[0])>1 and sp[0].find("UNKNOWN")==-1 and sp[0].find("UNIDENTIFIED")==-1:
                gangDic[ir]=gang
                if not (gang in byGang):
                    byGang[gang]=set()
                byGang[gang].add(ir)
            if len(sp[gangOrFac])>1 and sp[gangOrFac].find("UNKNOWN")==-1 and sp[gangOrFac].find("UNIDENTIFIED")==-1:
                facDic[ir]=fac
            
                if not (fac in byFac):
                    byFac[fac]=set()
                byFac[fac].add(ir)
    return gangDic, facDic, byGang, byFac

def cpdCrInterp(thePath,interpFile, facDic,G):
    with open(os.path.join(thePath,interpFile),'w') as fh:
        fh.write("node,taut,notInGang\n")
        for node in G:
            if node in facDic:
                notInGang = "0"
            else:
                notInGang ="1"
            fh.write(node+",1,"+notInGang+"\n")



def crGphAndFacFilesCPD(thePath,oldEdgeList,newEdgeList,interpFile,comDir,inputFile1,inputFile2,gangInputFile,gangOrFac,delim):
    arrToIr = {}
    addToA2I(thePath,inputFile1,arrToIr,delim)
    print "--",len(arrToIr)
    if not(inputFile2 == ""):
         addToA2I(thePath,inputFile2,arrToIr,delim)
    G=crNewEdgeList(thePath,oldEdgeList,newEdgeList,arrToIr,delim)
    gangDic, facDic, byGang, byFac = getGangAndFacDicts(thePath,gangInputFile,G,gangOrFac,delim)
    sendDocOfSetsToFolder(thePath,comDir,byFac)
    cpdCrInterp(thePath,interpFile,facDic,G)
    return G
   
 
def se(pos,tot):
    mean = float(pos)/float(tot)
    negMean = 1-mean
    meanSq = pow(mean,2)
    negMeanSq = pow(negMean,2)
    invN = 1/float(tot)
    invRtN = 1/pow(float(tot),0.5)
    ssPos = float(pos)*negMeanSq
    ssNeg = float(tot-pos)*meanSq
    sDev = pow(invN * (ssPos+ssNeg),0.5)
    ser = sDev*invRtN
    upper = 1.96*ser
    lower = 1.96*ser#
    upper=min(mean+(1.96*ser),1)
    lower=max(mean-(1.96*ser),0)
    return mean,upper,lower,sDev,ser

def seStr(pos,tot):
    if tot==0:
        return "DIV/0, DIV/0, DIV/0, DIV/0, DIV/0"
    else:
        mean,upper,lower,sDev,ser = se(pos,tot)
        return str(mean)+","+str(upper)+","+str(lower)+","+str(sDev)+","+str(ser)
    
    

def neighInOutComm(node,G,inCommunity):
    inCom = 0
    outCom = 0
    for neigh in G.neighbors(node):
        if neigh in inCommunity:
            inCom +=1
        else:
            outCom +=1
    return inCom,outCom
        

def loadInfo(originalGph, inputDiffuseFile,outCntFile,outFracFile):
    defaultK2=0
    for v in originalGph.nodes():
            deg = len(originalGph.neighbors(v))
            if deg > defaultK2:
                defaultK2=deg
    kStar = defaultK2

    inCommunity = set()
    with open(inputDiffuseFile, 'r') as fh:
        for line in fh.readlines():
            sp = line.split("\n")
            inCommunity.add(sp[0])

    inOutDict = {}
    for node in originalGph:
        inOutDict[node]=neighInOutComm(node,originalGph,inCommunity)
    sumPosCases = []
    sumTotCases =[]
    posCases = {}
    totCases = {}

    for i in range(0,kStar+1):
        sumPosCases.append(0)
        sumTotCases.append(0)
        posCases[i]=0
        totCases[i]=0
        

    fracTot =[]
    sumFracTot = []
    fracPos =[]
    sumFracPos = []

    for i in range(0,101):
        fracTot.append(0.0)
        sumFracTot.append(0.0)
        fracPos.append(0.0)
        sumFracPos.append(0.0)


    for node in originalGph:
        deg = len(originalGph.neighbors(node))
        if deg >0:         
			signals = inOutDict[node][0]
			frac  = int(100.0*float(signals)/float(deg))
			fracTot[frac]+=1

			for i in range(0,frac+1):
				sumFracTot[i]+=1
				if node in inCommunity:
					sumFracPos[i]+=1
			for i in range(0,signals+1):
				sumTotCases[i]+=1
				if node in inCommunity:
					sumPosCases[i]+=1
			if not (signals in totCases):
				totCases[signals]=0
				posCases[signals]=0
			totCases[signals]+=1
			if node in inCommunity:
				posCases[signals]+=1
				fracPos[frac]+=1

      
    flag = False
    for signals in range(1,kStar+1):
        if posCases[signals]>0:
            flag=True
    if flag:

        with open(outCntFile, 'w') as fh:
            fh.write("signals,pos,tot,sumPos,sumTot,signals,sumMean,upper,lower,sumSd,sumSe\n")
            for signals in totCases:
                outStr=str(signals)+","+str(posCases[signals])+","+str(totCases[signals])+","+str(sumPosCases[signals])+","+str(sumTotCases[signals])+","+str(signals)+","+seStr(sumPosCases[signals],sumTotCases[signals])+"\n"
                if outStr.find("DIV/0")==-1:
                    if signals >0:
                        fh.write(outStr)
        useFrac = False
        if useFrac:
                        with open(outFracFile, 'w') as fh:
                                fh.write("frac,pos,tot,sumPos,sumTot,frac,sumMean,upper,lower,sumSd,sumSe\n")
                                for frac in range(1,101):
                                        outStr=str(frac)+","+str(fracPos[frac])+","+str(fracTot[frac])+","+str(sumFracPos[frac])+","+str(sumFracTot[frac])+","+str(frac)+","+seStr(sumFracPos[frac],sumFracTot[frac])+"\n"
                                        if outStr.find("DIV/0")==-1:
                                                fh.write(outStr)

def convertInfoAndRunNewLearner(thePath,initFolder,oldEdgeList,inputFile1,inputFile2,gangInputFile,gangOrFac,delim):
        #newEdgeList =os.path.join(thePath,os.path.join(initFolder,newEdgeList)
        #interpFile =os.path.join(thePath,os.path.join(initFolder,interpFile)
        comDir = "FILES-"+initFolder
        interpFile = "ATTRIB"+initFolder+".csv"
        newEdgeList = "NEW-by-IR-"+oldEdgeList+".csv"
        thePath = os.path.join(thePath,initFolder)
        sourceFolder = os.path.join(thePath,"SOURCE")
        if not os.path.exists(sourceFolder): os.makedirs(sourceFolder)

        G = crGphAndFacFilesCPD(thePath,oldEdgeList,newEdgeList,interpFile,comDir,inputFile1,inputFile2,gangInputFile,gangOrFac,delim)
        for filename in os.listdir(thePath+"\\"+comDir):
                inputDiffuseFile = os.path.join(thePath+"\\"+comDir,filename)
                outCntFile = os.path.join(thePath+"\\"+comDir+"cr","CNT-"+filename+".csv")
                outFracFile = os.path.join(thePath+"\\"+comDir+"cr","FRAC-"+filename+".csv")
                loadInfo(G, inputDiffuseFile,outCntFile,outFracFile)
        createLbFiles(os.path.join(thePath,comDir+"cr"),os.path.join(thePath,comDir+"c"))
        crSource(os.path.join(thePath,comDir+'c'),os.path.join(thePath,comDir),sourceFolder)
        interpFolder = os.path.join(thePath,"INTERP")
        ruleFolder=os.path.join(thePath,"RULES")
        if not os.path.exists(interpFolder): os.makedirs(interpFolder)
        if not os.path.exists(ruleFolder): os.makedirs(ruleFolder)
        
        crInterp(os.path.join(thePath,comDir),interpFolder,G)
        crRules(os.path.join(thePath,comDir+"c"),ruleFolder)
        


def createLbFiles(thePath,newFolder):
    for filename in os.listdir(thePath):
        fullpath = os.path.join(thePath,filename)
        sp = filename.split("-")
        outpath = os.path.join(newFolder,sp[0]+"."+sp[1]+"-"+sp[2]+".LB.csv")
        outf = open(outpath,'w')
        with open(fullpath,'r') as fh:
            lowerLast = 0.0
            for line in fh.readlines()[1:]:
                sp = line.split(',')
                firstCol = sp[0]
                lower = float(sp[8])
                if lowerLast > lower:
                    lower = lowerLast
                lowerLast = lower
                if int(firstCol)>0:
                    outf.write(firstCol+","+str(lower)+"\n")
        outf.close()

def ineMk(pth):
        if not os.path.exists(pth): os.makedirs(pth)

                
#Creates source files for use with fixed point operator
def crSource(newFolder,gangFolder,sourceFolder):
    good = set()
    useful = os.listdir(newFolder)
    for gang in useful:
        sp = gang.split('.')
        if not (sp[1] in good):
            good.add(sp[1]+".csv")

    for filename in os.listdir(gangFolder):
        fullpath = os.path.join(gangFolder,filename)
        if filename in good:
            #print "ok"
            outf = open(os.path.join(sourceFolder,"FP."+filename+".csv"),'w')
        
            with open(fullpath, 'r') as fh:
                for gang in fh.readlines():
                    outf.write(gang.strip("\n")+",0\n")
            outf.close()            
           
def crRules(newFolder,ruleFolder):
    for filename in os.listdir(newFolder):
        sb = {}
        with open(os.path.join(newFolder,filename), 'r') as fh:
            for line in fh.readlines():
                sp = line.split(',')
                sb[sp[0]]=sp[1].strip("\n")
        with open(ruleFolder+"\\RULES."+filename,'w') as fh:
            fh.write("f,gnode,inbound,deltaT,signals,outbound,rawRatio,totalSupportInstances,positiveSupportInstances,stdDev,stdErr\n")
            head = "notInGang,taut,[1.0:1.0],1,"
            tail=":1.0],0,0,0,0,0\n"
            for signals in sb:
                fh.write(head+signals+",["+sb[signals]+tail)
    print("done with rule creation.")

#Do not use this for CPD data.
def crInterp(gangFolder,interpFolder,G):
    for filename in os.listdir(gangFolder):
        curSet = set()
        with open(os.path.join(gangFolder,filename),'r') as fh:
            for line in fh.readlines():
                curSet.add(line.strip('\n'))
        with open(os.path.join(interpFolder,"INTERP."+filename),'w') as fh:
            fh.write("node,taut,notInGang\n")
            for node in G:
                if node in curSet:
                    notInGang = "0"
                else:
                    notInGang ="1"
                fh.write(node+",1,"+notInGang+"\n")

