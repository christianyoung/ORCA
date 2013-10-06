import probComMemWcpdTools as analy
import mlFp as fixpt
import resForCpdv2 as res
import orgAn as oa

def mainW(thePath,initFolder,arRecLoc,arEdgeLoc,ccRecLoc,ccEdgeLoc,gangOrFac,delim):
	analy.initDirs(thePath,initFolder,arRecLoc,arEdgeLoc,ccRecLoc,ccEdgeLoc)
	analy.runConversion(thePath,initFolder,gangOrFac,delim)

	fixpt.cpdFp(thePath,initFolder)
	res.cleanupData(thePath, initFolder,delim)
	oa.analyze(thePath,initFolder,delim)
