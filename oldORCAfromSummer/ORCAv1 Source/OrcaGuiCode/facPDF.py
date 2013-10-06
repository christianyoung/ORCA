from fpdf import FPDF
import datetime
import pdfGen
import os

today = datetime.date.today()
todayString = today.strftime('%d %B %Y')

def generate(name, author, path, gang): #name - name of fac or gang, gang: 1 = gang, 0 = faction
        if not os.path.isfile(path+name+'.pdf'):
                pdf=PDF('P')
                pdf.name = name
                pdf.author = author
                pdf.alias_nb_pages()
                pdf.add_page()
                pdfGen.coversheet(pdf)
                pdf.add_page()
                pdfGen.stats(pdf,name,path,gang)
                pdf.add_page('P')
                pdfGen.fullNetwork(pdf,name,path,gang)
                pdf.add_page('P')
                pdfGen.coreAndAss(pdf,name,path,gang)
                #pdf.add_page('P')
                #pdfGen.seedSet(pdf,name,path,gang)
                pdf.add_page('P')
        	pdfGen.ecosystem(pdf,name,path,gang)
                pdf.add_page('P')
                pdfGen.connectingMem(pdf,name,path,gang)
                pdfGen.subGroups(pdf,name,path,gang)
                
                pdf.output(path+name+'.pdf','F')
def tacpdf(name,author,path,gang):
        if not os.path.isfile(path+name+'tac.pdf'):
                pdf=PDF('P')
                pdf.name=name
                pdf.author=author
                pdf.alias_nb_pages()
                pdf.add_page('P')
                pdfGen.coversheet2(pdf)
                
                pdfGen.stats(pdf,name,path,gang)
                pdf.add_page('P')
                pdfGen.ecosystem(pdf,name,path,gang)
                pdf.add_page('P')
                pdfGen.coreAndAss(pdf,name,path,gang)
                pdf.add_page('P')
                #pdfGen.seedSet(pdf,name,path,gang)
                #pdf.add_page('P')
                pdfGen.subGroups2(pdf,name,path,gang)
		pdf.output(path+name+'tac.pdf','F')
class PDF(FPDF):
		def header(this):
				this.set_font('Helvetica','BU',10)
				this.cell(0,3,'ANALYSIS OF '+this.name+' - '+todayString,0,1,'C')
				this.ln()
				this.cell(0,3,'Author: ' + this.author,0,1,'C')
				this.set_font('Helvetica','',10)
				this.ln()
				this.ln()

		def footer(this):
				this.set_y(-15)
				this.set_font('Helvetica','',10)
				this.cell(0,10,str(FPDF.page_no(this)),0,0,'C')	
