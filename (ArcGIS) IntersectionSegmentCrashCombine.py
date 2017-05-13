for fid in xrange(0,235):
    arcpy.SelectLayerByAttribute_management('S4_SOS_Intersections_083016',"NEW_SELECTION",r'"FID" = {0}'.format(fid))
    arcpy.SelectLayerByLocation_management('2015_SOS_Network Gray','intersect','S4_SOS_Intersections_083016',0.05)
    matchcount = int(arcpy.GetCount_management('2015_SOS_Network Gray')[0])

    if (matchcount == 0):
        continue

    cursor = arcpy.UpdateCursor('S4_SOS_Intersections_083016')
    for row in cursor:
            row.setValue("NoSegMat", matchcount)
            cursor.updateRow(row)

    del cursor

    cursor = arcpy.da.SearchCursor('S4_SOS_Intersections_083016',['FID','AllCrash'])
    for row in cursor:
        if (row[0] == fid):
            IntCrash = row[1]

    del cursor

    SegCrash = IntCrash / matchcount
    
    cursor = arcpy.UpdateCursor('2015_SOS_Network Gray')
    for row in cursor:
            row.setValue("IntTotCras", SegCrash)
            cursor.updateRow(row)

    del cursor
