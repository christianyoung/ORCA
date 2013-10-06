import csv
import vna2mpb
from fpdf import FPDF
import os

def stats(pdf,fac,p):
	filename = p+'STATS-FAC-'+fac+'-overallRollup'
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
		
def fullNetwork(pdf,fac,p):
	filename = p+'FAC-'+fac+'-overallRollup'
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	f = p+'FAC-'+fac+'-fullNet'
	vna2mpb.draw(f)
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' FULL NETWORK',0,1,'C')
	image1 = f+'.png'
	pdf.image(image1,75,30,150,100,type='',link="file:///"+f+'.png')
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
		pdf.cell(31,4,str[2],1,0)	
		pdf.cell(30,4,str[3][0:14],1,0)
		pdf.cell(30,4,str[4][0:14],1,0)	
		pdf.cell(30,4,str[5][0:14],1,0)
		pdf.cell(30,4,str[6][0:14],1,0)	
		pdf.cell(15,4,str[7],1,0)
		pdf.cell(10,4,str[8][0:1],1,0)	
		pdf.cell(29,4,str[9],1,1)
		
def coreAndAss(pdf,fac,p):
	filename = p+'CORE-MEM-ROLLUP'
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	f = p+'CORE-MEM-'
	vna2mpb.draw(f)
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' CORE MEMBERS AND ASSOCIATES',0,1,'C')
	image1 = f+'.png'
	pdf.image(image1,75,30,150,100,type='',link="file:///"+f+'.png')
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
		pdf.cell(31,4,str[2],1,0)	
		pdf.cell(30,4,str[3][0:14],1,0)
		pdf.cell(30,4,str[4][0:14],1,0)	
		pdf.cell(30,4,str[5][0:14],1,0)
		pdf.cell(30,4,str[6][0:14],1,0)	
		pdf.cell(15,4,str[7],1,0)
		pdf.cell(10,4,str[8][0:1],1,0)	
		pdf.cell(29,4,str[9],1,1)

def ecosystem(pdf,fac,p):
	filename = p+'BULLETS.FAC-'+fac
	f = p+'SUBGROUP-RELATIONS'
	vna2mpb.draw(f)
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter=',')
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,''+fac+' ECOSYSTEM',0,1,'C')
	image1 = f+'.png'
	pdf.image(image1,75,30,150,100,type='',link="file:///"+f+'.png')
	pdf.set_font('Helvetica','',8)
	pdf.ln(115)
	for row in reader:
		if row:
			if row[0] != '':
				pdf.cell(0,3,''+row[0],0,1)
			else:
				pdf.cell(0,3,'          '+row[2],0,1)
		pdf.ln()
		
def connectingMem(pdf,fac,p):
	filename = p+'CONNECTORS.FAC-'+fac
	reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
	
	pdf.set_font('Helvetica','BU',8)
	pdf.cell(0,3,fac+' CORE MEMBERS AND ASSOCIATES',0,1,'C')
	pdf.set_font('Helvetica','',8)
	pdf.ln(5)
	FLAG = 0
	for row in reader:
		if FLAG == 0:
			FLAG = 1
		else:
			j = 2		
			str = 'IR: ' + row[0] + '; Num. Groups: ' + row[1]
			pdf.cell(10,4,str,0,1)
			str = '     Member Sub-Groups: '
			while len(row) > j:
				if row[j] == '':
					str = str + row[j]
					break
				else:
					str = str + row[j] + ', '
				j = j+1
			pdf.multi_cell(0,4,str,0)
			str = '     Conn. Sub-Groups: '
			while len(row) > j:
				if row[j] != '':
					str = str + row[j] + ', '
				j = j+1				
			pdf.multi_cell(0,4,str,0)

def subGroups(pdf,fac,p):
	i = 1
	filename = p+'ORG-com-'+repr(i)+'-ROLLUP'
	while os.path.isfile(filename+'.csv'):
		pdf.add_page()
		reader = csv.reader(open(filename+'.csv', 'rb'),delimiter = ',')
		f = p+'ORG-com-'+repr(i)
		vna2mpb.draw(f)
	
		pdf.set_font('Helvetica','BU',8)
		pdf.cell(0,3,fac+' SUB-GROUP '+repr(i),0,1,'C')
		image3 = f+'.png'
		pdf.image(image3,75,30,150,100,type='',link="file:///"+f+'.png')
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
			pdf.cell(31,4,str[2],1,0)	
			pdf.cell(30,4,str[3][0:14],1,0)
			pdf.cell(30,4,str[4][0:14],1,0)	
			pdf.cell(30,4,str[5][0:14],1,0)
			pdf.cell(30,4,str[6][0:14],1,0)	
			pdf.cell(15,4,str[7],1,0)
			pdf.cell(10,4,str[8][0:1],1,0)	
			pdf.cell(29,4,str[9],1,1)
		i = i+1
		filename = p+'ORG-com-'+repr(i)+'-ROLLUP'	