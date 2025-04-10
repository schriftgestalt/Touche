# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from GlyphsApp import Glyphs, EDIT_MENU, NSMenuItem
from GlyphsApp.plugins import GeneralPlugin
from toucheTool import ToucheTool


class TouchePlugin (GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = "Touché"

	@objc.python_method
	def start(self):
		if Glyphs.buildNumber >= 3320:
			from GlyphsApp.UI import MenuItem
			newMenuItem = MenuItem(self.name, action=self.showWindow_, target=self)
		else:
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, self.showWindow_, "")
			newMenuItem.setTarget_(self)

		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		self.touche = ToucheTool()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
