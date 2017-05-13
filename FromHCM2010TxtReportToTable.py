import os
import glob
import re

NodeNum = re.compile(r'([0-9]+):')
SignalDelay = re.compile(r'HCM 2010 Ctrl Delay   				([0-9]+.[0-9])')
SignalLOS = re.compile(r'HCM 2010 LOS          				([A-Z])')

def GetWorstOne(string):
    temp = string.replace('$ ',"").split('\n')[0].split('\t')
    temp2=[]
    while len(temp)>0:
        element = temp.pop()
        if (element.replace('.','',1).isdigit()) or (element>='A' and element <='F'): temp2.append(element)
    try:
        return(str(max(map(float,temp2))))
    except ValueError:
        return(max(temp2))
    
fsum=open('H:\\projfile\\11730 - FDOT D5 Design Traffic and PDE Support\\TWO 43_US 301 DTTM\\Phase 2\\Figures\\HCM 2010 reports\\summary.txt','w')
for file in glob.glob('H:\\projfile\\11730 - FDOT D5 Design Traffic and PDE Support\\TWO 43_US 301 DTTM\\Phase 2\\Figures\\HCM 2010 reports\\*.txt'):
    with open(file,'r') as f:
        fsum.write(file + '\n')
        for line in f:
            Node = NodeNum.findall(line)
            if (Node):
                fsum.write(Node[0] + '\t')
                if 'AM' in file: fsum.write('\t' + 'AM' + '\t')
                if 'PM' in file: fsum.write('\t' + 'PM' + '\t')
            delay1 = SignalDelay.findall(line)
            if (delay1): fsum.write('\t' + delay1[0] + '\t')
            LOS1 = SignalLOS.findall(line)
            if (LOS1): fsum.write('\t' + LOS1[0] + '\n')
            if ('HCM Control Delay (s)' in line): fsum.write('\t' + GetWorstOne(line) + '\t')
            if ('HCM Lane LOS' in line): fsum.write('\t' + GetWorstOne(line) + '\n')
        fsum.write('\n')
        
fsum.close()
