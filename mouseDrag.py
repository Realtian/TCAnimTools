import math
import maya.cmds as mc
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QApplication
import re

class DragEventHandler(QtCore.QObject):
	def __init__(self):
		super(DragEventHandler, self).__init__()
		self.startPos = None
		
	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.MouseButtonPress:
			self.startPos = event.pos()
			global start_pos
			start_pos = get_QPoint_value(self.startPos)
			print start_pos
			return True

		elif event.type() == QtCore.QEvent.MouseMove and self.startPos is not None:
			current_pos = get_QPoint_value(event.pos())
			print current_pos
			return True
		
		elif event.type() == QtCore.QEvent.MouseButtonRelease and self.startPos is not None:
			self.startPos = None
			print 'stop'
			#app.removeEventFilter(self)
			return True
		
		return super(DragEventHandler, self).eventFilter(source, event)
		
def get_QPoint_value(QPoint):
	val_str = str(QPoint).split('(',1)[1]
	x_val = int(val_str.split(',',1)[0])
	y_val = int(val_str.split(', ',1)[1][:-1])
	return x_val, y_val

def run(pressOrRelease):
	if pressOrRelease == 'press':
		#mc.undoInfo(openChunk=1)
		app.installEventFilter(handler)
		print 'pressed'
	if pressOrRelease == 'release':
		app.removeEventFilter(handler)
		print 'released'


app = QApplication.instance()
handler = DragEventHandler()

'''
import sys

try:
    del sys.modules['mouseDrag']
except:
    pass
sys.path.append( '/net/homedirs/tchen/Documents' )

import mouseDrag
'''