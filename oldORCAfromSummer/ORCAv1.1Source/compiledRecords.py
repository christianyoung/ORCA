import os 

writeFile = open("compiledRecords", 'w')
#print os.getcwd()
dirList = []
fileList = []
arEdges = []
arRecords = []
ccEdges = []
ccRecords  = []
# C:\Users\x49962\Desktop\orcaModifications\dist\recordsFolder
def seperateFolders(theDir):
        for root, dirs, files in os.walk(theDir):
                if os.path.basename(root) == 'recordsFolder':
                        for i in dirs:
                                print os.path.join(os.getcwd(), 'recordsFolder', i)
                                if i == 'arRelationships':
                                        for x in os.listdir(os.path.join(root,i)):
                                                fileList.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                                arEdges.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                elif i == 'arRecords':
                                        for x in os.listdir(os.path.join(root,i)):
                                                fileList.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                                arRecords.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                elif i == 'ccRelationships':
                                        for x in os.listdir(os.path.join(root,i)):
                                                fileList.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                                ccEdges.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x))
                                elif i == 'ccRecords':
                                        for x in os.listdir(os.path.join(root,i)):
                                                fileList.append(os.path.join(os.getcwd(), 'recordsFolder', i, x))
                                                ccRecords.append(os.path.join(os.getcwd(), 'recordsFolder', i,  x)) 
		
