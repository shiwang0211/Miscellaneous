import csv

Legs_dict = {'E': 5, 'N': 1, 'S': 9, 'W': 13, 'NE': 3, 'NW': 15, 'SE': 7, 'SW': 11}
Orientation_dict = {'Default': ['S','N','E','W']}
ReplaceAll = 1
KeepAll = 0

# Read valid orientations for each node from csv -----


with open('NodeOrientations.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        temp=[]
        for index in xrange(5):
            if (row[str(index+1)] != ''): temp.append(row[str(index+1)])
            Orientation_dict[row['Node Number']] = temp

    
# Read Lane Turns from csv -----

with open('Timing Template.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        # Read numbers from csv -----
        SC = int(row['Node'])
        Node = int(row['Node'])
        Yellow = float(row['Yellow'])
        Red = float(row['Red'])
        Cycle = int(row['Cycletime'])

        Splits = []
        MinGreens = []
        LaneTurns_1 = []
        LaneTurns_2 = []
        GT_Starts =[]
        GT_Ends =[]
        U_Turns =[]
        
        for index in xrange(8):
            Splits.append(int(row['p'+str(index + 1)+'_Split']))
            MinGreens.append(int(row['p'+str(index + 1)+'_minGreen']))
            LaneTurns_1.append(row['p'+str(index + 1)+'_laneturn1'])
            LaneTurns_2.append(row['p'+str(index + 1)+'_laneturn2'])
            U_Turns.append(row['p'+str(index + 1)+'_Uturn'])
            
        for index in xrange(8):
            tmp = 0 if index <4 else 4
            GT_Starts.append( sum(Splits[tmp:index]) )
            GT_Ends.append( sum(Splits[tmp:(index+1)]) )
        
            
        # VISUM CODES -----        
        try:
            Visum.Net.AddSignalControl(SC)
            
        except:
            if(KeepAll == 1): 
                continue 
            
            if(ReplaceAll == 1):
                SignalController = Visum.Net.SignalControls.ItemByKey(SC) 
                Visum.Net.RemoveSignalControl(SignalController)
                Visum.Net.AddSignalControl(SC)

        SignalController = Visum.Net.SignalControls.ItemByKey(SC) 
        SignalController.AllocateNode(Node)
        SignalController.SetAttValue("Cycletime",Cycle)
        
        for index in xrange(8):
            
            # Set timing parameters ----
            Visum.Net.AddSignalGroup(index + 1, SC)
            SignalGroup = Visum.Net.SignalControls.ItemByKey(SC).SignalGroups.ItemByKey(SC, index + 1)
            SignalGroup.SetAttValue("Amber",Yellow)
            SignalGroup.SetAttValue("Allred",Red)
            SignalGroup.SetAttValue("GtStart",GT_Starts[index])
            SignalGroup.SetAttValue("GtEnd",GT_Ends[index])
            SignalGroup.SetAttValue("MinGreenTime",MinGreens[index])
            
            # Assign Turns for each ILane in ILeg and each OLane in OLeg----
            
            for LaneTurns in [LaneTurns_1, LaneTurns_2]:
                
                # if "all" is selected, match the FromLeg to all possible ToLegs
                LaneTurns_v2 = []
                if 'all' in LaneTurns[index]:
                    FromLeg = LaneTurns[index].split(' ')[0]
                    ToLegs = [leg for leg in Orientation_dict[str(Node)]]# if leg != FromLeg]
                    for ToLeg in ToLegs: LaneTurns_v2.append(FromLeg + '-' + ToLeg)                                
                
                elif LaneTurns[index] != 'NA' and U_Turns[index] == '1':
                    FromLeg = LaneTurns[index].split('-')[0]
                    LaneTurns_v2.append(LaneTurns[index])
                    LaneTurns_v2.append(FromLeg + "-" + FromLeg)
                    
                elif LaneTurns[index] != 'NA'and U_Turns[index] == '0':
                    LaneTurns_v2.append(LaneTurns[index])
                    
                else:
                    LaneTurns_v2=[]
                
                # Assign signal group to lane turn    
                for LaneTurn in LaneTurns_v2:
                    IOLegs = LaneTurn.split('-')
                    ILeg = Legs_dict[IOLegs[0]]
                    OLeg = Legs_dict[IOLegs[1]]
                
                    ILeg = Visum.Net.Legs(True).ItemByKey(Node,0,ILeg)
                    ILanes = ILeg.Lanes(True,False).GetAll
                    
                    OLeg = Visum.Net.Legs(True).ItemByKey(Node,0,OLeg)
                    OLanes = OLeg.Lanes(False,True).GetAll
                    
                    for ILane in ILanes:
                        for OLane in OLanes:
                            if(Visum.Net.LaneTurns(True).LaneTurnExistsByLanes(ILane, OLane) == True):
                                LT = Visum.Net.LaneTurns(True).ItemByLanes(ILane, OLane)
                                SignalGroup.AllocateLaneTurn(LT)
