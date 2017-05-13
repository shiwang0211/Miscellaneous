import subprocess
import time
import os
import sys
import glob
import re

path = os.getcwd()     
DateTime = re.compile(r'([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] - [0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])')
LineStart = (' 1 2 3')
Factor = re.compile('[0-9]\.[0-9][0-9]')
Area = re.compile(r'ALLCategory: (.*)')



for file in glob.glob(path + '/*.txt'):
    with open(file,'r') as f:
        DateTimes=[]
        Factors=[]
        Areas=[]
        for line in f:
          if ('ALLCategory' in line):
              Areas.extend(Area.findall(line))
              
          if (LineStart in line):
              DateTimes = DateTime.findall(line)
              L = len(DateTimes)
              Factors.extend(Factor.findall(line)[:L])

              
    fsum=open(path + '/Seasonal Adjustement Factor Summary' + os.path.basename(file),'w')
    firstline = '\t' + '\t'.join(Areas)
    fsum.write(firstline + '\n')

    line=''

    for i in range(0,L):
        line = line + DateTimes[i]
        for j in range(0,len(Areas)):
            line = line + '\t' + Factors[L * j + i]
        fsum.write(line + '\n')
        line=''

    fsum.close()
