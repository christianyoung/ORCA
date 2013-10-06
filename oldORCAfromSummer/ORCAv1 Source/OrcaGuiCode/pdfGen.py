# -*- coding: cp1252 -*-
import csv
import vna2mpb3
from fpdf import FPDF
import os
import sys

def stats(pdf,fac,p,g):
        
                
	if g == 0:
		filename = p+'STATS-FAC-'+fac+'-overallRollup'
	else:
		filename = p+'STATS-GANG'+fac+'-overallRollup'
		
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,'STATS',0,1,'C')
	pdf.set_font('Helvetica','',8)
	pdf.ln(5)
	for row in reader:
		j = 0		
		str = ['','']
		while len(row) > j:
			str[j] = row[j]
			str[j].rstrip()
			j = j+1
		pdf.cell(120,4,str[0],1,0)
		pdf.cell(30,4,str[1],1,1)
   
def coversheet(pdf):
        #pdf.cell(width,height,text,border,line, align)
        homepath= os.path.abspath(os.path.dirname(sys.argv[0]))
        def paragraph(Title,body):

              pdf.set_font('Helvetica','BU',12)
              pdf.write(5,Title+":")
              pdf.set_font('Helvetica','',10)
              pdf.write(5," "+body)
              pdf.ln()
              pdf.ln()
        pdf.set_font('Helvetica','B',16)
        pdlogopath ="images/nCPD1.jpg"        
        pdf.image(os.path.join(homepath,pdlogopath), 0,0, 30,30,type='')
        pdf.cell(0,4,"Chicago Police Department ORCA Gang Analysis Report","B",1,'C')
        pdf.ln()
        pdf.set_font('Helvetica','',12)
        paragraph("General", "In this network, nodes (dots) represent individuals, identified by Individual Record (IR) "+
        "number. If IR is unavailable, another ID number (or CC number) is used. Edges (lines connecting nodes) "+ 
        "represent relationships between two individuals.")
        paragraph("Nodes","Graphic representation of an individual. The size of the node is determined by that individual's "+
                  "number of personal connections, so that individuals with more connections appear as larger nodes. Node color "+
                  "indicates membership in a sub-group within the network, i.e. these individuals associate more regularly with each "+
                  "other than with other members of the network.  Identical colors belong to the same sub-group. In all network visuals, "+
                  "except the \"Sub-Group Relations\" visual, nodes that are white denote individuals for which no particular sub-group "+
                  "affilation has been determined.")
        paragraph("Finding Unidentified Members","In the dataset, not all individuals in the social network admitted to being in a gang "+
                  "or faction.  Calculated probabilities(or degree of membership) for individuals who are not aligned with a given gang "+
                  "are provided.  Self- or positively-identified members have the number \"1.0\" displayed in parenthesis after their "+
                  "identification number.  Individuals who are not self- or pos-identified as members have their calculated membership "+
                  "displayed in parenthesis after their identification number.  This number can be converted to a percentage probability. "+
                  "For example, (.37) would equal 37% probability of membership." )
        paragraph("Overall Network Layout","Visualization and chart of the social network as a whole(all network members).")
        paragraph("Core Member Layout","Visualization and chart of the core members of the overall network and those persons to whom "+
                  "they have immediate connection.")
        paragraph("Core and Covering Members","Core members are individuals who, by number and type of connections, are crucial to holding the "+
                  "network together; they are the \"backbone\" of the network.  Covering members are core members who are connected to all other "+
                  "core members.  These individuals are not only crucial to holding the network together, but their connection to all other "+
                  "core members makes them valuable sources of information.")
        paragraph("Community Structure","The network is divided into sub-groups. The premise is that within the sub-groups, there are "+
                  "many connections and between sub-groups there are fewer connections. All sub-groups identified have at least ten members. "+
                  "Remaining members are collected in a group labeled \"Sub-Others\". How well defined these sub-groups are is also calculated "+
                  "(whether the overall network has strong, defined sub-groups or not)")
        paragraph("Ecosystem","Describes relationships between all subgroups within the overall data sets. This allows for identifying which "+
                  "sub-groups are directly interacting with other sub-groups--including sub-groups in other gang networks.  Visualization of "+
                  "these is provided.  The quality (or strength) of these links is provided. Additionally, a chart is provided that shows "+
                  "which network members have the most connections to other sub-groups. These individuals are \"human bridges\" between their "+
                  "own sub-group and other sub-groups.")
        paragraph("Individual Sub-Groups","Network for all subgroups with at least ten members, list of members, and identification of core "+
                  "and covering core members for each sub-group is provided.")



def coversheet2(pdf):
        homepath= os.path.abspath(os.path.dirname(sys.argv[0]))
        def paragraph(Title,body):

              pdf.set_font('Helvetica','BU',12)
              pdf.write(5,Title+":")
              pdf.set_font('Helvetica','',10)
              pdf.write(5," "+body)
              pdf.ln()
              pdf.ln()
        pdf.set_font('Helvetica','B',16)
        pdlogopath ="images/nCPD1.jpg"
        
        pdf.image(os.path.join(homepath,pdlogopath), 0,0, 30,30,type='')
        pdf.cell(0,4,"Chicago Police Department ORCA Gang Analysis Report","B",1,'C')
        pdf.ln()
        pdf.set_font('Helvetica','',12)
        paragraph("General","Nodes (dots) represent individuals, identified by IR number (or CC number). "+
                  "Individuals with more connections appear as larger nodes.  Node color indicates membership "+
                  "in a sub-group within the network.  Identical colors belong to the same sub-group. In all "+
                  "network visuals, except the \"Sub-Group Relations\" visual, nodes that are white denote "+
                  "individuals for which no particular sub-group affiliation has been determined. Edges (lines "+
                  "connecting nodes) represent relationships between two individuals.")
        paragraph("Finding Unidentified Members","Calculated probabilities of membership for individuals "+
                  "who did not admit to being in a gang or faction but were arrested or contacted with an "+
                  "admitted gang member. Self- or positively-identified members are numbers \"1.0\".")
        paragraph("Ecosystem","This chart for identifies which sub-groups are directly interacting with other "+
                  "sub-groups – including sub-groups in other gang networks. Visualization of these is provided. "+
                  "The quality (or strength) of these links is provided.  Additionally, a chart is provided that "+
                  "shows which network members have the most connections to other sub-groups.  These individuals are "+
                  "\"human bridges\" between their own sub-group and other sub-groups.")
        paragraph("Core Member Layout","Visualization and chart of the core members of the overall network and those "+
                  "persons to whom they have immediate connection.")
        paragraph("Core and Covering Members","Core members are individuals who, by number and type of connections, are "+
                  "crucial to holding the network together; they are the \"backbone\" of the network. Covering members "+
                  "are core members who are connected to all other core members. These individuals are not only crucial "+
                  "to holding the network together, but their connection to all other core members makes them valuable sources of information.")
        paragraph("Sub-Group Core Members","Chart listing core members of each sub-group only. Full listing of sub-group membership can be "+
                  "found in ORCA or the full pdf report.")

                  

        


def fullNetwork(pdf,fac,p,g):
	if g == 0:
		filename = p+'FAC-'+fac+'-overallRollup'
		f = p+'FAC-'+fac+'-fullNet'
		tempString = "FAC-"
	else:
		filename = p+'GANG'+fac+'-overallRollup'
		f = p+'GANG'+fac+'-fullNet'
		tempString = "GANG"
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	name2=tempString +fac
        vna2mpb3.fullnet(p,name2,1)
        image1=p+tempString+fac+"-fullnet.PNG"	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' FULL NETWORK',0,1,'C')
	
	pdf.image(image1,30,30,150,100,type='')
	pdf.set_font('Helvetica','',8)
	pdf.ln(115)
	for row in reader:
		j = 0		
		str = ['','','','','','','','','','']
		while len(row) > j:
			str[j] = row[j]
			str[j].rstrip()
			j = j+1
		pdf.cell(9,4,str[0],1,0)	
		pdf.cell(31,4,str[1],1,0)	
		pdf.cell(15,4,str[2],1,0)	
		pdf.cell(30,4,str[3][0:14],1,0)
		pdf.cell(30,4,str[4][0:14],1,0)	
		pdf.cell(15,4,str[5][0:14],1,0)
		pdf.cell(15,4,str[6][0:14],1,0)	
		pdf.cell(15,4,str[7],1,0)
		pdf.cell(6,4,str[8][0:1],1,0)	
		pdf.cell(24,4,str[9],1,1)
		
def coreAndAss(pdf,fac,p,g):
	filename = p+'CORE-MEM-ROLLUP'
        if g==0:
                tempString = "FAC-"
        if g==1:
                tempString= "GANG"
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	f = p+'CORE-MEM-'
        name2= tempString+fac
	vna2mpb3.coremem(p,name2,1)
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' CORE MEMBERS AND ASSOCIATES',0,1,'C')
	image1 = p+tempString+fac+'-coremem.png'
	pdf.image(image1,30,30,150,100,type='')
	pdf.set_font('Helvetica','',8)
	pdf.ln(115)
	for row in reader:
		j = 0		
		str = ['','','','','','','','','','']
		while len(row) > j:
			str[j] = row[j]
			str[j].rstrip()
			j = j+1
		pdf.cell(9,4,str[0],1,0)	
		pdf.cell(31,4,str[1],1,0)	
		pdf.cell(15,4,str[2],1,0)	
		pdf.cell(30,4,str[3][0:14],1,0)
		pdf.cell(30,4,str[4][0:14],1,0)	
		pdf.cell(15,4,str[5][0:14],1,0)
		pdf.cell(15,4,str[6][0:14],1,0)	
		pdf.cell(15,4,str[7],1,0)
		pdf.cell(6,4,str[8][0:1],1,0)	
		pdf.cell(24,4,str[9],1,1)

def ecosystem(pdf,fac,p,g):
	if g == 0:
		filename = p+'BULLETS.FAC-'+fac
		tempString="FAC-"
	else:
		filename = p+'BULLETS.GANG'+fac
		tempString="GANG"
	f = p+'SUBGROUP-RELATIONS'
	vna2mpb3.subgrouprelations(p,tempString+fac,1)
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter=',')
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,''+fac+' ECOSYSTEM',0,1,'C')
	image1 = p+tempString+fac+'-subgrouprelations.png'
	pdf.image(image1,30,30,150,100,type='')
	pdf.set_font('Helvetica','',8)
	pdf.ln(115)
	
	for row in reader:
                #new row
		if row:

			if row[0] != '':
                                #if the row isn't null, it has a name
                                
				pdf.cell(0,3,''+row[0],0,0)
				pdf.ln()
			else:
                                
				#the row is null, it is a listing
                                maxlen = len(row)
                                i = 2
                                str1=''
                                while (i<maxlen):
                                        
                                       if pdf.get_string_width(str1) > 150:
                                              pdf.cell(150,3,'          '+str1,0,0)
                                              pdf.ln()
                                              str1 = ''
                                       else: 
                                              str1 = str1 +str(row[i]).rstrip()+', '
                                              i=i+1
                                str2 = '          '+str1
                                str3 = str2[:len(str2)-4]
                                pdf.cell(150,3,str3,0,0)
                                pdf.ln()
		pdf.ln()
		
        
		
def connectingMem(pdf,fac,p,g):
	if g == 0:
		filename = p+'CONNECTORS.FAC-'+fac
	else:
		filename = p+'CONNECTORS.GANG'+fac
		
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' CORE MEMBERS AND ASSOCIATES',0,1,'C')
	pdf.ln(5)
	FLAG = 0
	for row in reader:
		if FLAG == 0:
			FLAG = 1
		else:
			j = 2
			
			if row[1] < 3:
                                
                                pass
                        else:
                                pdf.set_font('Helvetica','B',8)			
                                str = 'IR: ' + row[0] + '; Num. Groups: ' + row[1]
                                pdf.cell(0,4,str,0,1)
                                pdf.set_font('Helvetica','',8)
                                str = 'Member Sub-Groups: '
                                while len(row) > j:
                                        if row[j] == '':
                                                str = str + row[j]
                                                break
                                        else:
                                                str = str + row[j] + ', '
                                        j = j+1
                                pdf.multi_cell(0,4,str,0,'L')
                                str = 'Conn. Sub-Groups: '
                                while len(row) > j:
                                        if row[j] != '':
                                                str = str + row[j] + ', '
                                        j = j+1				
                                pdf.multi_cell(0,4,str,0,'L')
                                pdf.ln(3)

def subGroups(pdf,fac,p,g):
	i = 1
	filename = p+'ORG-com-'+repr(i)+'-ROLLUP'
	while os.path.isfile(filename+'.csv'):
		pdf.add_page()
		reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
		f = p+'\\'+'ORG-com-'+repr(i)
		pdf.set_font('Helvetica','BU',8)
		pdf.cell(0,3,fac+' SUB-GROUP '+repr(i),0,1,'C')
		vna2mpb3.subgroupmap(f,1)
		image1 = f+'-subgroupmap.png'
                pdf.image(image1,30,30,150,100,type='')
		pdf.set_font('Helvetica','',8)
		pdf.ln(115)
		
		for row in reader:
			j = 0		
			str = ['','','','','','','','','','']
			while len(row) > j:
				str[j] = row[j]
				str[j].rstrip()
				j = j+1
			pdf.cell(9,4,str[0],1,0)	
			pdf.cell(31,4,str[1],1,0)	
			pdf.cell(15,4,str[2],1,0)	
			pdf.cell(30,4,str[3][0:14],1,0)
			pdf.cell(30,4,str[4][0:14],1,0)	
			pdf.cell(15,4,str[5][0:14],1,0)
			pdf.cell(15,4,str[6][0:14],1,0)	
			pdf.cell(15,4,str[7],1,0)
			pdf.cell(6,4,str[8][0:1],1,0)	
			pdf.cell(24,4,str[9],1,1)
			
		i = i+1
		filename = p+'ORG-com-'+repr(i)+'-ROLLUP'
def subGroups2(pdf,fac,p,g):
	i = 1
	filename = p+'ORG-com-'+repr(i)+'-ROLLUP'
	while os.path.isfile(filename+'.csv'):
		
		reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
		f = p+'\\'+'ORG-com-'+repr(i)
		pdf.set_font('Helvetica','BU',8)
		pdf.cell(0,3,fac+' SUB-GROUP '+repr(i)+' CORE MEMBERS',0,1,'C')
		pdf.ln(10)
		pdf.set_font('Helvetica','',8)
		
		
		for row in reader:
                        if row[1] != '':
                                j = 0		
                                str = ['','','','','','','','','','']
                                while len(row) > j:
                                        str[j] = row[j]
                                        str[j].rstrip()
                                        j = j+1
                                pdf.cell(9,4,str[0],1,0)	
                                pdf.cell(31,4,str[1],1,0)	
                                pdf.cell(15,4,str[2],1,0)	
                                pdf.cell(30,4,str[3][0:14],1,0)
                                pdf.cell(30,4,str[4][0:14],1,0)	
                                pdf.cell(15,4,str[5][0:14],1,0)
                                pdf.cell(15,4,str[6][0:14],1,0)	
                                pdf.cell(15,4,str[7],1,0)
                                pdf.cell(6,4,str[8][0:1],1,0)	
                                pdf.cell(24,4,str[9],1,1)
			else:
                                pass
			
		i = i+1
		filename = p+'ORG-com-'+repr(i)+'-ROLLUP'
                pdf.ln(30)

		
def seedSet(pdf,fac,p,g):
        if g == 1:
                tempString= "GANG"
        if g==0:
                tempString= "FAC-"
        filename= p+"\\"+tempString+fac+"-fullNet-SEED.csv"
        reader = csv.reader(open(filename,'rb'),delimiter = ',')
        pdf.set_font('Helvetica','BU',8)
        for row in reader:
                i=0
                while (i<len(row)):
                        pdf.cell(10,4,row[i],0,0)
                        i=i+1
                        pdf.ln()

