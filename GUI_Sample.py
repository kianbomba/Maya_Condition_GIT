import maya.cmds as cmds
import maya.mel as mel
import re
def renameHP():
    for s in cmds.ls(sl = True, l = True):
        if 'HP_' not in s:
            cmds.rename(s, 'HP_' + s.split('|')[-1])
def renameLP():
    for s in cmds.ls(sl = True, l = True):
        if 'LP_' not in s:
            cmds.rename(s, 'LP_' + s.split('|')[-1])

def removePrefix():
    for s in cmds.ls(sl = True,):
  
        if 'HP_'  in s:
            mel.eval('searchReplaceNames "HP_" " ""selected";')
        if 'LP_'  in s:
            mel.eval('searchReplaceNames "LP_" " ""selected";')
       

def bakesSource():
    obj = cmds.ls(sl = True)[0:]
    get = len(obj)
    get += int(get)
    if get == 0 :
        pass
    
    cmds.select( obj, r=True )
    highSel = cmds.ls( "HP_*", sl =True )
    cmds.duplicate( highSel , un = True, n = 'highBakes_')
    mel.eval('CreatePolyFromPreview;')
    cmds.select( obj, r=True )
    lowSel = cmds.ls( "LP_*", sl =True )
    cmds.duplicate( lowSel , un = True, n = 'lowBakes_')
    
    selLow = cmds.ls('lowBakes_*',g=True)[0:]
    if int(len(selLow)) > 1:  
        cmds.select(  'lowBakes_*', r=True ) 
        mel.eval('polyPerformAction polyUnite o 0;BakeAllNonDefHistory;')
        cmds.select(  'lowBakes_*', r=True )
        cmds.rename( "lowBakes_")
        cmds.select(cl=True)
    
    selHigh = cmds.ls('highBakes_*',g =True )
    if int(len(selHigh)) > 1:
        cmds.select(  'highBakes_*', r=True )
        mel.eval('polyPerformAction polyUnite o 0;BakeAllNonDefHistory;') 
        cmds.select(  'highBakes_*', r=True )
        cmds.rename( "highBakes_")   
    
    return
    
      
def exportSceneBake():   
    obj = cmds.ls(sl = True)[0:]
    get = len(obj)
    get += int(get)
    if get == 0 :
        pass
    else:      
        setObj = cmds.sets(n="setTemp")
        cmds.select (cl=True)
    #Duplicate High
    cmds.select( "setTemp", r=True ) 
    highSel = cmds.ls( "HP_*", sl =True ) 
    cmds.duplicate( highSel , un = True, n = 'highTemp_') 
    #Duplicate Low
    cmds.select( "setTemp", r=True )   
    lowSel = cmds.ls( "LP_*", sl =True ) 
    cmds.duplicate( lowSel , un = True, n = 'lowTemp_') 
    #export Select Low
    cmds.select('lowTemp_*') 
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExportSmoothMesh -v true')
    mel.eval('FBXExport -file "C:/TempFBX/_low.fbx" -s ;')
    #export Select High
    cmds.select('highTemp_*')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExportSmoothMesh -v false')
    mel.eval('FBXExport -file "C:/TempFBX/_high.fbx" -s ;')
    #Delete Scene Bake
    cmds.select("lowTemp_*","highTemp_*", r = True)
    cmds.Delete()
    cmds.select ( 'setTemp', r=True, ne =True, )
    cmds.Delete() 
    cmds.select( obj, r=True )
  
          

def surBake():
    bakesSource()
    mel.eval('surfaceSampler -target lowBakes_ -uvSet map1 -searchOffset 0.08660254038 -maxSearchDistance 0.08660254038 -searchCage "" -source highBakes_ -mapOutput normal -mapWidth 2048 -mapHeight 2048 -max 1 -mapSpace tangent -mapMaterials 0 -shadows 1 -filename "C:/tempMaps/_Maya_normals" -fileFormat "png" -mapOutput alpha -mapWidth 2048 -mapHeight 2048 -max 1 -mapSpace tangent -mapMaterials 1 -shadows 1 -filename "C:/tempMaps/_Maya_normals" -fileFormat "png" -superSampling 2 -filterType 0 -filterSize 3 -overscan 0 -searchMethod 0 -useGeometryNormals 0 -ignoreMirroredFaces 1 -flipU 0 -flipV 0  ;')
    cmds.select(   'highBakes_','lowBakes_', r = True) 
    cmds.Delete()
    

        
def geoBake():
     bakesSource()
     mel.eval('surfaceSampler -target lowBakes_ -uvSet map1 -searchOffset 0.001732050808 -maxSearchDistance 0 -searchCage "" -source highBakes_ -mapOutput normal -mapWidth 2048 -mapHeight 2048 -max 1 -mapSpace tangent -mapMaterials 0 -shadows 1 -filename "C:/tempMaps/_Maya_normals" -fileFormat "png" -mapOutput alpha -mapWidth 2048 -mapHeight 2048 -max 1 -mapSpace tangent -mapMaterials 1 -shadows 1 -filename "C:/tempMaps/_Maya_normals" -fileFormat "png" -superSampling 2 -filterType 0 -filterSize 3 -overscan 4 -searchMethod 0 -useGeometryNormals 1 -ignoreMirroredFaces 1 -flipU 0 -flipV 0;')    
     cmds.select('highBakes_','lowBakes_', r = True) 
     cmds.Delete()
     
 

def GUI():
    if (cmds.window("mainWindow", exists = True)):
	cmds.deleteUI("mainWindow", wnd=True)
	cmds.windowPref("mainWindow", r=True) 
    cmds.window("mainWindow", s=True, tlb=True, rtf=True, mxb=True,t="TL Uvs Tools", width = 188, height = 20)
    cmds.frameLayout ("frameTools", label = "Map2048",  collapsable  = True, bgc = (.3,.3,.3), parent = "mainWindow")
    
    cmds.gridLayout("gridLayout07", numberOfRowsColumns = (1,3), cellWidthHeight = (64,25), parent = "frameTools")
    cmds.button(label = "rename HP_", c = "renameHP()", bgc=(0.2, 0.2, 0.2), parent = "gridLayout07")
    cmds.button(label = "rename LP_", 	c = "renameLP()", bgc=(0.2, 0.2, 0.2), parent = "gridLayout07")
    cmds.button(label = "Remove", 	c = "removeSufix()", bgc=(1, 0.000, 0.000), parent = "gridLayout07")

    cmds.gridLayout("gridLayout08", numberOfRowsColumns = (1,2), cellWidthHeight = (96,40), parent = "frameTools")
    cmds.button(label = "Bake Geometry", c = "geoBake()", bgc=(0 , 0.2, 0.5), parent = "gridLayout08")
    cmds.button(label = "Bake Surface", 	c = "surBake()", bgc=(0 , 0.2, 0.5), parent = "gridLayout08")

    cmds.setParent( '..' )
    cmds.columnLayout( "columnName01", adjustableColumn = True, parent = "frameTools")
    cmds.button (label = "Export Marmoset", command = "exportSceneBake()", bgc=(0.000, 0.545, 0.545), parent = "columnName01")

    cmds.showWindow()

GUI()    






