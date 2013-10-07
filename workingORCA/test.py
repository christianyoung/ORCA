import facPDF
import os

path = "C:\\Users\\x41830\\desktop\\ORCAGUI\\ORG-RES\\FAC-BUSH\\"
facPDF.generate('BUSH','Author of File', path)
fullpath = path + "BUSH.PDF"
os.system('start '+ fullpath)