import glob
import re

NodeNum = re.compile(r'([0-9]+): ')
GrowRate = re.compile(r'_([0-9])_HCM')
SignalDelay_2010 = re.compile(r'HCM 2010 Ctrl Delay   				([0-9]+.[0-9])')
SignalLOS_2010 = re.compile(r'HCM 2010 LOS          				([A-Z])')
SignalDelay_2000 = re.compile(r'HCM 2000 Control Delay				([0-9]+.[0-9])')
SignalLOS_2000 = re.compile(r'HCM 2000 Level of Service					([A-Z])')
AppDelay_2010 = re.compile(r'LnGrp Delay\(d\),s/veh  (.+)')
AppDelay_2000 = re.compile(r'Approach Delay \(s\)    (.+)')
VC_2010 = re.compile(r'V/C Ratio\(X\)          (.+)') 
VC_2000 = re.compile(r'v/c Ratio             	(.+)') 

Path = 'H:\\projfile\\9891 - Brevard MPO General Planning\\Task 28 - Wickham Road Concept Development\\Synchro\\Existing Conditions\\HCM2010_Text_Report\\'
Signalized = True

def GetWorstOne(string): # Apply for both delay values and level of service "A-F"
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
    
def HCM_2000_VC(line):
    global Signalized
    VCs=VC_2000.findall(line) # Movement VC
    if(VCs and Signalized):  # Signalized v/c ratio for 12 movements
        VC=VCs[0].split('\t')
        VC.pop(0)
        for i in xrange(12): fsum.write('\t' + VC[i])
    if (not Signalized and 'Direction, Lane #' in line):# Non-signalized, placeholder only once
        for i in xrange(12): fsum.write('\t' + '')

def HCM_2010_VC(line):
    global Signalized
    VCs=VC_2010.findall(line) # Movement VC
    if(VCs and Signalized):  # Signalized v/c ratio for 12 movements
        VC=VCs[0].split('\t')
        VC.pop(0)
        VC.pop(0)
        for i in xrange(12): fsum.write('\t' + VC[i])
    if(not Signalized and 'Minor Lane/Major Mvmt' in line):# Non-signalized, placeholder only once
        for i in xrange(12): fsum.write('\t' + '')
        
        
def HCM_2000_AppDelay(line):
    global Signalized
    AppDelays=AppDelay_2000.findall(line)# Approach Delay
    if(AppDelays and Signalized):# Signalized Approach delay, four approaches
        AppDelay = AppDelays[0].replace('\t\n','').split('\t\t')
        AppDelay = [temp.replace('\t','') for temp in AppDelay]
        if AppDelay[0]=='' : AppDelay.pop(0)
        if AppDelay[0]=='' : AppDelay.pop(0)
        if len(AppDelay)>3: fsum.write('\t' + AppDelay[0] + '\t' + AppDelay[1] + '\t' + AppDelay[2] +  '\t' + AppDelay[3])
    if(not Signalized and 'Direction, Lane #' in line):# Non-signalized, placeholder only once
        fsum.write('\t' + '' + '\t' + '' + '\t' + '' +  '\t' + '')          

def HCM_2010_AppDelay(line): 
    global Signalized       
    AppDelays=AppDelay_2010.findall(line) # Approach Delay
    if(AppDelays and Signalized): # Signalized Approach delay, four approaches
        AppDelay = AppDelays[0].split('\t')
        AppDelay.pop(0)
        AppDelay.pop(0)
        fsum.write('\t' + AppDelay[1] + '\t' + AppDelay[4] + '\t' + AppDelay[7] +  '\t' + AppDelay[10])
    if(not Signalized and 'Minor Lane/Major Mvmt' in line):# Non-signalized, placeholder only once
        Signalized=False
        fsum.write('\t' + '' + '\t' + '' + '\t' + '' +  '\t' + '')          
        
        

        
def HCM_2000(line):
    
    global Signalized
    
    if 'Traffic Volume (vph)' in line: Signalized = True
    if 'Traffic Volume (veh/h)' in line: Signalized = False
    
    IntDelay = SignalDelay_2000.findall(line) # signalized intersection delay
    if (IntDelay): fsum.write('\t' + IntDelay[0])# signalized intersection delay
    
    IntLOS = SignalLOS_2000.findall(line) # signalized intersection LOS
    if (IntLOS): fsum.write('\t' + IntLOS[0])# signalized intersection LOS
    
    if ('Control Delay (s)' in line): fsum.write('\t' + GetWorstOne(line)) # Non-signalized Worst Movement delay
    if ('Lane LOS' in line): fsum.write('\t' + GetWorstOne(line)) # Non-signalized Worst Movement LOS
    
    HCM_2000_VC(line)
    HCM_2000_AppDelay(line)
   

        
def HCM_2010(line):   
    
    global Signalized
    
    if 'Traffic Volume (veh/h)'in line: Signalized = True
    if 'Traffic Vol, veh/h' in line: Signalized = False
    
    IntDelay = SignalDelay_2010.findall(line) # signalized intersection delay
    if (IntDelay): fsum.write('\t' + IntDelay[0])# signalized intersection delay
    
    IntLOS = SignalLOS_2010.findall(line) # signalized intersection LOS
    if (IntLOS): fsum.write('\t' + IntLOS[0])# signalized intersection LOS
    
    if ('HCM Control Delay (s)' in line): fsum.write('\t' + GetWorstOne(line)) # Non-signalized Worst Movement delay
    if ('HCM Lane LOS' in line): fsum.write('\t' + GetWorstOne(line)) #Non-signalized Worst Movement LOS
    
    HCM_2010_VC(line)
    HCM_2010_AppDelay(line)
     

if __name__ == "__main__":        
    fsum=open(Path + 'summary.txt','w')
    for file in glob.glob(Path +'*.txt'):
        with open(file,'r') as f:
            if 'summary' not in file:
                Version = '2000' if '2000' in file else '2010'
                rate = GrowRate.findall(file)[0]
                fsum.write(file + '\n')
                for line in f:
                    Node = NodeNum.findall(line) #Int Number
                    if (Node):
                        CurrentNode = Node[0]
                        fsum.write('\n' + CurrentNode + '\t' + Version + '\t' + rate + '%')
                        if 'AM' in file: fsum.write('\t' + 'AM')
                        if 'PM' in file: fsum.write('\t' + 'PM')
              
                    if  Version == '2000': HCM_2000(line)
                    if  Version == '2010': HCM_2010(line)
                       
                    print repr(line)
                fsum.write('\n')
    fsum.close()
