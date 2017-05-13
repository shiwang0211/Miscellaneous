import subprocess
import time
import os
import sys
import glob
import re

folders = []
folders.append('/TEMP/')
               
path = os.getcwd()     
TimeStamp = re.compile(r'([0-9][0-9])00    ')# we want to find the Hour in parenthesis
Direction = re.compile(r'Direction: ([A-Z])')
fsum=open(path + '/Mainline_Summary_Nov15.txt','w')         

for folder in folders:
               
    for file in glob.glob(path + folder + '*.syn'):
      pre, ext = os.path.splitext(file)
      os.rename(file, pre + ".txt")

    for file in glob.glob(path + folder +'*.txt'):
        with open(file,'r') as f:
            for line in f:

                if ('County:' in line) | ('COUNTY:' in line):
                    County=int(line.split(':')[1])
                    
                if ('Station:' in line) | ('STATION:' in line):
                    stationID=str(County) + str(line.split(':')[1].strip())
                
                if ('Start Date:' in line) | ('START DATE:' in line):
                    startDate=line.split(':   ')[1].replace('\n','',1)
                    
                if (('Direction:' in line) & (not('Combined Directions' in line))) | (('DIRECTION:' in line) & (not('COMBINED DIRECTIONS' in line))):
                    Directions = Direction.findall(line)

                if(TimeStamp.match(line)):
                    Hour = TimeStamp.match(line).group(0)[:2] #only match the start of a string
                    volumes = line.split()
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':00' + '\t' + str(volumes[1]) + '\t' + Directions[0]  +'\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':15' + '\t' + str(volumes[2]) + '\t' + Directions[0]+ '\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':30' + '\t' + str(volumes[3]) + '\t' + Directions[0]  + '\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':45' + '\t' + str(volumes[4]) + '\t' + Directions[0]+ '\n')
                    
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':00' + '\t' + str(volumes[7]) + '\t' + Directions[1]  +'\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':15' + '\t' + str(volumes[8]) + '\t' + Directions[1]+ '\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':30' + '\t' + str(volumes[9]) + '\t' + Directions[1]+ '\n')
                    fsum.write(stationID + '\t' + startDate + '\t' + Hour + ':45' + '\t' + str(volumes[10]) + '\t' + Directions[1]+ '\n')


fsum.close()
