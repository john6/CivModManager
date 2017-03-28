from Tkinter import *
import sys, shutil, os
#from os import listdir
#Example SOURCEFOLDER"C:\Users\[User Name]\Documents\My Games\Sid Meier's Civilization 5 - Copy\MODS"
#Example DESTINATIONFOLDER = "Q:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V - Copy\Assets\DLC\Expansion2"
SOURCEFOLDER = ""
DESTINATIONFOLDER = ""


"""
Plan is to rewrite these as folders as args but lets just try it out first
"""

sourceFileNames = []
checkButtonNames = []
checkButtons = []
buttonToVar = {}
modsIncluded = []
sourcePathList = []
destPathList = []
dumbList = []


def GetFilesFromFolder(folder):
	#there is zero reason for this function
	fileNames = os.listdir(folder)
	return fileNames

def SubmitModSelection():
	for checkButton in checkButtons:
		if buttonToVar[checkButton[1]].get() == 1:
			modsIncluded.append(checkButton[0])
	window2.destroy()

def SubmitPathSelection():
	dumbList.append(sourcePathList[0].get())
	dumbList.append(destPathList[0].get())
	window1.destroy()
	return

def CopyPasteModFolder(modFolderNameList, sourceFolder, destinationFolder):
	for modFolderName in modFolderNameList:
		fullSourceName = sourceFolder + "\\" + modFolderName
		newFileName = destinationFolder + "\\" + modFolderName
		#print fullSourceName
		shutil.copytree(fullSourceName, newFileName)

def getXmlFileNames(modFolderNameList, sourceFolder):
	xmlFileNames = []
	for folderName in modFolderNameList:
		fullSourceName = sourceFolder + "\\" + folderName
		for window, dirs, files in os.walk(fullSourceName):
			for file in files:
				if file.endswith(".xml"):
					#print file
					xmlFileNames.append(file)
	return xmlFileNames

def CreatePathEntryGUI():
	window1.title("Select Filepath")
	window1.geometry("1250x500")
	sourcePathLabel = Label( window1, text="\n\nCopy, paste the complete filepath for 'Sid Meier's Civilization 5\MODS Folder'")
	sourcePathLabel2 = Label( window1, text="(C:\Users\[User Name]\Documents\My Games\Sid Meier's Civilization 5 - Copy\MODS)")
	sourcePathEntry = Entry(window1, bd =5)
	sourcePathList.append(sourcePathEntry)
	destPathLabel = Label( window1, text="\n\n\n\n\nCopy, paste the complete filepath for 'Sid Meier's Civilization V\Assets\DLC\Expansion2 Folder'")
	destPathLabel2 = Label( window1, text="(C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V - Copy\Assets\DLC\Expansion2)")
	destPathEntry = Entry(window1, bd =5)
	destPathList.append(destPathEntry)
	sourcePathLabel.pack()
	sourcePathLabel2.pack()
	sourcePathEntry.pack()
	destPathLabel.pack()
	destPathLabel2.pack()
	destPathEntry.pack()
	submitButton = Button(window1, text = "Submit", command = SubmitPathSelection)	
	submitButton.pack(pady = 20, padx = 20)
	window1.mainloop()

def CreateSelectionGUI(sourceFileNames):
	window2.title("Select MODS")
	window2.geometry("1250x500")
	for fileName in sourceFileNames:
		checkButtonVar = IntVar(window2)
		checkButton = Checkbutton(text=fileName, variable=checkButtonVar, onvalue=1, offvalue= 0)
		buttonToVar[checkButton] = checkButtonVar
		checkButtons.append([fileName, checkButton])
	for checkButton in checkButtons:
		checkButton[1].pack()
	submitButton = Button(window2, text = "Submit", command = SubmitModSelection)	
	submitButton.pack(pady = 20, padx = 20)
	window2.mainloop()

def EditCivPkgFile(xmlFileNames, destFolder):
	pkgFilePath = destFolder + "\\" + "Expansion2.Civ5Pkg"
	with open(pkgFilePath, 'r+') as openFile:
		origPkgText = openFile.read()	
		#print origPkgText
		fileAddition = ""
		for fileName in xmlFileNames:
			xmlLines = "<GameData>" + fileName + "</GameData>" + "\n" + "<TextData>" + fileName + "</TextData>" + "\n"
			#print xmlLines
			fileAddition += xmlLines
		fileAddition = "<Gameplay>\n\n" + "<!-- Mod Files -->" + "\n" + fileAddition + "<!-- End Of Mod Files -->"
		#print fileAddition
		newPkgText = str.replace(origPkgText, "<Gameplay>", fileAddition)
		#print newPkgText
		openFile.seek(0)
		openFile.write(newPkgText)
		openFile.truncate()

window1 = Tk()
CreatePathEntryGUI()
SOURCEFOLDER = dumbList[0]
DESTINATIONFOLDER = dumbList[1]
sourceFileNames = GetFilesFromFolder(SOURCEFOLDER)
window2 = Tk()
CreateSelectionGUI(sourceFileNames)
#print "MODS INCLUDED"
#print modsIncluded
#print "____________\n"
CopyPasteModFolder(modsIncluded, SOURCEFOLDER, DESTINATIONFOLDER)
xmlFiles = getXmlFileNames(modsIncluded, SOURCEFOLDER)
#print "xmlFiles"
#print xmlFiles
#print "____________\n"
EditCivPkgFile(xmlFiles, DESTINATIONFOLDER)