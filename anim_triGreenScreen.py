# key out green screen in ref
# make sure the file names have frame extensions something like imagename.001.jpg 
# chroma key color is automatically detected but if it's not accurate you can also 
# go into the stencil node to change the color
# the image plane is created at the origin
# there are attributes on the image plane geo to retime the reference and to fine
# tune the chroma key
# tags: imageplane, reference, animtool
# icon: :/anim_greenScreen.png
# iconLabel: greenScreen

import maya.cmds as mc
import maya.OpenMaya as om
import sys
import os
from PIL import Image

def nameGen(stringOrList, suffix=False):

    # If stringOrList is a string
    if isinstance(stringOrList, str):
        result = stringOrList.split('.')[0]

    # If stringOrList is not a string
    else:
        newObj = ""
        underscore = ""
        for o in stringOrList:
            newObj += underscore + o.split('.')[0]
            underscore = '_'
        result = newObj

    if suffix:
        suffix = '_' + suffix.split('.')[0]
    else:
        suffix = ""
    name = "{}{}".format(result, suffix)
    num = 0
    while mc.objExists(name):
        num += 1
        name = "{}{}{}".format(result, suffix, num)

    return name

def addMeshPlane(filepath, refGrp, rgb):
    r = float(rgb[0])/255
    g = float(rgb[1])/255
    b = float(rgb[2])/255
    # Create File Node
    fileNode = mc.createNode('file', name='file')
    mc.setAttr(fileNode + '.fileTextureName', filepath, type="string")
    mc.setAttr(fileNode + '.useFrameExtension', 1)
    X = mc.getAttr(fileNode + '.outSizeX')
    Y = mc.getAttr(fileNode + '.outSizeY')
    # Create Poly Plane
    # name = filepath.split('.0')[0].split('/')[-1]
    width = 10
    height = (float(Y)/float(X))*width
    plane, planeShape = mc.polyPlane(name=nameGen('ReferencePlane'), w=width, h=height ,sx=1, sy=1)
    mc.setAttr(plane + '.rotateX', 90)
    mc.makeIdentity(plane, apply=True)
    mc.delete(plane, ch=True)
    mc.parent(plane, refGrp, r=True)
    mc.setAttr(plane + '.visibility', k=False, channelBox=True)
    
    # Add frame attribute to plane
    mc.addAttr(plane, longName='frame', at='float', k=True)
    mc.connectAttr(plane + '.frame', fileNode + '.frameExtension')
    minFrame = mc.playbackOptions(minTime=True, q=True)
    maxFrame = mc.playbackOptions(maxTime=True, q=True)
    mc.setKeyframe(plane, attribute='frame', v=1, t=minFrame)
    mc.setKeyframe(plane, attribute='frame', v=maxFrame-minFrame+1, t=maxFrame)
    mc.keyTangent(plane, inTangentType='linear', outTangentType='linear')
    mc.setInfinity(plane, pri='linear', poi='linear')

    # Create Surface Shader
    shader = mc.createNode('surfaceShader', name=nameGen('surfaceShader'))
    mc.select(plane, r=True)
    mc.hyperShade(plane, assign=shader)
    mc.connectAttr(fileNode + '.outColor', shader + '.outColor')
    
    # Create stencil node
    stencil = mc.createNode('stencil')
    mc.connectAttr(fileNode + '.outColor', stencil + '.image')
    mc.setAttr(stencil + '.colorKey', r, g, b, type='double3')
    mc.setAttr(stencil + '.hueRange', 1)
    mc.setAttr(stencil + '.saturationRange', .1)
    mc.setAttr(stencil + '.valueRange', .1)
    mc.setAttr(stencil + '.threshold', .1)
    mc.setAttr(stencil + '.keyMasking', 1)
    mc.connectAttr(stencil + '.outAlpha', shader + '.outTransparencyR')
    mc.connectAttr(stencil + '.outAlpha', shader + '.outTransparencyG')
    mc.connectAttr(stencil + '.outAlpha', shader + '.outTransparencyB')

    # Add range attribute
    mc.addAttr(plane, longName='range', minValue=0, maxValue=1, at='float', k=False)
    mc.setAttr(plane + '.range', channelBox=True)
    # mc.connectAttr(plane + '.range', stencil + '.hueRange')
    mc.connectAttr(plane + '.range', stencil + '.saturationRange')
    mc.connectAttr(plane + '.range', stencil + '.valueRange')
    mc.setAttr(plane + '.range', .1)

    mc.select(plane)

def run(startingDirectory=None):
    if not startingDirectory:
        startingDirectory = os.path.expanduser('~')
    filepath = mc.fileDialog2(fileMode=1, caption='Choose Image Sequence', startingDirectory=startingDirectory)
    
    if not filepath:
        return
    filepath = filepath[0]
    
    rgb = get_dominant_color(filepath)
    
    if '.0' not in filepath:
        om.MGlobal.displayWarning('Chosen file does not contain frame extension. Needs "filename.0001.filetype" naming convention.')
        return

    refGrp = 'videoReference_GRP'
    if mc.objExists(refGrp) == False:
        refGrp = mc.group(name='videoReference_GRP', em=True)

    addMeshPlane(filepath, refGrp, rgb)

def get_dominant_color(img_path):
    
    original = Image.open(img_path)
    reduced = original.convert("P", palette=Image.WEB)
    palette = reduced.getpalette()
    palette = [palette[3*n:3*n+3] for n in range(256)]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    dominant_color = max([sublist for sublist in color_count])
    
    return dominant_color[1]

