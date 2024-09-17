# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from Cocoa import NSMenuItem
from GlyphsApp import Glyphs, EDIT_MENU
from GlyphsApp.plugins import GeneralPlugin
from toucheTool import ToucheTool


class TouchePlugin (GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = "Touché"

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		if not newMenuItem.target():
			newMenuItem.setTarget_(self)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		self.touche = ToucheTool()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
