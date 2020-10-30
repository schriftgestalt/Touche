# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc, time, traceback
from GlyphsApp import *
from GlyphsApp.plugins import *
from toucheTool import ToucheTool

class TouchePlugin (GeneralPlugin):
	def settings(self):
		self.name = u"Touché"
	
	def start(self):
		try: 
			newMenuItem = NSMenuItem(self.name, self.showWindow)
			Glyphs.menu[EDIT_MENU].append(newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow, signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)
	
	def showWindow(self, sender):
		self.touche = ToucheTool()
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	