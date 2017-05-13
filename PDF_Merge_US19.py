import sys
import os
sys.path.append('C:/Python27/ArcGIS10.2/Lib')
import PyPDF2

pagenums = [1,2,3,4,5,6,7,8,9,10,13,11,12]
subdirs = [x[0] for x in os.walk(os.getcwd())] # get all subfolders
subdirs.pop(0)

path=os.getcwd()

##for subdir in subdirs:
##    
##    pdfFiles = []
##    pdfWriter = PyPDF2.PdfFileWriter()
##    
##    for filename in os.listdir(subdir): # get all pdf files under each subfolder
##        if filename.endswith('.pdf'):
##            pdfFiles.append(filename)
##            
##    for pageNum in pagenums:
##        for pdffile in pdfFiles:
##            pdfFileObj = open(subdir + "\\" + pdffile, 'rb')
##            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
##            pageObj = pdfReader.getPage(pageNum-1)
##            pdfWriter.addPage(pageObj)
##
##    pdfOutput = open(subdir.split("\\")[-1] + '.pdf', 'wb') # name export pdf with subfolder name
##    pdfWriter.write(pdfOutput)
##    pdfOutput.close()

AppendixF=[]
AppendixG=[]
for filename in os.listdir("."): # get all pdf files under each subfolder
    if 'F - ' in filename and filename.endswith('.pdf'): AppendixF.append(filename)
    if 'G - ' in filename and filename.endswith('.pdf'): AppendixG.append(filename)

    
##pdfWriter = PyPDF2.PdfFileWriter()
##for pdfFile in AppendixF:
##    pdfFileObj = open(path + "\\" + pdfFile, 'rb')
##    pdfReader = PyPDF2.PdfFileReader(pdfFile)
##    for pageNum in range(pdfReader.numPages):
##        pdfWriter.addPage(pdfReader.getPage(pageNum))
##
##pdfOutput = open(path + '\\' + 'AppendixF.pdf', 'wb')
##pdfWriter.write(pdfOutput)
##pdfOutput.close()

pdfWriter = PyPDF2.PdfFileWriter()
for pdfFile in AppendixG:
    pdfFileObj = open(path + "\\" + pdfFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    for pageNum in range(pdfReader.numPages):
        pdfWriter.addPage(pdfReader.getPage(pageNum))

pdfOutput = open(path + '\\' + 'AppendixG.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()
