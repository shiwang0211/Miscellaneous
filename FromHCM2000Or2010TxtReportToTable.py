import os
import glob
import re

NodeNum = re.compile(r'([0-9]+):')
SignalDelay_2010 = re.compile(r'HCM 2010 Ctrl Delay   				([0-9]+.[0-9])')
SignalLOS_2010 = re.compile(r'HCM 2010 LOS          				([A-Z])')
SignalDelay_2000 = re.compile(r'HCM 2000 Control Delay				([0-9]+.[0-9])')
SignalLOS_2000 = re.compile(r'HCM 2000 Level of Service					([A-Z])')

def GetWorstOne(string):
    temp = string.replace('$ ',"").split('\n')[0].split('\t')
    temp.pop(0)
    temp2=[]
    while len(temp)>0:
        element = temp.pop()
        if (element.replace('.','',1).isdigit()) or (element>='A' and element <='F'): temp2.append(element)
    try:
        return(str(max(map(float,temp2))))
    except ValueError:
        if temp2 <> [] : return(max(temp2))
        if temp2 == [] : return('')
    
fsum=open('H:\\projfile\\13066 - FDOT D5 Districtwide Travel Demand Modeling\\TWO 23 and 24 SR 535 Corridor Study\\Synchro\\Existing Conditions\\Growth Rate Tests\\summary.txt','w')
for file in glob.glob('H:\\projfile\\13066 - FDOT D5 Districtwide Travel Demand Modeling\\TWO 23 and 24 SR 535 Corridor Study\\Synchro\\Existing Conditions\\Growth Rate Tests\\*.txt'):
    with open(file,'r') as f:
        fsum.write(file + '\n')
        for line in f:
            Node = NodeNum.findall(line)
            if (Node):
                fsum.write('\n' + Node[0] + '\t')
                if 'AM' in file: fsum.write('\t' + 'AM' + '\t')
                if 'PM' in file: fsum.write('\t' + 'PM' + '\t')
                
            if '2000' in file:
                delay1 = SignalDelay_2000.findall(line)
                if (delay1): fsum.write('\t' + delay1[0] + '\t')
                LOS1 = SignalLOS_2000.findall(line)
                if (LOS1): fsum.write('\t' + LOS1[0])
                if ('Control Delay (s)' in line): fsum.write('\t' + GetWorstOne(line) + '\t')
                if ('Lane LOS' in line): fsum.write('\t' + GetWorstOne(line))
                
            if '2010' in file:
                delay1 = SignalDelay_2010.findall(line)
                if (delay1): fsum.write('\t' + delay1[0] + '\t')
                LOS1 = SignalLOS_2010.findall(line)
                if (LOS1): fsum.write('\t' + LOS1[0])
                if ('HCM Control Delay (s)' in line): fsum.write('\t' + GetWorstOne(line) + '\t')
                if ('HCM Lane LOS' in line): fsum.write('\t' + GetWorstOne(line))
        fsum.write('\n')
fsum.close()
