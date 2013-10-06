#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

##Changes from v1-> v1.1
##    1. The input method has been changed from adding all records individually to entering
##        the record folder and that's it.
##    2. The format for the Tac PDF was modified to fit Officer Berteto's preferences.
##    3. Added an exception handler for adding in new districts. Now able to ingest district
##        3 and 4 data.
##    4. Removed the influence set from the full version PDF. 
        
import Tkinter
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import textwrap
import os
import facPDF
import whatIf
import autocomplete as ac
import vna2mpb3
import cpdMainWrapper as cmw
global displayVar    #for recordFolder Directory
global displayVar5   #for Old analysis ORG-RES locations
global displayVar6   # directory for new analysis
global displayVar7   # project name
global author

     #for the gang/fac selection menu
Options= []  #contains the name and full path FACTIONS (ie "FAC-79THAND..., C:/users/.../ORG-RES/FAC-79THAND...")
Options2=[]  #contains the name and full path for GANGS


def submitnew(gangOrFac):
    recordDirectory = displayVar.get()
    for root, dirs, files in os.walk(recordDirectory):
        if os.path.basename(root) == 'recordsFolder':
            for i in dirs:
                    if i == 'arRelationships':
                        arEdge = os.path.join(recordDirectory, i)
                    elif i == 'arRecords':
                        arRec = os.path.join(recordDirectory, i)
                    elif i == 'ccRelationships':
                        ccEdge =os.path.join(recordDirectory, i)
                    elif i == 'ccRecords':
                        ccRec =os.path.join(recordDirectory, i) 
    thePath = displayVar6.get()
    initFolder = displayVar7.get()
    delim = "\t"
    if os.path.isdir(thePath+"\\"+initFolder):
        tkMessageBox.showerror("Folder already exists", "You have given a project name that \
    already exists as a file directory. Choose a new project name or new project directory")
    else:
        cmw.mainW(thePath, initFolder, arRec,arEdge,ccRec,ccEdge,gangOrFac,delim)
        displayVar5.set(thePath+"\\"+ initFolder)
        submitold()
    
    

def submitold():
    GangFac = 0
    GangFac2= 0
    path = displayVar5.get()
    
    path = path + "\\ORG-RES"
    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for dirname in dirnames:
                if dirname[0:3] == 'FAC':
                    GangFac = 1
                    
                if dirname[0:4] == 'GANG':
                    GangFac2= 1
        if (GangFac and GangFac2):
            tkMessageBox.showerror("Error","This directory has more than one analysis and will not be opened.")
        else:
            create_widgets_in_select_gangfac_frame(path,GangFac)
            call_select_gangfac_on_top()
    else:
        tkMessageBox.showerror("Analysis Not Found", "No ORCA analysis found in that folder.\
 Please double check the name and path of the analysis you are looking for.")
    
def load_file():
     fname = askdirectory(mustexist=True, title = "find the Record Folder Directory.")
     if fname:
        try:
              displayVar.set(fname)
        except:                     
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

##def load_file2():
##     fname2 = askdirectory(mustexist=True, title = "find the arrest records Directory")
##     if fname2:
##        try:
##           displayVar2.set(fname2)
##        except:                     
##              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
##        return
##
##def load_file3():
##     fname3 = askdirectory(mustexist=True, title = "find the contact card relationship Directory")
##     if fname3:
##        try:
##           displayVar3.set(fname3)
##        except:                     
##              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
##        return
##
##def load_file4():
##     fname4 = askdirectory(mustexist=True, title = "find the contact card records Directory")
##     if fname4:
##        try:
##           displayVar4.set(fname4)
##        except:                     
##              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
##        return

def load_file5():
     fname5 = askdirectory(mustexist=True, title = "find the Project Directory")
     if fname5:
        try:
           displayVar5.set(fname5)
        except:                    
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return
    
def load_file6():
     fname6 = askdirectory(mustexist=True, title = "find the directory you would like this project to be saved in")
     if fname6:
        try:
           displayVar6.set(fname6)
        except:                     
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return



def create_widgets_in_first_frame():
    
    #photo=PhotoImage(file='CPDLogo.gif')
    
    disclaimer ="""Chicago Police Dept. ORCA Software
 
This version of ORCA has been created especially for the Chicago Police Department (CPD) by students and faculty of the Dept. of Electrical Engineering and Computer Science at the U.S. Military Academy, West Point, NY. \nCPD is granted unlimited, unrestricted use of this software.
 
This software was created by the U.S. Department of Defense (US DoD). All intellectual property rights are retained by the US DoD. Please contact MAJ Paulo Shakarian if you wish to re-distribute this software outside the CPD in any way.
 
\nThis software is experimental in nature. The validity of the results is not guaranteed. Further, there is no expressed or implied warranty or long-term support plan for this software. Potential sources of problems for this or any experimental software can include (but are not limited to) incorrect assumptions of the underlying model, incorrect parameters, the use of heuristic algorithms, improper data input, coding bugs, user error, and/or incorrect interpretation of results.

Click “accept” to continue using this software or “decline” to exit."""

    disclaimer2 = textwrap.dedent(disclaimer).strip()

 
    
    #img=Tkinter.Label(first_frame, image = photo)
    #img.pack()
    first_window_label = Tkinter.Label(first_frame, justify =LEFT, wraplength = 1200,text= textwrap.fill(disclaimer2,width=100,initial_indent = '    ') )
    first_window_label.pack()
    first_window_button_frame = Frame(first_frame)
    
    first_window_quit_button = Tkinter.Button(first_window_button_frame, text = "Decline", command = quit_program)
    first_window_quit_button.pack(side=LEFT)
    first_window_next_button = Tkinter.Button(first_window_button_frame, text = "Accept", command = call_second_frame_on_top)
    first_window_next_button.pack(side=LEFT)
    first_window_button_frame.pack()
    

def create_widgets_in_second_frame():

    
    second_window_label = Tkinter.Label(second_frame, wraplength = 200, text='Would you like to create a new analysis or open an existing one?')
    second_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))

    
    second_window_back_button = Tkinter.Button(second_frame, text = "Open Existing", command = call_open_existing_on_top)
    second_window_back_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    second_window_next_button = Tkinter.Button(second_frame, text = "Create New", command = call_create_new_on_top)
    second_window_next_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))
def generatePDF(analyzeThis,author,gangFac,popup):
    popup.destroy()
    call_select_gangfac_on_top()
    facPDF.generate(analyzeThis[0][4:], author.get(), analyzeThis[1]+"\\",gangFac)
    fullpath = analyzeThis[1] +"\\"+analyzeThis[0][4:]+".PDF"
    os.startfile(fullpath)

def generatetacPDF(analyzeThis,author,gangFac,popup):
    popup.destroy()
    call_select_gangfac_on_top()
    facPDF.tacpdf(analyzeThis[0][4:], author.get(), analyzeThis[1]+"\\",gangFac)
    fullpath = analyzeThis[1] +"\\"+analyzeThis[0][4:]+"tac.PDF"
    os.startfile(fullpath)

    
def viewPDF(analyzeThis):
    
    gangFac= 0
    
    
    fullpath = analyzeThis[1] +"\\"+analyzeThis[0][4:]+".PDF"
    if analyzeThis[0][0:3] == 'FAC':
        pass
    else:
        gangFac=1
        
    if os.path.isfile(fullpath):
        os.startfile(fullpath)
    else:   
        create_widgets_in_author_input_frame(analyzeThis,gangFac)
     
def tacPDF(analyzeThis):
    
    gangFac= 0
    
    
    fullpath = analyzeThis[1] +"\\GANG"+analyzeThis[0]+"tac.PDF"
    if analyzeThis[0][0:3] == 'FAC':
        fullpath = analyzeThis[1] +"\\FAC-"+analyzeThis[0]+"tac.PDF"
    else:
        gangFac=1
        fullpath = analyzeThis[1] +"\\GANG"+analyzeThis[0]+"tac.PDF"  
    if os.path.isfile(fullpath):
        os.startfile(fullpath)
    else:   
        create_widgets_in_author_input_frame2(analyzeThis,gangFac)
    

    
def Show_View_Net_Map(analyzeThis):
    vna2mpb3.fullnet(analyzeThis[1]+"\\",analyzeThis[0],0)
    
def Show_Core_Mem(analyzeThis):
    vna2mpb3.coremem(analyzeThis[1]+"\\",analyzeThis[0],0)	
def Show_Sub_Group_Relations(analyzeThis):
    vna2mpb3.subgrouprelations(analyzeThis[1]+"\\",analyzeThis[0],0)
    
    
def Show_Details_SubGroup(analyzeThis):
    
    fullpath = analyzeThis[1] + "\\" + "BULLETS." + analyzeThis[0] + ".csv"
    os.startfile(fullpath)
def Show_Connectors(analyzeThis):

    fullpath = analyzeThis[1] + "\\" + "CONNECTORS." +analyzeThis[0]+".csv"
    os.startfile(fullpath)
    
def Show_stats(analyzeThis):
    fullpath = analyzeThis[1] +"\\STATS-" + analyzeThis[0] + "-overallRollup.csv"
    os.startfile(fullpath)

def create_widgets_in_author_input_frame(analyzeThis,gangFac):
    
    textFrame = Frame(author_input_frame)
    entryLabel= Label(textFrame)
    entryWidget= Entry(textFrame, textvariable = author)
    entryLabel["text"] = "NO PDF FOUND. Generate a new one. Author's Name:"
    entryLabel.pack(side=LEFT)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)
    Enter = Button(textFrame, text = "Generate", command = lambda: generatePDF(analyzeThis,author,gangFac, textFrame))
    Cancel= Button(textFrame, text = "Cancel", command = lambda:select_different_gangfac(textFrame))
    Cancel.pack()
    Enter.pack()
    textFrame.pack()
    call_author_input_on_top()

def create_widgets_in_author_input_frame2(analyzeThis,gangFac):
    
    textFrame = Frame(author_input_frame2)
    entryLabel= Label(textFrame)
    entryWidget= Entry(textFrame, textvariable = author)
    entryLabel["text"] = "NO PDF FOUND. Generate a new one. Author's Name:"
    entryLabel.pack(side=LEFT)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)
    Enter = Button(textFrame, text = "Generate", command = lambda: generatetacPDF(analyzeThis,author,gangFac, textFrame))
    Cancel= Button(textFrame, text = "Cancel", command = lambda:select_different_gangfac(textFrame))
    Cancel.pack()
    Enter.pack()
    textFrame.pack()
    call_author_input2_on_top()



    
    
    
def create_widgets_in_open_existing_frame():
    textFrame = Frame(open_existing_frame)
    textFrame2= Frame(open_existing_frame)
    entryLabel= Label(textFrame)
    entryLabel["text"] = "Enter the directory for the old analysis"
    entryLabel.pack(side=LEFT)
    entryWidget = Entry(textFrame, textvariable = displayVar5)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)
    
    browseButton = Button(textFrame, text= "browse...", command=load_file5, width=10)
    browseButton.pack(side=LEFT)
    
    back = Button(textFrame2, text = "Back", command=call_second_frame_on_top, width=10)
    back.pack(side=LEFT)
    Submit = Button(textFrame2, text = "Submit", command= submitold, width=10)
    Submit.pack(side=LEFT)
    textFrame.pack()
    textFrame2.pack()
def select_different_analysis(self):
    self.destroy()
    call_open_existing_on_top()
def select_different_gangfac(self):
    self.destroy()
    call_select_gangfac_on_top()

def create_widgets_in_select_gangfac_frame(path,gangFac):
    def verifyinput(path,PrintableNames,selection):
        if selection in PrintableNames:
            if gangFac ==0:
                selection = "GANG-"+selection
            else:
                selection = "FAC-"+selection

            return (selection,str(path)+"\\"+selection)
        else:
            tkMessageBox.showerror("Error","The gang name entered is not recognized.")
    textFrame = Frame(select_gangfac_frame)
    optionLabel = Label(textFrame)
    optionLabel["text"] = "Select a faction/gang from the dropdown"
    optionLabel.pack(side=LEFT)
    PrintableNames = []
    authorinputbool=False
    if gangFac:
        variableLength=4
    else:
        variableLength=5
    for (dirpath, dirnames, filenames) in os.walk(path):        
        for dirname in dirnames:
            PrintableNames.append(str(dirname[variableLength:]))
    selection = ac.AutocompleteCombobox(textFrame)
    selection.set_completion_list(PrintableNames)
    selection.pack(side=LEFT)
    #optionMenuWidget = Tkinter.OptionMenu(textFrame, selection, PrintableNames[0], *PrintableNames[1:])
    #optionMenuWidget.config(width = 40)
    #selection.set(PrintableNames[0])
    #optionMenuWidget["width"] =40
    #optionMenuWidget.pack(side=LEFT)
    textFrame.pack()
    backButton = Button(textFrame, text = "<--Back", command = lambda: select_different_analysis(textFrame),width =30)
    backButton.pack()


    

    viewFullNetworkButton = Button(textFrame, text = "View Full Network (Map)", command = lambda: Show_View_Net_Map(verifyinput(path,PrintableNames,selection.get())), width = 30)
    coreMemberAssocNetworkButton  = Button(textFrame, text = "View Core Member (Map)", command = lambda: Show_Core_Mem(verifyinput(path,PrintableNames,selection.get())), width = 30)
    subGrpRelsButton  = Button(textFrame, text = "Sub Group Relations (Map)", command = lambda: Show_Sub_Group_Relations(verifyinput(path,PrintableNames,selection.get())), width = 30)
    detailsOnSubGrpButton  = Button(textFrame, text = "Details on Sub-Group (Excel)", command = lambda: Show_Details_SubGroup(verifyinput(path,PrintableNames,selection.get())), width = 30)
    connectorsButton = Button(textFrame, text = "Connecting Members (Excel)", command = lambda: Show_Connectors(verifyinput(path,PrintableNames,selection.get())), width = 30)
    statsButton = Button(textFrame, text = "Membership Breakdown (Excel)", command = lambda: Show_stats(verifyinput(path,PrintableNames,selection.get())), width = 30)
    pdfButton = Button(textFrame, text = "View PDF", command = lambda: viewPDF(verifyinput(path,PrintableNames,selection.get())), width = 20)
    tacpdfButton=Button(textFrame,text = "View Tactical PDF",command=lambda:tacPDF(verifyinput(path,PrintableNames,selection.get())),width = 20)

    viewFullNetworkButton.pack()
    coreMemberAssocNetworkButton.pack()
    subGrpRelsButton.pack()
    detailsOnSubGrpButton.pack()
    connectorsButton.pack()
    statsButton.pack()
    pdfButton.pack()
    tacpdfButton.pack()
def create_widgets_in_create_new_frame():
    topFrame  = Frame(create_new_frame)
    textFrame = Frame(topFrame)
    bottomFrame=Frame(create_new_frame)
    textFrame5= Frame(bottomFrame)
    textFrame6= Frame(bottomFrame)
    textFrame7= Frame(bottomFrame)
    entryLabel= Label(textFrame, anchor = "e")
    entryLabel5= Label(textFrame5)
    entryLabel6= Label(textFrame6)
    entryLabel["text"] = "Records Folder Directory:"
    entryLabel5["text"] = "Directory for output:"
    entryLabel6["text"] = "Project Name:"
    entryLabel["width"]= 35
    

    entryLabel.pack(side = LEFT)
    entryLabel5.pack(side = LEFT)
    entryLabel6.pack(side = LEFT)

    entryWidget = Entry(textFrame, textvariable = displayVar)
    entryWidget5 = Entry(textFrame5, textvariable = displayVar6)
    entryWidget6 = Entry(textFrame6, textvariable = displayVar7)
    entryWidget["width"] = 50
    entryWidget5["width"] = 50
    entryWidget.pack(side = LEFT)
    entryWidget5.pack(side = LEFT)
    entryWidget6.pack(side = LEFT)
    
    browseButton = Button(textFrame, text= "browse...", command=load_file,width=10)
    browseButton.pack(side = LEFT)
    browseButton5 = Button(textFrame5, text= "browse...", command=load_file6, width=10)
    browseButton5.pack(side = LEFT)
    textFrame.pack(anchor= "w")
    v = IntVar()
    gangButton = Radiobutton(textFrame6, text = "Gang", variable = v, value = 0)
    factionButton=Radiobutton(textFrame6, text = "Faction", variable = v, value =1)
    
    gangButton.pack(side = LEFT)
    factionButton.pack(side = LEFT)
    back = Button(textFrame7, text = "Back", command=call_second_frame_on_top, width=10)
    back.pack(side = LEFT)
    Submit = Button(textFrame7, text = "Create New", command=  lambda: submitnew(v.get()), width=10)
    Submit.pack(side = LEFT)
    
    textFrame5.pack()
    textFrame6.pack()
    textFrame7.pack()
    topFrame.pack()
    bottomFrame.pack(pady = 30)

def create_widgets_in_third_frame():
    # Create the label for the frame
    third_window_label = Tkinter.Label(third_frame, text='Window 3')
    third_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))

    # Create the button for the frame
    third_window_back_button = Tkinter.Button(third_frame, text = "Back", command = call_second_frame_on_top)
    third_window_back_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    third_window_quit_button = Tkinter.Button(third_frame, text = "Quit", command = quit_program)
    third_window_quit_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))

def call_open_existing_on_top():
    root_window.title("Open an Existing...")
    select_gangfac_frame.forget()
    second_frame.grid_forget()
    open_existing_frame.pack()

def call_create_new_on_top():
    root_window.title("Create a new analysis...")
    second_frame.grid_forget()
    create_new_frame.pack()
def call_author_input_on_top():
    root_window.title("Generate New PDF")
    select_gangfac_frame.forget()
    author_input_frame.pack()
def call_author_input2_on_top():
    root_window.title("Generate New TAC PDF")
    select_gangfac_frame.forget()
    author_input_frame2.pack()
def call_select_gangfac_on_top():
    root_window.title("Select a gang/faction")
    author_input_frame.forget()
    author_input_frame2.forget()
    open_existing_frame.forget()
    create_new_frame.forget()
    select_gangfac_frame.pack()

    
def call_first_frame_on_top():
    root_window.title("Legal Disclaimer")
   
    second_frame.grid_forget()
    first_frame.pack()
def call_second_frame_on_top():
    root_window.title("Chicago PD Analyzer")
  
    first_frame.forget()
    third_frame.grid_forget()
    create_new_frame.forget()
    open_existing_frame.forget()
    select_gangfac_frame.forget()

    second_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def call_third_frame_on_top():

    second_frame.grid_forget()
    third_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def quit_program():
    root_window.destroy()

if __name__ =="__main__":
    root_window = Tkinter.Tk()
    authorinputbool=False

    window_width = 500
    window_height = 400
    selection  =StringVar()
    displayVar =StringVar()
##    displayVar2=StringVar()
##    displayVar3=StringVar()
##    displayVar4=StringVar()
    displayVar5=StringVar()
    displayVar6=StringVar()
    displayVar7=StringVar()
    author  = StringVar()
    author.set("Chicago PD")

    first_frame= Tkinter.Frame(root_window, width=window_width, height=window_height)
    first_frame['borderwidth'] = 2
    first_frame['relief'] = 'sunken'
    first_frame.pack()

    second_frame= Tkinter.Frame(root_window, width=window_width, height=window_height)
    second_frame['borderwidth'] = 2
    second_frame['relief'] = 'sunken'
    second_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

    open_existing_frame = Tkinter.Frame(root_window, width=window_width, height=window_height)
    open_existing_frame['borderwidth'] = 2
    open_existing_frame['relief'] = 'sunken'
    open_existing_frame.grid(column=0, row=0,padx=20, pady =5, sticky=(Tkinter.W,Tkinter.N, Tkinter.E))

    create_new_frame = Tkinter.Frame(root_window, width=window_width, height=window_height)
    create_new_frame['borderwidth'] = 2
    create_new_frame.pack()

    select_gangfac_frame = Tkinter.Frame(root_window, width=window_width, height = window_height)
    select_gangfac_frame['borderwidth']=2
    select_gangfac_frame.pack()

    third_frame=Tkinter.Frame(root_window, width=window_width, height=window_height)
    third_frame['borderwidth'] = 2
    third_frame['relief'] = 'sunken'
    third_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

    author_input_frame= Tkinter.Frame(root_window, width = window_width, height = window_height)
    author_input_frame['borderwidth'] =2
    author_input_frame.pack()
    author_input_frame2= Tkinter.Frame(root_window, width = window_width, height = window_height)
    author_input_frame2['borderwidth'] =2
    author_input_frame2.pack()

    # Create all widgets to all frames
    create_widgets_in_third_frame()
    create_widgets_in_second_frame()
    create_widgets_in_first_frame()
    create_widgets_in_create_new_frame()
    create_widgets_in_open_existing_frame()





    # Hide all frames in reverse order, but leave first frame visible (unhidden).
    third_frame.grid_forget()
    second_frame.grid_forget()
    open_existing_frame.grid_forget()
    create_new_frame.forget()
    select_gangfac_frame.forget()

    author_input_frame.forget()
    author_input_frame2.forget()
    # Start Tkinter event - loop
    root_window.title("Legal Disclaimer")
    root_window.mainloop()
