import subprocess
import time
import os
import sys
import glob
import re

path = os.getcwd()     
TimeStamp = re.compile(r'([0-9][0-9]:[0-9][0-9])')# we want to find the Hour in parenthesis
fsum=open(path + '/TurnPike_Count_Summary.txt','w')
          
for file in glob.glob(path +'/*.txt'):
    stationID = file.split('_')[1]
    with open(file,'r') as f:
        for line in f:
            if(TimeStamp.match(line)):#only match start
                time = re.findall(TimeStamp, line)[0]
                volume = line.split()[1:]
                for weekday in xrange(0,5):
                    if (time == '12:00'): # switch AM and PM to display in excel
                        fsum.write(stationID + '\t' + time + ' ' + 'PM' + '\t' + str(weekday+1) + '\t' + volume[weekday*2] + '\n')
                        fsum.write(stationID + '\t' + time + ' ' + 'AM' + '\t' + str(weekday+1) + '\t' + volume[weekday*2+1] + '\n')
                    if (time != '12:00'):
                        fsum.write(stationID + '\t' + time + ' ' + 'AM' + '\t' + str(weekday+1) + '\t' + volume[weekday*2] + '\n')
                        fsum.write(stationID + '\t' + time + ' ' + 'PM' + '\t' + str(weekday+1) + '\t' + volume[weekday*2+1] + '\n')
               
fsum.close()
