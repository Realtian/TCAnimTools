import math
import maya.cmds as mc
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QApplication
import re

def get_sel_data():

    #get graph editor selection
    curve_obj = mc.keyframe(q=1, name=1)

    #save all selected data
    index_list = mc.keyframe(q=1, indexValue=1)
    keys_data = []
    for i in index_list:
        data = mc.keyframe(curve_obj, 
                           q=1, 
                           index=(i, i), 
                           indexValue=1, 
                           timeChange=1, 
                           valueChange=1)
        keys_data.append(data)

    #get cap frames data
    cap_start_index = int(index_list[0]-1)
    cap_end_index = int(index_list[-1]+1)
    start_frame = mc.keyframe(curve_obj, 
        q=1, 
        index=(cap_start_index, cap_start_index), 
        indexValue=1, 
        timeChange=1, 
        valueChange=1)
    end_frame = mc.keyframe(curve_obj, 
        q=1, 
        index=(cap_end_index, cap_end_index), 
        indexValue=1, 
        timeChange=1, 
        valueChange=1)
    cap_keys_data = [start_frame, end_frame]

    keys_data.insert(0, start_frame)
    keys_data.insert(len(keys_data), end_frame)

    #get arctan shift factor
    #get arctan ease factor

    return keys_data, curve_obj

class EaseTween():
    
    def __init__(self, ease_factor, shift_factor):
        #data variable format: index, frame#, value
        self.keys_data              = get_sel_data()[0]
        self.selected_keys_data     = get_sel_data()[0][1:-1]
        self.start_frame_num        = self.keys_data[0][1]
        self.end_frame_num          = self.keys_data[-1][1]
        self.start_frame_val        = self.keys_data[0][2]
        self.end_frame_val          = self.keys_data[-1][2]
        self.ease_factor            = ease_factor
        self.shift_factor           = shift_factor
        self.curve_obj                    = get_sel_data()[1]

    def interpolate(self, val_list):
        interpolated_list = []
        #print val_list
        for i in val_list:
            new_val = ((i - val_list[0]) /
                       (val_list[-1] - val_list[0]) *
                       (self.end_frame_val - self.start_frame_val) +
                       self.start_frame_val)
            interpolated_list.append(new_val)
        return interpolated_list

    def get_arctan_factor_list(self):
        symmetry_frame_range = [i-((int(self.end_frame_num - self.start_frame_num)+1)/2) for i in range(0, int(self.end_frame_num - self.start_frame_num)+1)]
        arctan_factor = [math.atan(float((i + self.shift_factor) * self.ease_factor)) for i in symmetry_frame_range]
        arctan_index_list = [int(i[1])-int(self.keys_data[0][1]) for i in self.keys_data]
        arctan_factor = [arctan_factor[i] for i in arctan_index_list]
        return arctan_factor

    def apply_new_values(self):
        #interpolate factored value list
        arctan_factor_list = self.get_arctan_factor_list()
        avg_value = (self.start_frame_val + self.end_frame_val)/2
        arctan_value_list = [(avg_value + f) for f in arctan_factor_list]
        interpolated_arctan_value_list = self.interpolate(arctan_value_list)
        #apply new value list
        for i, v in zip(self.selected_keys_data, interpolated_arctan_value_list[1:-1]):
            mc.keyframe(self.curve_obj, index = (i[0], i[0]), valueChange = v)

def get_QPoint_value(QPoint):
    val_str = str(QPoint).split('(',1)[1]
    x_val = int(val_str.split(',',1)[0])
    y_val = int(val_str.split(', ',1)[1][:-1])
    return x_val, y_val

class DragEventHandler(QtCore.QObject):
    def __init__(self):
        super(DragEventHandler, self).__init__()
        self.startPos = None
        
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.startPos = event.pos()
            global start_pos
            start_pos = get_QPoint_value(self.startPos)
            #print start_pos
            return True
        elif event.type() == QtCore.QEvent.MouseMove and self.startPos is not None:
            current_pos = get_QPoint_value(event.pos())
            print current_pos
            x_diff = float(start_pos[0] - current_pos[0])/150 + .001
            y_diff = float(current_pos[1] - start_pos[1])/200 + .001
            #print x_diff, y_diff
            a = EaseTween(y_diff, x_diff)
            a.apply_new_values()
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease and self.startPos is not None:
            self.startPos = None
            print 'stop'
            app.removeEventFilter(self)
            mc.undoInfo(closeChunk=1)
            return True
        elif event.type() == QtCore.QEvent.KeyPress:
            print event.text()
        return super(DragEventHandler, self).eventFilter(source, event)
        

handler = DragEventHandler()
app = QApplication.instance()
mc.undoInfo(openChunk=1)
app.installEventFilter(handler)

'''

import sys

try:
    del sys.modules['EaseTween']
except:
    pass
sys.path.append( 'D:/Files/coding' )

import EaseTween



'''
