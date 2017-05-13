import sys
import os
#sys.path.append('C:/Python27/ArcGIS10.2/Lib')
import openpyxl
import re


def writecount(direction, MachineCountID, wb, fsum):
    sheet = wb.get_sheet_by_name(direction)
    for rowOfCellObjects in sheet['W104':'AK196']:
        fsum.write(MachineCountID + '\t')
        fsum.write(direction + '\t')
        for cellObj in rowOfCellObjects:
            fsum.write(str(cellObj.value) + '\t')
        fsum.write('\n')

fsum = open('MachineCountSummary.txt', 'w')           
path = os.getcwd()
CountIDMatch = re.compile(r'([0-9][0-9]?) - ')

MachineCountfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith(".xlsx") and "Class" in root]

for file in MachineCountfiles:
    MachineCountID = re.findall(CountIDMatch, file.split("\\")[-1])[0]
    wb = openpyxl.load_workbook(file, data_only=True)
    writecount('NB-EB',MachineCountID,wb,fsum)
    writecount('SB-WB',MachineCountID,wb,fsum)

fsum.close()
