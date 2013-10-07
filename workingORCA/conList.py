import shortestPath as sp

startList = [1584925]
endList = [1836914,1982150,1823466,1498611,1573715,1630440]

for start in startList:
    for end in endList:
        sp.path(start,end)
