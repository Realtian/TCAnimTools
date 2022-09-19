import sys
import maya.cmds as mc
mc.select('pCube1')

import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as om

class MotionTrailPoint():
    def __init__(self):
        self.cameraInfo = {}
        self.objectInfo = {}
        self.keyframeList = sorted(set(mc.keyframe( mc.ls(sl=1), query=True )), key=float)
        #self.mpPoint 
        self.currentTime = []
        self.objDistance = 0
        self.mtPointDistance = True
        
    def updateCameraInfo(self):
        panel = mc.getPanel(underPointer=True)
        if panel:
            #camera = mc.modelPanel(panel, q=True, cam=True)
            camera = 'persp'
            if camera:
                self.cameraInfo['cam'] = camera
                camPosRaw = mc.xform(camera, query=True, worldSpace=True, rotatePivot=True)
                camPos = om.MVector(camPosRaw[0],camPosRaw[1],camPosRaw[2])
                self.cameraInfo['camPos'] = [camPos.x, camPos.y, camPos.z]
                print self.cameraInfo
                
    def refreshSelection(self):
        selection = mc.ls(sl=True, type='transform')
        for f in self.keyframeList:
            objPosRaw = mc.xform(selection, query=True, worldSpace=True, rotatePivot=True)
            objPos = om.MVector(objPosRaw[0],objPosRaw[1],objPosRaw[2])
            self.objectInfo[f] = [objPos.x, objPos.y, objPos.z]

    def push(self):
        self.updateCameraInfo()
        self.refreshSelection()
        for obj in self.objectInfo.keys():
            objPos = self.objectInfo[obj]
            print self.cameraInfo
            camPos = self.cameraInfo['camPos']
            objNormal = [a-b for a, b in zip(objPos, camPos)]
            objNormal = om.MVector(objNormal)
            objNormal.normalize()
            newPos = objPos + (objNormal * 0.1)
            #mc.xform(obj, translation=(newPos[0], newPos[1], newPos[2]), ws=True)

        
#create point obj
#get vector
#get world pos in relation to cam

def printVector(vector):
    print vector[0], vector[1], vector[2]

keyframeList = sorted(set(mc.keyframe( 'pCube1', query=True )), key=float)
currentFrame = mc.currentTime(q=1)
mtPointPosList = []
for i in keyframeList:
    mc.setAttr('time1.outTime', i)





    objNormal = objPos - camPos
    objNormal.normalize()
    mtPointPos = camPos + (objNormal * 1)
    mtPointPosList.append(mtPointPos)
mc.setAttr('time1.outTime', currentFrame)

for i in mtPointPosList:
    loc = mc.createNode('locator')
    locTransform = mc.listRelatives(loc, p=1)
    mc.xform(locTransform, translation=(i[0], i[1], i[2]), scale=(0.01, 0.01, 0.01), ws=True)



mc.createNode('follicle')




frameRange = [mc.playbackOptions(q=1, min=1), mc.playbackOptions(q=1, max=1)]
currentFrame = mc.currentTime(q=1)
#get camera vector frame list
#get obj vector frame list
objPosList = []
camPosList = []
for i in range(int(frameRange[0])-1, int(frameRange[1])):
    mc.setAttr('time1.outTime', i)
    camPosRaw = mc.xform('persp1', query=True, worldSpace=True, rotatePivot=True)
    camPos = om.MVector(camPosRaw[0],camPosRaw[1],camPosRaw[2])
    objPosRaw = mc.xform('pCube1', query=True, worldSpace=True, rotatePivot=True)
    objPos = om.MVector(objPosRaw[0],objPosRaw[1],objPosRaw[2])
    objPosList.append(objPos)
    camPosList.append(camPos)
mc.setAttr('time1.outTime', currentFrame)



'''
try:
    del sys.modules['SPMotionTrail']
except:
    pass
sys.path.append( '/net/homedirs/tchen/Documents' )

import SPMotionTrail
a = SPMotionTrail.MotionTrailPoint()
a.push()
'''