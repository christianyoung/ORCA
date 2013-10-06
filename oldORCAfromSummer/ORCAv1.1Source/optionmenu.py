1.  # File name: tkinterOptionMenu.py
2.  # Author: S.Prasanna
3.
from Tkinter import *
import tkMessageBox

def displayOption():
   """ Display the OptionMenu selection. """
   global optionMenuWidget, DEFAULTVALUE_OPTION
   if (optionMenuWidget.cget("text") == DEFAULTVALUE_OPTION):
        tkMessageBox.showerror("Tkinter OptionMenu Widget", "Select a valid option.")
   else:
         tkMessageBox.showinfo("Tkinter OptionMenu Widget", "OptionMenu value =" + optionMenuWidget.cget("text"))
if __name__ == "__main__":
     root = Tk()
     DEFAULTVALUE_OPTION = "Select a faction."
     root.title("Tkinter OptionMenu Widget")
     root["padx"] = 40
     root["pady"] = 20 

     # Create an Option frame to hold the option Label and the optionMenu widget
     optionFrame = Frame(root)

    #Create a Label in textFrame
     optionLabel = Label(optionFrame)
     optionLabel["text"] = DEFAULTVALUE_OPTION
     optionLabel.pack(side=LEFT)

     # Create an optionMenu Widget in the optionFrame
     optionTuple = ("Option 1", "Option 2", "Option 3", "Option 4", "Option 5")

     defaultOption = StringVar()
     optionMenuWidget = apply(OptionMenu, (optionFrame, defaultOption) + optionTuple)
     defaultOption.set(DEFAULTVALUE_OPTION)
     optionMenuWidget["width"] = 15
     optionMenuWidget.pack(side=LEFT)

     optionFrame.pack()

     button = Button(root, text="Submit", command=displayOption)
     button.pack()
     root.mainloop()
