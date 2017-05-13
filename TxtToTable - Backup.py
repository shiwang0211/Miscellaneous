import glob
import re

NodeNum = re.compile(r'([0-9]+): ')
SignalDelay_2010 = re.compile(r'HCM 2010 Ctrl Delay   				([0-9]+.[0-9])') # Intersection Delay
SignalLOS_2010 = re.compile(r'HCM 2010 LOS          				([A-Z])') # Intersection LOS
SignalDelay_2000 = re.compile(r'HCM 2000 Control Delay				([0-9]+.[0-9])') # Intersection Delay
SignalLOS_2000 = re.compile(r'HCM 2000 Level of Service					([A-Z])') # Intersection LOS

AppDelay_2010 = re.compile(r'Approach Delay, s/veh (.+)') # Signalized Int App Delay
AppLOS_2010 = re.compile(r'Approach LOS          (.+)') # Signalized Int App LOS
AppDelay_2000 = re.compile(r'Approach Delay \(s\)    (.+)') # Signalized Int App Delay
AppLOS_2000 = re.compile(r'Approach LOS          	(.+)') # Signalized Int App LOS

VC_2010 = re.compile(r'V/C Ratio\(X\)          (.+)')  # Signalized Int Movement VC
Vol_2010 = re.compile(r'Adj Flow Rate, veh/h  (.+)') # Signalized Int Movement Vol
Cap_2010 = re.compile(r'Lane Grp Cap\(c\), veh/h(.+)') # Signalized Int Movement Cap
VC_2000 = re.compile(r'v/c Ratio             	(.+)') # Signalized Int Movement VC
Vol_2000 = re.compile(r'Adj[.] Flow \(vph\)       (.+)') # Signalized Int Movement Vol
Cap_2000 = re.compile(r'Lane Grp Cap \(vph\)    (.+)') # Signalized Int Movement Cap

Path = 'C:\\Users\\swang\\Desktop\\I-4 IAP Synchro Outputs\\'
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
    
def HCM_Read(line, parameter, version):
    
    global Signalized
    func = parameter + "_" + version + ".findall(line)"
    Nums = eval(func)

    if(Nums and Signalized):  # Signalized Adjusted Volumes/Capacity/VC for 12 movements
        Nums=Nums[0].split('\t')
        while len(Nums) > 12:
            Nums.pop(0)
        for i in xrange(12): fsum.write('\t' + Nums[i])
    if (not Signalized and version == "2000" and 'Direction, Lane #' in line) or (not Signalized and version =="2010" and 'Minor Lane/Major Mvmt' in line):
        for i in xrange(12): fsum.write('\t' + '') # Non-signalized, placeholder only once
        
def HCM_2000_App(line, parameter):
    
    global Signalized
    
    if(parameter == "Delay"): Nums=AppDelay_2000.findall(line)# Approach Delay
    if(parameter == "LOS"): Nums=AppLOS_2000.findall(line)# Approach LOS
    
    if(Nums and Signalized):# Signalized Approach delay, four approaches
        Num = Nums[0].replace('\t\n','').split('\t\t')
        Num = [temp.replace('\t','') for temp in Num]
        if Num[0]=='' : Num.pop(0)
        if Num[0]=='' : Num.pop(0)
        if len(Num)>3: fsum.write('\t' + Num[0] + '\t' + Num[1] + '\t' + Num[2] +  '\t' + Num[3])
    if(not Signalized and 'Direction, Lane #' in line):# Non-signalized, placeholder only once
        fsum.write('\t' + '' + '\t' + '' + '\t' + '' +  '\t' + '')          

def HCM_2010_App(line, parameter): 
    
    global Signalized     
    
    if(parameter == "Delay"): Nums=AppDelay_2010.findall(line) # Approach Delay
    if(parameter == "LOS"): Nums=AppLOS_2010.findall(line)# Approach LOS
    
    if(Nums and Signalized): # Signalized Approach delay, four approaches
        Num = Nums[0].split('\t')
        Num.pop(0)
        Num.pop(0)
        fsum.write('\t' + Num[1] + '\t' + Num[4] + '\t' + Num[7] +  '\t' + (Num[10] if Num[10]!= '' else Num[9])) # Temporary Fix....
    if(not Signalized and 'Minor Lane/Major Mvmt' in line):# Non-signalized, placeholder only once
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
    
    #HCM_Read(line, "VC", "2000")
    HCM_Read(line, "Vol", "2000")
    HCM_Read(line, "Cap", "2000")
    HCM_2000_App(line, "Delay")
    HCM_2000_App(line, "LOS")

        
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
    
    #HCM_Read(line, "VC", "2010")
    HCM_Read(line, "Vol", "2010")
    HCM_Read(line, "Cap", "2010")
    HCM_2010_App(line,"Delay")
    HCM_2010_App(line,"LOS")
     

if __name__ == "__main__":      
    fsum=open(Path + 'summary.txt','w')
    for file in glob.glob(Path +'*.txt'):
        with open(file,'r') as f:
            if 'summary' not in file:
                Version = '2000' if '2000' in file else '2010'
                #rate = GrowRate.findall(file)[0]
                fsum.write(file + '\n')
                for line in f:
                    Node = NodeNum.findall(line) #Int Number
                    if (Node):
                        CurrentNode = Node[0]
                        fsum.write('\n' + CurrentNode + '\t' + Version)
                        if 'AM' in file: fsum.write('\t' + 'AM')
                        if 'PM' in file: fsum.write('\t' + 'PM')
              
                    if  Version == '2000': HCM_2000(line)
                    if  Version == '2010': HCM_2010(line)
                       
                    print repr(line)
                fsum.write('\n')
    fsum.close()
