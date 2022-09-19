import maya.cmds as mc
import maya.mel

def frame_range(start=None, end=None):
    if not start and not end:
        gPlayBackSlider = maya.mel.eval('$temp=$gPlayBackSlider')
        if mc.timeControl(gPlayBackSlider, query=True, rangeVisible=True):
            frameRange = mc.timeControl(gPlayBackSlider, query=True, rangeArray=True)
            start = frameRange[0]
            end = frameRange[1]-1
        else:
            start = mc.playbackOptions(query=True, min=True)
            end = mc.playbackOptions(query=True, max=True)

    return start,end

def key_list(increment):
	kl = list(range(int(frame_range()[0]), int(frame_range()[1]), increment))
	return kl

def increment_bake(obj, increment):
	no_key_list = [x for x in key_list(1) if x not in key_list(2)]
	
	anim_curve_list = []
	
	anim_curve_list.append(mc.listConnections(obj, s=1, type='animCurveTU'))
	anim_curve_list.append(mc.listConnections(obj, s=1, type='animCurveTL'))
	anim_curve_list.append(mc.listConnections(obj, s=1, type='animCurveTA'))
	anim_curve_list = filter(None, anim_curve_list)
	anim_curve_list = sum(anim_curve_list, [])
	
	mc.cutKey(anim_curve_list, time=[(key,key) for key in no_key_list])

obj = mc.ls(sl=1)
increment_bake(obj, 2)