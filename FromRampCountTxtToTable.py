import subprocess
import time
import os
import sys
import glob
import re

folders = []
folders.append('/District 1 (US 27) - 2014/Michael_I4_BTU/')
folders.append('/District 5 - 2016/HOURLY VOLUMES/')
               
path = os.getcwd()     
TimeStamp = re.compile(r'([0-9][0-9])00  ')# we want to find the Hour in parenthesis
fsum=open(path + '/Ramp_Count_Summary.txt','w')
          

for folder in folders:
               
    for file in glob.glob(path + folder + '*.syn'):
      pre, ext = os.path.splitext(file)
      os.rename(file, pre + ".txt")

    for file in glob.glob(path + folder +'*.txt'):
        with open(file,'r') as f:
            for line in f:
                if ('Station:' in line):
                    stationID=int(line.split(':')[1])

                if ('Start Date:' in line):
                    startDate=line.split(':   ')[1].replace('\n','',1)

                if(TimeStamp.match(line)):#only match start
                    Hour = TimeStamp.match(line).group(0)[:2] 
                    volumes = line.split()
                    fsum.write(str(stationID) + '\t' + startDate + '\t' + Hour + ':00' + '\t' + str(volumes[1]) + '\n')
                    fsum.write(str(stationID) + '\t' + startDate + '\t' + Hour + ':15' + '\t' + str(volumes[2])+ '\n')
                    fsum.write(str(stationID) + '\t' + startDate + '\t' + Hour + ':30' + '\t' + str(volumes[3]) + '\n')
                    fsum.write(str(stationID) + '\t' + startDate + '\t' + Hour + ':45' + '\t' + str(volumes[4]) + '\n')


fsum.close()
