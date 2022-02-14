#-------------Obsidian: Quick daily note writer------------#
# Author: Adrian Papineau
# Date created: February 14th, 2022

# A simple one-line quick entry GUI for your Obsidian daily notes in markdown format. 


from PyQt5.QtWidgets import * 
import sys
from datetime import date
import time
import glob, os  

###------------------------------------------###


ObsidianVaultFolder = ""    # Example :"C:/Users/User/Documents/ObsidianVault/VaultName"
DailyNotesFolder = ""       # Example :"C:/Users/User/Documents/ObsidianVault/VaultName/DailyNotes"
DateFormat = 1 

'''
DateFormat 1 = MMMM Do, YYYY (November 22,2021)
DateFormat 2 = YYYY-MM-DD (2021-11-22)
'''

#return current daily note file path
def RoamFormatDate(): 
    today = date.today()
    dateExtractMonth = today.strftime('%B')
    dateExtractDay = today.strftime('%d')
    dateExtractYear = today.strftime('%Y')
    # Get rid of the beginning 0 in day of the month. 
    if dateExtractDay[0] == "0":
        dateExtractDay = dateExtractDay[-1]
    # Add the "th" or similar
    if ((int(dateExtractDay) >= 10) and (int(dateExtractDay) <20)) or (dateExtractDay[-1] == "0") or ((int(dateExtractDay[-1]) >=4) and (int(dateExtractDay[-1]) <10)):       
        dateExtractNUM = str(dateExtractDay + "th")
    elif dateExtractDay[-1] == "1":       
        dateExtractNUM = str(dateExtractDay + "st")
    elif dateExtractDay[-1] == "2":       
        dateExtractNUM = str(dateExtractDay + "nd")
    elif dateExtractDay[-1] == "3":       
        dateExtractNUM = str(dateExtractDay + "rd")
    RoamFormat = str(dateExtractMonth + " " + dateExtractNUM + ", " + dateExtractYear)
    return RoamFormat
#print("Roam format date is: " + RoamFormatDate())
def SecondFormatDate():
    dateFormat = str(date.today())
    return dateFormat
#print("Second format date is: " + SecondFormatDate())

def CurrentDate():
    if DateFormat == 1:
        return RoamFormatDate()
    if DateFormat == 2:
        return SecondFormatDate()
    else:
        print("Invalid number selection for DateFormat")

def CurrentDailyNote():
    DailyNoteName = (CurrentDate() + ".md")
    DailyNotePath = DailyNotesFolder + "/" + DailyNoteName
    return DailyNotePath
print("Currently monitoring the daily note: " + "\n" + CurrentDailyNote())

###------------------------------------------###

def getTime():
    currentTime = time.strftime("%H:%M")
    return(str(currentTime))


class Window(QDialog):
  
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Quick daily note entry")
        self.setGeometry(100, 100, 500, 100)# setting geometry to the window
        self.formGroupBox = QGroupBox("Daily note entry")
        self.nameLineEdit = QLineEdit()    
        self.createForm()    
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)      
        self.buttonBox.accepted.connect(self.getInfo)      
        self.buttonBox.rejected.connect(self.reject)   
        mainLayout = QVBoxLayout()   
        mainLayout.addWidget(self.formGroupBox)      
        mainLayout.addWidget(self.buttonBox)  
        self.setLayout(mainLayout)
    
    def getInfo(self): 
        currentEntry = (self.nameLineEdit.text())
        AppendToNote(getTime() + " " + str(currentEntry))
        self.close() 

    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("-"), self.nameLineEdit)
        self.formGroupBox.setLayout(layout)
  
###-----###

def NotePath():
    LinkName = (RemoveAlias() + ".md")
    LinkNotePath = ObsidianVaultFolder + "/" + LinkName
    return(LinkNotePath)

def AppendToNote(desiredBlock):
    Notefile = open(CurrentDailyNote(), encoding="utf8")
    NoteContent = Notefile.read()
    Notefile.seek(0)
    Notefile = open(CurrentDailyNote(), "w", encoding="utf8")
    Notefile.write(NoteContent + "\n" + "- " + desiredBlock)
    print("Sucessfully wrote to desired note")
    Notefile.seek(0)
    Notefile.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())