mxd = arcpy.mapping.MapDocument("CURRENT")
#FigNum=xrange(17,parameters[0].value+1)
FigNum={parameters[0].value}	
#FigNum={24,25,32,33,37,39}

for i in FigNum:
        lyrs = arcpy.mapping.ListLayers(mxd,r"Fig {0} -*".format(i))
        for index in xrange(1, len(lyrs)+1):
                lyr = arcpy.mapping.ListLayers(mxd,r"Fig {0} -*".format(i))[index-1]
                lyr.visible=True
        
        legend=arcpy.mapping.ListLayoutElements(mxd,"GRAPHIC_ELEMENT",r"Fig {0}*".format(i))[0]
        tempX=legend.elementPositionX
        tempY=legend.elementPositionY
        legend.elementPositionX=0.5
        legend.elementPositionY=1.15

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        arcpy.mapping.ExportToPDF(mxd, "H:\projfile\9891 - Brevard MPO General Planning\Task 26 - 2015 SOS\GIS\PDF\{0}.pdf".format(lyrs[0].name))

        legend.elementPositionX=tempX
        legend.elementPositionY=tempY

        for index in xrange(1, len(lyrs)+1):
                lyr = arcpy.mapping.ListLayers(mxd,r"Fig {0} -*".format(i))[index-1]
                lyr.visible=False

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
