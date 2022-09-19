import maya.cmds as mc
import maya.OpenMaya as om

def push(cam, obj, multiplier):
    camPosRaw = mc.xform(cam, query=True, worldSpace=True, rotatePivot=True)
    camPos = om.MVector(camPosRaw[0],camPosRaw[1],camPosRaw[2])
    objPosRaw = mc.xform(obj[0], query=True, worldSpace=True, rotatePivot=True)
    objPos = om.MVector(objPosRaw[0],objPosRaw[1],objPosRaw[2])
    distanceToObj = objPos - camPos
    distanceToObjRaw = objPos - camPos
    if abs(distanceToObjRaw[0]) > 1:
        distanceToObj.normalize()
        newPos = objPos + (distanceToObj * multiplier)
        mc.xform(obj, worldSpace=True, translation=(newPos[0], newPos[1], newPos[2]))
    else:
        newPos = objPos + (distanceToObj * (multiplier+1))
        mc.xform(obj, worldSpace=True, translation=(newPos[0], newPos[1], newPos[2]))

def actualPush(slider, cam, speed, *args):
    obj = mc.ls(sl=1)
    value = mc.intSlider(slider, q=True, value=True)
    if len(obj)>1:
        mc.error('Only select 1 object')
    elif len(obj)==0:
        mc.error('Select object to push/pull')
    else:
        push(cam, obj, float(value)/100.00*(speed/50.00))

    

def getSpeedFactor(slider):
    global speed_factor
    speed_factor = mc.intSlider(slider, q=True, value=True)
    return speed_factor


def pushPullUI():
    winName = 'pushPullWin'
   
    curCamera = mc.modelEditor(mc.getPanel(type="modelPanel")[0], q=1, av=1, cam=1)
   
    if mc.window(winName, exists=True):
        mc.deleteUI(winName)

    mc.window(winName, title='push pull', iconName='push pull', width=300, height=60)

    mc.rowColumnLayout( numberOfRows=4,
                  columnAttach=[(1, 'left', 5),
                                (2, 'left', 0),
                                (3, 'left', 0),
                                (3, 'left', 0)])

    
    mc.text('   pull<<<                             move                          >>>push')
    slider = mc.intSlider(min=-100, max=100, value=0, step=1, w=290)
    mc.intSlider(slider, w=290, e=True, dc=lambda x: actualPush(slider, curCamera, speed_factor))

    mc.text(' slow<<<                             speed                          >>>fast')
    sliderSpeed = mc.intSlider(min=1, max=200, value=100, step=1, w=290)
    mc.intSlider(sliderSpeed, w=290, e=True, dc=lambda x: getSpeedFactor(sliderSpeed))    

    mc.showWindow(winName)

    mc.window(winName, edit=True, width=300, height=60)

pushPullUI()