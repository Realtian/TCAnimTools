from pymel import core

fps_dict = {"game": 15.0,
            "film": 24.0,
            "pal": 25.0,
            "ntsc": 30.0,
            "show": 48.0,
            "palf": 50.0,
            "ntscf": 60.0}

cam_dict = {"cam_animShape1": -10.0,
            "cam_animShape2": 40.0,
            "cam_anim": 70.0,
            "cam_animShape3": 120.0}

start_frame = core.getAttr('time1.outTime')
frame_range = [core.playbackOptions(q=1, min=1), core.playbackOptions(q=1, max=1)]
fps = fps_dict[core.currentUnit(q=1, t=1)]

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key
    return "key doesn't exist"

def get_sections(dict):
    markers = list(dict.values())
    markers = sorted([int(x) for x in markers])
    sections = []
    for i in markers:
        try:
            sections.append(( i, markers[markers.index(i)+1]-1 ))
        except:
            sections.append(( i, int(frame_range[1]) ))
    return sections, markers


def play_seq():
    try:
        core.timer(e=1)
    except:
        pass
    core.currentTime(int(frame_range[0]))
    core.timer(s=1)
    #core.play(state=1)
    while core.timer(lap=1)*int(fps) <= int(frame_range[1]):
        current_frame = core.currentTime(int(core.timer(lap=1)*int(fps)), e=True)
        sections = get_sections(cam_dict)
        for i, o in zip(sections[0], sections[1]):
            if i[0] <= int(current_frame) <= i[1]:
                core.lookThru(get_key(o, cam_dict))
            else:
                pass

    core.timer(e=1)
           
core.nameCommand( 'playCamSeq', ann='play camera sequence', c='python("play_seq()");' )
core.hotkey(k="/",n='playCamSeq')











def queryInputs(*args):
    #args0 = label01
    print(cmds.text(args[0], q=True, label = 1))
    #args[1] = int_01
    print(cmds.textField(args[1], q=True, v = 1))
    #args[2] = cb_01
    print(cmds.checkBox(args[2], q=True, v = 1))
    
def addInputs(*args):
    cmds.button( label = 'get selected camera', align = 'left' )
    cmds.textField()
    cmds.checkBox (label='Y/N')    


def runGrid():
    if cmds.window('camSeqWindow', ex=True):
        cmds.deleteUI('camSeqWindow', window=True)

    cmds.window('camSeqWindow', title='camera sequence', sizeable=False, resizeToFitChildren=True)

    cmds.rowColumnLayout( numberOfColumns = 4, columnWidth = [ (1, 150), (2, 100), (3, 75)])  
    
    button_01 = cmds.button( label = 'get selected camera', align = 'left' )
    #label_01 = cmds.text( label = 'number of sections wide:', align = 'left')
    
    int_01 = buildingWidth = cmds.textField()

    cb_01 = numberOfFloors = cmds.checkBox (label='Y/N')    

    cmds.button( label = 'Add', command = addInputs )

    cmds.button( label = 'Apply', command = partial(queryInputs, button_01, int_01, cb_01) )

    cmds.button( label = 'Cancel', command = 'cmds.deleteUI("camSeqWindow", window=True)')

    cmds.showWindow()

runGrid()






def cam_seq_window():
    
    if cmds.window('camSeqWindow', ex=True):
        cmds.deleteUI('camSeqWindow', window=True)
        
    window = cmds.window(title='camSeqWindow')
    column = cmds.columnLayout()

    def add_row(cameraname) :
        cmds.setParent(column)
        this_row = cmds.rowLayout(nc=4, cw4 = (72, 72, 72, 72) )
        cmds.text(l= cameraname )
        cmds.text(l=u'Start Frame')
        start = cmds.intField()

        def do_render(_):
            startframe = cmds.intField(start, q=True, v=True)
            print "rendering ", cameraname, "frames", startframe

    for cam in cmds.ls(sl=1):
        add_row(cam)


    cmds.showWindow(window)


cam_seq_window()
