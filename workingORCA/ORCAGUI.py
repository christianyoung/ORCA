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
        
import Tkinter, shutil, distutils.dir_util
import dateutil
from dateutil.relativedelta import *
import time
from datetime import *
import glob
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
global delNodeList
global delIR
global alteredProject
global author
global select_gangfac_frame_path
global nday
global nyear
global nmonth
global recDir
global projDir
global gangFac
global prevDir
global gangFacFrameFlag

PrintableNames = []
displayVar = ""
displayVar6 = ""
gangFac = 1
prevDir = ""
gangFacFrameFlag = 0
     #for the gang/fac selection menu
Options= []  #contains the name and full path FACTIONS (ie "FAC-79THAND..., C:/users/.../ORG-RES/FAC-79THAND...")
Options2=[]  #contains the name and full path for GANGS

def isIntList(intList):
    try:
        for i in intList: 
            int(i)
            return True
    except:
        return False

#makes sure a folder exists
def ensure_dir(f):
    if not os.path.isdir(f):
        os.makedirs(f)

def monthToInt(month):
        monthToIntDict = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,
                          "october":10,"november":11,"december":12,"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,
                          "aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
        return monthToIntDict[month.strip().lower()]

def ensureRecProj(rDir,pDir):
    ensure_dir(rDir)
    ensure_dir(rDir+'\\arRecords')
    ensure_dir(rDir+'\\arRelationships')
    ensure_dir(rDir+'\\nonArRecords')
    ensure_dir(rDir+'\\nonArRelationships')
    ensure_dir(rDir+'\\RemovedNodes')
        
    ensure_dir(pDir)

def readPrefs(prefPath):
    prefs = open(prefPath,'r')
    readlines = []
    for line in prefs:
        readlines.append(line)
    arRec = readlines[0].split(',')[0].strip()
    arEdge = readlines[0].split(',')[1].strip()
    nonArRec = readlines[0].split(',')[2].strip()
    nonArEdge = readlines[0].split(',')[3].strip()
    remNodes = readlines[0].split(',')[4].strip()
    dateString = readlines[1].split(',')[0].strip()
    day = readlines[1].split(',')[1].strip()
    month = readlines[1].split(',')[2].strip()
    year = readlines[1].split(',')[3].strip()
    gangOrFac = readlines[2].split(',')[0].strip()
    arFlag = readlines[2].split(',')[1].strip()
    nonArFlag = readlines[2].split(',')[2].strip()
    removedFlag = readlines[2].split(',')[3].strip()
    prefs.close()
    return arRec, arEdge, nonArRec, nonArEdge, remNodes, dateString, day, month, year, gangOrFac, arFlag, nonArFlag, removedFlag

def listToFile(list_, dst):
    file_ = open(dst, 'w')
    file_.write("IR\n")
    for item in list_:
        file_.write(item+'\n')
    file_.close()

def saveSettings(purgeAr,purgeNonAr,purgeProj,months1,months2,months3,recDir,projDir):
    """
    settings file format follows:
    
    purgeAr(1 = on, 0 = off),months1
    purgeNonAr(1 = on, 0 = off),months2
    purgeProj(1 = on, 0 = off),months3
    Record Directory
    Project Directory
    
    """
    global displayVar
    global displayVar6
    
    try:
        if purgeAr == 1:
            int(months1.strip())
        if purgeNonAr == 1:
            int(months2.strip())
        if purgeProj == 1:
            int(months3.strip())
    except:
        tkMessageBox.showerror("Invalid Input", "The number of months is invalid, please go back or try again.")
        return
    try:
        os.exists(recDir)
    except:
        try:
            ensureRecProj(recDir,projDir)
        except:
            tkMessageBox.showerror("Invalid Input", "The record directory is empty, please go back or try again.")

##    readlines = []
##    fr = open('settings','r')
##    for line in fr:
##        readlines.append(line)
##    fr.close()
    writelines = []
    writelines.append(str(purgeAr)+','+str(months1).strip()+'\n')
    writelines.append(str(purgeNonAr)+','+str(months2).strip()+'\n')
    writelines.append(str(purgeProj)+','+str(months3).strip()+'\n')
    writelines.append(str(recDir)+'\n')
    writelines.append(str(projDir)+'\n')
    fw = open('settings','w')
    for line in writelines:
        fw.write(line)
    fw.close()
    displayVar = recDir
    displayVar6 = projDir
    tkMessageBox.showinfo("Saved", "Settings Saved.")

def overwriteDialog():
    result = tkMessageBox.askquestion("Project Already Exists", "You have given a project name that\
already exists as a file directory. Would you like to overwrite?", icon='warning')
    if result == 'yes':
        return True
    else:
        return False
    

def submitnew(gangOrFac,ar,nonAr,removal,day,month,year, forcastFlag):
    monthToIntDict = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    yearOne = datetime.strptime('110001', "%d%m%Y").date()
    
    if day == "Day" or month == "Month" or year == "Year":
        dateLimit = yearOne
    else:
        dateLimit = datetime.strptime(str(day)+str(monthToIntDict[month])+str(year), "%d%m%Y").date()

    recordDirectory = displayVar
    if os.path.basename(recordDirectory) == 'recordsFolder':
            ensure_dir(recordDirectory+'\\arRelationships')
            ensure_dir(recordDirectory+'\\arRecords')
            ensure_dir(recordDirectory+'\\nonArRelationships')
            ensure_dir(recordDirectory+'\\nonArRecords')
            ensure_dir(recordDirectory+'\\RemovedNodes')
            ensure_dir(recordDirectory+'\\Blank')
            blankFiles = glob.glob(recordDirectory+'/Blank/*')
            for f in blankFiles:
                os.remove(f)
            
    for root, dirs, files in os.walk(recordDirectory):
        if os.path.basename(root) == 'records':
            for i in dirs:
                    if i == 'arRelationships':
                        arEdge = os.path.join(recordDirectory, i)
                    elif i == 'arRecords':
                        arRec = os.path.join(recordDirectory, i)
                    elif i == 'nonArRelationships':
                        nonArEdge =os.path.join(recordDirectory, i)
                    elif i == 'nonArRecords':
                        nonArRec =os.path.join(recordDirectory, i)
                    elif i == 'RemovedNodes':
                        remNodes = os.path.join(recordDirectory, i)
    if ar == 0:
        arEdge = os.path.join(recordDirectory, 'Blank')
        arRec = os.path.join(recordDirectory, 'Blank')
    if nonAr == 0:
        nonArEdge = os.path.join(recordDirectory, 'Blank')
        nonArRec = os.path.join(recordDirectory, 'Blank')
    if removal == 0:
        remNodes = os.path.join(recordDirectory, 'Blank')
    thePath = displayVar6
    initFolder = displayVar7.get()
    delim = "\t"
    if initFolder == "":
            tkMessageBox.showerror("Blank Entry","Enter a name for the altered project.")
            return
    elif os.path.isdir(thePath+"\\"+initFolder) and not forcastFlag:
        if not overwriteDialog():
            return

    ensure_dir(thePath+'\\'+initFolder)
    if day == "Day" or month == "Month" or year == "Year":
       dateString = '110001'
    else:
        dateStringList = [str(day),str(monthToInt(month)),str(year)]
        if len(dateStringList[0]) == 1:
            dateStringList[0] = '0'+dateStringList[0]
        if len(dateStringList[1]) == 1:
            dateStringList[1] = '0'+dateStringList[1]
        if len(dateStringList[2]) == 2:
            dateStringList[2] = '20'+dateStringList[2]
        dateString = str(dateStringList[0])+str(dateStringList[1])+str(dateStringList[2])
    prefs = open(displayVar6+'\\'+displayVar7.get()+'\\DataPreferences','w')
    prefs.write(str(arRec)+','+str(arEdge)+','+str(nonArRec)+','+str(nonArEdge)+','+str(remNodes)+'\n')
    prefs.write(dateString+','+day+','+month+','+year+'\n')
    prefs.write(str(gangOrFac)+','+str(ar)+','+str(nonAr)+','+str(removal)+','+str(ar)+'\n')
    prefs.close()

    newRemNodes = thePath+'\\'+initFolder+'\\projectRemoved'

    if forcastFlag:
        remNodes = prevDir+'\\projectRemoved'
    
    ensure_dir(newRemNodes)
    distutils.dir_util.copy_tree(remNodes, newRemNodes)

    if forcastFlag:
        shutil.copy(displayVar5.get()+'\\removeMore.dsv',newRemNodes)
        remNodes = newRemNodes
        
    cmw.mainW(thePath, initFolder, arRec,arEdge,nonArRec,nonArEdge,remNodes,dateLimit,gangOrFac,delim)
    displayVar5.set(thePath+"\\"+ initFolder)
    submitold()


def forecastNodes(IRorFile):
    global prevDir
    nodeList = []
    valid = False
    thePath = os.path.dirname(os.path.abspath(str(displayVar5.get())))
    initFile = os.path.split(os.path.abspath(str(displayVar5.get())))[1]
    newFolder = alteredProject.get()
    IRList = delIR.get().split(',')
    index = 0
    prevDir = str(displayVar5.get())
    
    for i in IRList:
        IRList[index] = i.strip()
        index += 1
    if IRorFile == 0:
        if isIntList(IRList):
            for i in IRList:
                nodeList.append(str(i))
            valid = True
        else:
            tkMessageBox.showerror("IR invalid","The IR numbers entered are invalid.")
    else:
        try:
            f = open(os.path.abspath(delNodeList.get()),'r')
            for line in f:
                nodeList.append(str(int(line)))
            f.close()
            valid = True
        except:
            tkMessageBox.showerror("File invalid","The node list file entered is invalid.")
    if valid:
        if alteredProject.get() == "":
            tkMessageBox.showerror("Blank Entry","Enter a name for the altered project.")
            return
        elif os.path.isdir(thePath+"\\"+newFolder):
            if not overwriteDialog():
                return

            
##            forecastRem = displayVar6+'\\'+displayVar7.get()+'\\forecastRem'
##            ensure_dir(forecastRem)
##            for filename in os.listdir(remNodes):
##                if not os.path.exists(forecastRem+'\\'+filename):
##                    shutil.copy(os.path.abspath(remNodes+'\\'+filename),forecastRem)
##                    
##            readlines = []
##            prefs = open(thePath+'\\'+initFolder+'\\DataPreferences','r')
##            for line in prefs:
##                    readlines.append(line.split(','))
##            prefs.close()
##            arRec = readlines[0][0].strip()
##            arEdge = readlines[0][1].strip()
##            nonArRec = readlines[0][2].strip()
##            nonArEdge = readlines[0][3].strip()
##            remNodes = readlines[0][4].strip()
##            dateLimit = datetime.strptime(readlines[1][0].strip(), "%d%m%Y").date()
##            gangOrFac = int(readlines[2][0].strip())
##            
            #whatIf.whatIf(thePath,initFile,newFolder,nodeList,'\t')
        prefs = readPrefs(displayVar5.get()+'\\DataPreferences')
        
        displayVar5.set(thePath+"\\"+ newFolder)
        displayVar7.set(newFolder)
        displayVar6 = thePath

        ensure_dir(displayVar5.get())
        listToFile(nodeList, displayVar5.get()+'\\removeMore.dsv')
        
        submitnew(int(prefs[9]),int(prefs[10]),int(prefs[11]),int(prefs[12]),prefs[6],prefs[7],prefs[8], True)
        select_gangfac_frame_path.set(thePath+"\\"+ newFolder + "\\ORG-RES")
        call_select_gangfac_on_top()
    
    
#opens a project that has already been processed
def submitold():
    global gangFac
    GangFac1 = 0
    GangFac2= 0
    path = displayVar5.get()
    path = path + "\\ORG-RES"
    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for dirname in dirnames:
                if dirname[0:3] == 'FAC':
                    GangFac1 = 1
                    gangFac = 1
                    
                if dirname[0:4] == 'GANG':
                    GangFac2= 1
                    gangFac = 0
        if (GangFac1 and GangFac2):
            tkMessageBox.showerror("Error","This directory has more than one analysis and will not be opened.")
        elif (gangFacFrameFlag == 0):
            create_widgets_in_select_gangfac_frame(path,GangFac1)
            
        call_select_gangfac_on_top()
    else:
        tkMessageBox.showerror("Analysis Not Found", "No ORCA analysis found in that folder.\
 Please double check the name and path of the analysis you are looking for.")
    
def load_file():
    global displayVar
    fname = askdirectory(mustexist=True, title = "find the Record Folder Directory.",initialdir=displayVar)
    if fname:
        try:
              displayVar = fname
        except:                     
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

def load_file0():
     fname = askopenfilename(title = "find the List File.")
     if fname:
        try:
              delNodeList.set(fname)
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
     fname5 = askdirectory(mustexist=True, title = "find the Project Directory",initialdir=displayVar6)
     if fname5:
        try:
           displayVar5.set(fname5)
        except:                    
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

def load_fileRec():
     fname5 = askdirectory(mustexist=True, title = "find the Record Folder Directory.",initialdir=displayVar6)
     if fname5:
        try:
           recDir.set(fname5)
        except:                    
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

def load_fileProj():
     fname5 = askdirectory(mustexist=True, title = "find the Project Directory",initialdir=displayVar6)
     if fname5:
        try:
           projDir.set(fname5)
        except:                    
              showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return
    
def load_file6():
    global displayVar6
    fname6 = askdirectory(mustexist=True, title = "find the directory you would like this project to be saved in")
    if fname6:
        try:
            displayVar6 = fname6
        except:                     
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return



def create_widgets_in_first_frame():
    
    #photo=PhotoImage(file='CPDLogo.gif')
    
    disclaimer ="""ORCA Software
 
This version of ORCA has been created by students and faculty of the Dept. of Electrical Engineering and Computer Science at the U.S. Military Academy, West Point, NY. \nYou are granted unlimited, unrestricted use of this software.
 
This software was created by the U.S. Department of Defense (US DoD). All intellectual property rights are retained by the US DoD. Please contact MAJ Paulo Shakarian if you wish to re-distribute this software in any way.
 
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
    second_window_label.grid(column=0, row=0,columnspan=2, pady=10, padx=10, sticky=(Tkinter.N))

    
    second_window_back_button = Tkinter.Button(second_frame, text = "Open Existing", command = call_open_existing_on_top)
    second_window_back_button.grid(column=0, row=1, pady=10, sticky=(Tkinter.N))
    second_window_next_button = Tkinter.Button(second_frame, text = "Create New", command = call_create_new_on_top)
    second_window_next_button.grid(column=1, row=1, pady=10, sticky=(Tkinter.N))
    second_window_settings_button = Tkinter.Button(second_frame, text = "Records Management", command = call_settings_on_top)
    second_window_settings_button.grid(column=0, row=2, columnspan = 2, pady=10, padx=20, sticky=(Tkinter.N))
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
    
    fullpath = analyzeThis[1] + "\\" + "BULLETS-" + analyzeThis[0] + ".csv"
    os.startfile(fullpath)
def Show_Connectors(analyzeThis):

    fullpath = analyzeThis[1] + "\\" + "CONNECTORS-" +analyzeThis[0]+".csv"
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

def create_widgets_in_settings_frame():
    def disabledCheck():
        if arPurge.get() == 0:
            entryWidget.configure(state='disabled')
            numMonths1.set(" ")
        else:
            entryWidget.configure(state='normal')
        if nonArPurge.get() == 0:
            entryWidget5.configure(state='disabled')
            numMonths2.set(" ")
        else:
            entryWidget5.configure(state='normal')
        if projPurge.get() == 0:
            entryWidget6.configure(state='disabled')
            numMonths3.set(" ")
        else:
            entryWidget6.configure(state='normal')

    readlines = []
    fr = open('settings','r')
    for line in fr:
        readlines.append(line)
    fr.close()
    oldPurgeAr = readlines[0].split(',')[0]
    oldPurgeNonAr = readlines[1].split(',')[0]
    oldPurgeProj = readlines[2].split(',')[0]
    oldMonths1 = readlines[0].split(',')[1]
    oldMonths2 = readlines[1].split(',')[1]
    oldMonths3 = readlines[2].split(',')[1]
    oldRecDir = readlines[3].strip()
    oldProjDir = readlines[4].strip()

    
    tipTopFrame = Frame(settings_frame)
    topFrame = Frame(settings_frame)
    bottomFrame=Frame(settings_frame)
    ttFrame1 = Frame(tipTopFrame)
    ttFrame2 = Frame(tipTopFrame)
    textFrame = Frame(bottomFrame)
    textFrame5= Frame(bottomFrame)
    textFrame6= Frame(bottomFrame)
    textFrame7= Frame(bottomFrame)
    textFrame8= Frame(bottomFrame)
    del_window_label = Tkinter.Label(topFrame, wraplength = 300,justify='left', text='Retention Scheduling: \nCheck a box to purge data older than x months on start up. An unchecked box means that purging is turned off.')
    del_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(Tkinter.N))
    arPurge = IntVar()
    nonArPurge = IntVar()
    projPurge = IntVar()
    numMonths1 = StringVar()
    numMonths2 = StringVar()
    numMonths3 = StringVar()
    arCheck = Checkbutton(textFrame5, text = "Arrest Data", variable = arPurge, onvalue = 1, offvalue = 0, command = disabledCheck)
    nonArCheck = Checkbutton(textFrame6, text = "Non Arrest Data", variable = nonArPurge, onvalue = 1, offvalue = 0, command = disabledCheck)
    projCheck = Checkbutton(textFrame7, text = "Saved Projects", variable = projPurge, onvalue = 1, offvalue = 0, command = disabledCheck)
    entryLabel1= Label(ttFrame1,text='Records Directory: ')
    entryLabel2= Label(ttFrame2,text='Project Directory: ')
    entryWidget2 = Entry(ttFrame1, textvariable = recDir)
    entryWidget3 = Entry(ttFrame2, textvariable = projDir)
    entryWidget = Entry(textFrame5, textvariable = numMonths1)
    entryWidget5 = Entry(textFrame6, textvariable = numMonths2)
    entryWidget6 = Entry(textFrame7, textvariable = numMonths3)
    entryWidget2["width"] = 25
    entryWidget3["width"] = 25
    entryWidget["width"] = 5
    entryWidget5["width"] = 5
    entryWidget6["width"] = 5
    browseButton1 = Button(ttFrame1, text= "browse...", command=load_fileRec,width=10)
    browseButton2 = Button(ttFrame2, text= "browse...", command=load_fileProj,width=10)
    
    arPurge.set(oldPurgeAr)
    nonArPurge.set(oldPurgeNonAr)
    projPurge.set(oldPurgeProj)
    numMonths1.set(oldMonths1)
    numMonths2.set(oldMonths2)
    numMonths3.set(oldMonths3)
    recDir.set(oldRecDir)
    projDir.set(oldProjDir)
    disabledCheck()

    back = Button(textFrame8, text = "Back", command=call_second_frame_on_top, width=10)
    back.pack(side = LEFT)
    Submit = Button(textFrame8, text = "Save Settings", command=  lambda: saveSettings(arPurge.get(),nonArPurge.get(),projPurge.get(),numMonths1.get(),numMonths2.get(),numMonths3.get(),recDir.get(),projDir.get()), width=15)
    Submit.pack(side = LEFT)

    entryLabel1.pack(side = LEFT)
    entryLabel2.pack(side = LEFT)
    entryWidget2.pack(side = LEFT)
    entryWidget3.pack(side = LEFT)
    browseButton1.pack(side = LEFT)
    browseButton2.pack(side = LEFT)
    arCheck.pack(side = LEFT)
    entryWidget.pack(side = LEFT)
    nonArCheck.pack(side = LEFT)
    entryWidget5.pack(side = LEFT)
    projCheck.pack(side = LEFT)
    entryWidget6.pack(side = LEFT)
    ttFrame1.pack()
    ttFrame2.pack()
    textFrame.pack()
    textFrame5.pack()
    textFrame6.pack()
    textFrame7.pack()
    textFrame8.pack()
    tipTopFrame.pack()
    topFrame.pack()
    bottomFrame.pack()

def create_widgets_in_delNode_frame():
    entryLabel= Label(delNode_frame, anchor = "e")
    entryLabel.grid(column=0, row=1, sticky=W)
    entryLabel5= Label(delNode_frame)
    entryLabel5.grid(column=0, row=2, sticky=W)
    entryLabel6= Label(delNode_frame)
    entryLabel6.grid(column=0, row=3, sticky=W)
    del_window_label = Tkinter.Label(delNode_frame, wraplength = 300, text='Submit a file with a list of nodes, or submit IR numbers separated by comma.')
    del_window_label.grid(column=0, row=0, columnspan=3, sticky=(Tkinter.N))
    entryLabel["text"] = "Node List File:"
    entryLabel5["text"] = "IR Numbers:"
    entryLabel6["text"] = "Altered Project Name:"

    entryWidget = Entry(delNode_frame, textvariable = delNodeList)
    entryWidget.grid(column=1, row=1, sticky=W)
    entryWidget5 = Entry(delNode_frame, textvariable = delIR)
    entryWidget5.grid(column=1, row=2, sticky=W)
    entryWidget6 = Entry(delNode_frame, textvariable = alteredProject)
    entryWidget6.grid(column=1, row=3, sticky=W)
    entryWidget["width"] = 50
    entryWidget5["width"] = 50
    entryWidget6["width"] = 30
    
    browseButton = Button(delNode_frame, text= "browse...", command=load_file0,width=10)
    browseButton.grid(column=2, row=1, pady=10, padx=10, sticky=W)
    v = IntVar()
    fileButton = Radiobutton(delNode_frame, text = "List File", variable = v, value = 1)
    fileButton.grid(column=2, row=3, sticky=W)
    irButton=Radiobutton(delNode_frame, text = "IR", variable = v, value =0)
    irButton.grid(column=1, row=3, sticky=E)


    back = Button(delNode_frame, text = "Back", command=call_select_gangfac_on_top, width=10)
    back.grid(column=1, row=4, pady=10, padx=10, sticky=W)
    Submit = Button(delNode_frame, text = "Submit", command=  lambda: forecastNodes(v.get()), width=10)
    Submit.grid(column=1, row=4, pady=10, padx=10, sticky=E)
    
    

    
#Menu for viewing project analysis options(PDFs, excel, map, etc.)
def create_widgets_in_select_gangfac_frame(path,gangFac):
    global PrintableNames, gangFacFrameFlag
    select_gangfac_frame_path.set(path)
    def verifyinput(selection):
        global PrintableNames
        if selection in PrintableNames:
            if gangFac ==0:
                selection = "GANG-"+selection
            else:
                selection = "FAC-"+selection

            return (selection,str(select_gangfac_frame_path.get())+"\\"+selection)
        else:
            tkMessageBox.showerror("Error","The gang name entered is not recognized.")
    gangFacFrameFlag = 1
    textFrame = Frame(select_gangfac_frame)
    optionLabel = Label(textFrame)
    optionLabel["text"] = "Select a faction/gang from the dropdown"
    optionLabel.pack(side=LEFT)
    tempPrintableNames = []
    authorinputbool=False
    if gangFac:
        variableLength=4
    else:
        variableLength=5
    for (dirpath, dirnames, filenames) in os.walk(path):        
        for dirname in dirnames:
            tempPrintableNames.append(str(dirname[variableLength:]))
    PrintableNames = tempPrintableNames
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


    

    viewFullNetworkButton = Button(textFrame, text = "View Full Network (Map)", command = lambda: Show_View_Net_Map(verifyinput(selection.get())), width = 30)
    coreMemberAssocNetworkButton  = Button(textFrame, text = "View Core Member (Map)", command = lambda: Show_Core_Mem(verifyinput(selection.get())), width = 30)
    subGrpRelsButton  = Button(textFrame, text = "Sub Group Relations (Map)", command = lambda: Show_Sub_Group_Relations(verifyinput(selection.get())), width = 30)
    detailsOnSubGrpButton  = Button(textFrame, text = "Details on Sub-Group (Excel)", command = lambda: Show_Details_SubGroup(verifyinput(selection.get())), width = 30)
    connectorsButton = Button(textFrame, text = "Connecting Members (Excel)", command = lambda: Show_Connectors(verifyinput(selection.get())), width = 30)
    statsButton = Button(textFrame, text = "Membership Breakdown (Excel)", command = lambda: Show_stats(verifyinput(selection.get())), width = 30)
    pdfButton = Button(textFrame, text = "View Full Report (PDF)", command = lambda: viewPDF(verifyinput(selection.get())), width = 30)
    tacpdfButton=Button(textFrame,text = "View Tactical Report (PDF)",command=lambda:tacPDF(verifyinput(selection.get())),width = 30)
    delNodesButton=Button(textFrame,text = "Forecast",command=call_del_nodes_on_top,width = 30)

    viewFullNetworkButton.pack()
    coreMemberAssocNetworkButton.pack()
    subGrpRelsButton.pack()
    detailsOnSubGrpButton.pack()
    connectorsButton.pack()
    statsButton.pack()
    delNodesButton.pack()
    pdfButton.pack()
    tacpdfButton.pack()
    
def create_widgets_in_create_new_frame():

    v = IntVar()
    ar = IntVar()
    nonAr = IntVar()
    removal = IntVar()
    nday = StringVar()
    nmonth = StringVar()
    nyear = StringVar()
    nac = IntVar()
    
    today = date.today()
    day = today.day
    month = today.month
    year = today.year

    monthToIntDict = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    intToMonthDict = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

    yearList = []
    monthList =["January","February","March","April","May","June","July","August","September","October","November","December"]
    dayList = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        
    for i in range(0,11):
        yearList.append(str(year-i))

    #change default based on policy
    defaultYear = year - 3
    defaultMonth = month
    if month != 2 or day != 29:
        defaultDay = day
    else:
        defaultDay = 28

    
    def naccheck():
        if nac.get() == 0:
            dayb.configure(state='disabled')
            monb.configure(state='disabled')
            yearb.configure(state='disabled')
            nday.set('Day')
            nmonth.set('Month')
            nyear.set('Year')
        else:
            dayb.configure(state='normal')
            monb.configure(state='normal')
            yearb.configure(state='normal')

    
    topFrame  = Frame(create_new_frame)
    textFrame = Frame(topFrame)
    textFrame2 = Frame(topFrame)
    textFrame3 = Frame(topFrame)
    bottomFrame=Frame(create_new_frame)
    textFrame5= Frame(bottomFrame)
    textFrame6= Frame(bottomFrame)
    textFrame7= Frame(bottomFrame)
    entryLabel= Label(textFrame, anchor = "e")
    entryLabel5= Label(textFrame5)
    entryLabel6= Label(textFrame6)
    entryLabel6["text"] = "Project Name:"
    entryLabel["width"]= 35
    

    entryLabel.pack(side = LEFT)
    entryLabel5.pack(side = LEFT)
    entryLabel6.pack(side = LEFT)
    entryWidget6 = Entry(textFrame6, textvariable = displayVar7)
    entryWidget6.pack(side = LEFT)
    

    textFrame.pack(anchor= "w")
    
    ArCheck = Checkbutton(textFrame2, text = "Arrest Data", variable = ar, onvalue = 1, offvalue = 0)
    nonArCheck = Checkbutton(textFrame2, text = "Non Arrest Data", variable = nonAr, onvalue = 1, offvalue = 0)
    removalCheck = Checkbutton(textFrame2, text = "Removal Data", variable = removal, onvalue = 1, offvalue = 0)

    ar.set(1)
    nonAr.set(1)
    removal.set(1)
        
    ck1 = Checkbutton(textFrame3, text='Pull records from today through:',variable=nac, command=naccheck)
    ck1.pack(side="left")

    dayb = OptionMenu(textFrame3, nday, *dayList)
    yearb = OptionMenu(textFrame3, nyear, *yearList)
    monb = OptionMenu(textFrame3, nmonth, *monthList)

    dayb.config(state='disabled',width=3)
    monb.config(state='disabled',width=10)
    yearb.config(state='disabled',width=7)

##    nday.set(defaultDay)
##    nmonth.set(intToMonthDict[defaultMonth])
##    nyear.set(defaultYear)

    nday.set('Day')
    nmonth.set('Month')
    nyear.set('Year')
    
    dayb.pack(side="left")
    monb.pack(side="left")
    yearb.pack(side="left")

    
    gangButton = Radiobutton(textFrame6, text = "Gang", variable = v, value = 0)
    factionButton=Radiobutton(textFrame6, text = "Faction", variable = v, value =1)

    ArCheck.pack(side=LEFT)
    nonArCheck.pack(side=LEFT)
    removalCheck.pack(side=LEFT)
    gangButton.pack(side = LEFT)
    factionButton.pack(side = LEFT)
    back = Button(textFrame7, text = "Back", command=call_second_frame_on_top, width=10)
    back.pack(side = LEFT)
    Submit = Button(textFrame7, text = "Create New", command=  lambda: submitnew(v.get(),ar.get(),nonAr.get(),removal.get(),nday.get(),nmonth.get(),nyear.get(), False), width=10)
    Submit.pack(side = LEFT)

    textFrame2.pack()
    textFrame3.pack()
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
    delNode_frame.forget()
    open_existing_frame.pack()
def call_del_nodes_on_top():
    root_window.title("Remove Nodes")
    select_gangfac_frame.forget()
    delNode_frame.pack()
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
    root_window.title("Main Menu")
    author_input_frame.forget()
    author_input_frame2.forget()
    open_existing_frame.forget()
    create_new_frame.forget()
    delNode_frame.forget()
    select_gangfac_frame.pack()

def call_settings_on_top():
    root_window.title("Records Managment")
    author_input_frame.forget()
    author_input_frame2.forget()
    open_existing_frame.forget()
    create_new_frame.forget()
    second_frame.grid_forget()
    delNode_frame.forget()
    select_gangfac_frame.forget()
    settings_frame.pack()

    
def call_first_frame_on_top():
    root_window.title("Legal Disclaimer")
   
    second_frame.grid_forget()
    first_frame.pack()
def call_second_frame_on_top():
    root_window.title("ORCA Analyzer")
    settings_frame.forget()
    first_frame.forget()
    third_frame.grid_forget()
    create_new_frame.forget()
    open_existing_frame.forget()
    select_gangfac_frame.forget()
    delNode_frame.forget()

    second_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def call_third_frame_on_top():

    second_frame.grid_forget()
    third_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))

def purge():
    global displayVar
    global displayVar6

    readlines = []
    try:
        fr = open('settings','r')
    except:
        writelines = []
        writelines.append('0,\n')
        writelines.append('0,\n')
        writelines.append('0,\n')
        writelines.append(os.path.abspath(os.path.dirname(sys.argv[0]))+'\\records\n')
        writelines.append(os.path.abspath(os.path.dirname(sys.argv[0]))+'\\projects\n')
        fw = open('settings','w')
        for line in writelines:
            fw.write(line)
        fw.close()
        return
    for line in fr:
        readlines.append(line)
    fr.close()
    oldPurgeAr = readlines[0].split(',')[0]
    oldPurgeNonAr = readlines[1].split(',')[0]
    oldPurgeProj = readlines[2].split(',')[0]
    oldMonths1 = readlines[0].split(',')[1]
    oldMonths2 = readlines[1].split(',')[1]
    oldMonths3 = readlines[2].split(',')[1]
    recDir = readlines[3].strip()
    projDir = readlines[4].strip()

    ensureRecProj(recDir,projDir)
    displayVar = recDir
    displayVar6 = projDir
    
    yearOne = datetime.strptime('110001', "%d%m%Y").date()
    today = date.today()
    arDate = yearOne
    nonArDate = yearOne
    projDate = yearOne
    arPath = os.path.abspath(recDir+'\\arRecords')
    nonArPath = os.path.abspath(recDir+'\\nonArRecords')
    if oldPurgeAr == '1' and os.path.isdir(arPath):
        arDate = today - relativedelta(months=int(oldMonths1.strip()))
        for filename in os.listdir(arPath):
            fullpath = os.path.join(arPath,filename)
            readlines = []
            r = open(fullpath,'r')
            for line in r:
                readlines.append(line)
            r.close()
            writelines = []
            first = True
            for line in readlines:
                if first:
                    writelines.append(line)
                    first = False
                else:
                    dateStringList = line.split('\t')[13].split('-')
                    dateStringList[1] = str(monthToInt(dateStringList[1]))
                    if len(dateStringList[0]) == 1:
                            dateStringList[0] = '0'+dateStringList[0]
                    if len(dateStringList[1]) == 1:
                            dateStringList[1] = '0'+dateStringList[1]
                    if len(dateStringList[2]) == 2:
                            dateStringList[2] = '20'+dateStringList[2]
                    dateString = str(dateStringList[0])+str(dateStringList[1])+str(dateStringList[2])
                    if datetime.strptime(dateString, "%d%m%Y").date() > arDate:
                        writelines.append(line)
            w = open(fullpath,'w')
            for line in writelines:
                w.write(line)
            w.close()
    if oldPurgeNonAr == '1' and os.path.exists(nonArPath):
        nonArDate = today - relativedelta(months=int(oldMonths2.strip()))
        for filename in os.listdir(nonArPath):
            fullpath = os.path.join(nonArPath,filename)
            readlines = []
            r = open(fullpath,'r')
            for line in r:
                readlines.append(line)
            r.close()
            writelines = []
            first = True
            for line in readlines:
                if first:
                    writelines.append(line)
                    first = False
                else:
                    dateStringList = line.split('\t')[12].split('-')
                    dateStringList[1] = str(monthToInt(dateStringList[1]))
                    dateStringList[2] = dateStringList[2].split(' ')[0]
                    if len(dateStringList[0]) == 1:
                            dateStringList[0] = '0'+dateStringList[0]
                    if len(dateStringList[1]) == 1:
                            dateStringList[1] = '0'+dateStringList[1]
                    if len(dateStringList[2]) == 2:
                            dateStringList[2] = '20'+dateStringList[2]
                    dateString = str(dateStringList[0])+str(dateStringList[1])+str(dateStringList[2])
                    if datetime.strptime(dateString, "%d%m%Y").date() > nonArDate:
                        writelines.append(line)
            w = open(fullpath,'w')
            for line in writelines:
                w.write(line)
            w.close()
#    if oldPurgeProj == '1' and os.path.exists(os.path.abspath('Projects')):
#        projDate = today - relativedelta(months=int(oldMonths3.strip()))

        

def quit_program():
    root_window.destroy()

if __name__ =="__main__":
    root_window = Tkinter.Tk()
    authorinputbool=False
    try:
        purge()
    except:
        print 'purge failed'
    window_width = 500
    window_height = 400
    selection  =StringVar()
##    displayVar2=StringVar()
##    displayVar3=StringVar()
##    displayVar4=StringVar()
    displayVar5=StringVar()
    displayVar7=StringVar()
    author  = StringVar()
    author.set("ORCA PDF")
    delNodeList=StringVar()
    delIR=StringVar()
    alteredProject=StringVar()
    select_gangfac_frame_path=StringVar()
    recDir = StringVar()
    projDir = StringVar()
    

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

    delNode_frame = Tkinter.Frame(root_window, width=window_width, height=window_height)
    delNode_frame['borderwidth'] = 2
    delNode_frame.grid(column=0, row=0,padx=20, pady =5, sticky=(Tkinter.W,Tkinter.N, Tkinter.E))

    settings_frame = Tkinter.Frame(root_window, width=window_width, height = window_height)
    settings_frame['borderwidth']=2
    settings_frame.pack()

    # Create all widgets to all frames
    create_widgets_in_third_frame()
    create_widgets_in_second_frame()
    create_widgets_in_first_frame()
    create_widgets_in_create_new_frame()
    create_widgets_in_open_existing_frame()
    create_widgets_in_delNode_frame()
    create_widgets_in_settings_frame()



    # Hide all frames in reverse order, but leave first frame visible (unhidden).
    delNode_frame.grid_forget()
    third_frame.grid_forget()
    second_frame.grid_forget()
    open_existing_frame.grid_forget()
    create_new_frame.forget()
    select_gangfac_frame.forget()
    settings_frame.forget()

    author_input_frame.forget()
    author_input_frame2.forget()
    # Start Tkinter event - loop
    root_window.title("Legal Disclaimer")
    root_window.mainloop()
