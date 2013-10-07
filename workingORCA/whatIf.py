import os, time
from datetime import *
import shutil
import orgAn
import resForCpdv2 as res
import cpdMainWrapper as cmw

#copies an entire directory (initFolder) to (copiedFolder)
def dupe(thePath, initFolder, copiedFolder):
	print "Copying project..."
	shutil.copytree(os.path.join(thePath,initFolder),os.path.join(thePath,copiedFolder))

def hasDelNode(nodeList, line):
		res = False
		for node in nodeList:
			if line.find(node)>-1:
				res=True
		return res

#perminently deletes nodes from the processed project data.
def delNodes(thePath, initFolder, nodesToDel):
	fileLines = []
	with open(os.path.join(os.path.join(thePath,initFolder),"NEW-by-IR-OLD-EDGELIST.dsv.csv"),'r') as fh:
		for line in fh.readlines():
			if not hasDelNode(nodesToDel, line):
				fileLines.append(line)
	with open(os.path.join(os.path.join(thePath,initFolder),"NEW-by-IR-OLD-EDGELIST.dsv.csv"),'w') as fh:
		for line in fileLines:
			fh.write(line)
	print "done."


def whatIf(thePath, initFolder,copiedFolder,nodesToDel,delim):
	dupe(thePath, initFolder, copiedFolder)
	delNodes(thePath,copiedFolder, nodesToDel)
	os.chdir(os.path.join(thePath,copiedFolder))
	for fileName in os.listdir(os.path.join(thePath,copiedFolder)):
	
		if fileName.find(initFolder)>-1:
			newFn = fileName.replace(initFolder,copiedFolder)
			
			os.rename(fileName,newFn)
	res.cleanupData(thePath, copiedFolder,delim)
	orgAn.analyze(thePath,copiedFolder,delim)
