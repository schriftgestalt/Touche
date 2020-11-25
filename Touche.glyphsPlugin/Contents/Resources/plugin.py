# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc, time, traceback
from GlyphsApp import *
from GlyphsApp.plugins import *
from toucheTool import ToucheTool

class TouchePlugin (GeneralPlugin):
	def settings(self):
		self.name = "Touché"
	
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)
	
	def showWindow_(self, sender):
		self.touche = ToucheTool()
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	