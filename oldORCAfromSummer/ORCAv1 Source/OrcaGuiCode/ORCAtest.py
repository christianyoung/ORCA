import cpdMainWrapper as cmw
import os
import whatIf

#Main Path
thePath = r"c:\batch\experVersionCpd"

#Init files (assumed to be in the above path)

#Init arrest files
arRecLoc = r"C:\batch\experVersionCpd\initFiles\arRec"
arEdgeLoc = r"C:\batch\experVersionCpd\initFiles\arEdge"
ccRecLoc = r"C:\batch\experVersionCpd\initFiles\ccRec"
ccEdgeLoc = r"C:\batch\experVersionCpd\initFiles\ccEdge"

#0 for gang, 1 for fac
gangOrFac = 1

#Project name
#initFolder="allFac4"
initFolder="allGang3"

#Delimiter used in input files
delim = "\t"

#Main wrapper that gets run
cmw.mainW(thePath,initFolder,arRecLoc,arEdgeLoc,ccRecLoc,ccEdgeLoc,gangOrFac,delim)

#What-if package takes a list of nodes to kill and re-does the analysis
#whatIf.whatIf(thePath,initFolder,initFolder+"-copy",['2015918'],delim)

print "done with all."



