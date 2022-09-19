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
			x_diff = float(start_pos[0] - current_pos[0])/150 + .001
			y_diff = float(current_pos[1] - start_pos[1])/200 + .001
			return True
		elif event.type() == QtCore.QEvent.MouseButtonRelease and self.startPos is not None:
			self.startPos = None
			print 'stop'
			app.removeEventFilter(self)
			return True
		elif event.type() == QtCore.QEvent.KeyPress:
			print event.text()
		return super(DragEventHandler, self).eventFilter(source, event)
		
def get_QPoint_value(QPoint):
	val_str = str(QPoint).split('(',1)[1]
	x_val = int(val_str.split(',',1)[0])
	y_val = int(val_str.split(', ',1)[1][:-1])
	return x_val, y_val

handler = DragEventHandler()
app = QApplication.instance()
mc.undoInfo(openChunk=1)
app.installEventFilter(handler)