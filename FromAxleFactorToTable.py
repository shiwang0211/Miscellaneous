import subprocess
import time
import os
import sys
import glob
import re

path = os.getcwd()     
DateTime = re.compile(r'([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] - [0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])')
LineStart = ('1 2 3 4 5 6 7 8 9 10')
Factor = re.compile('[0-9]\.[0-9][0-9]')
Area1 = re.compile(r'[0-9][0-9]   (.*?)[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]')
Area2 = re.compile(r'[0-9]\.[0-9][0-9]  (.*?)[0-9]\.[0-9][0-9]')



for file in glob.glob(path + '/*.txt'):
    with open(file,'r') as f:
        DateTimes=[]
        Factors=[]
        Areas=[]
        for line in f:
          if (LineStart in line):
              DateTimes = DateTime.findall(line)
              Factors.extend(Factor.findall(line))
              Areas.extend(Area1.findall(line))  
              Areas.extend(Area2.findall(line))

    fsum=open(path + '/Axle Correction Factor Summary' + os.path.basename(file),'w')
    firstline = '\t' + '\t'.join(Areas)
    fsum.write(firstline + '\n')

    line=''
    L1 = len(DateTimes)
    L2 = len(Factors)/len(DateTimes)

    for i in range(0,L1):
        line = line + DateTimes[i]
        for j in range(0,L2):
            line = line + '\t' + Factors[L1 * j + i]
        fsum.write(line + '\n')
        line=''

    fsum.close()
