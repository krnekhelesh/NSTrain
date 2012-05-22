#! /usr/bin/env python

from gi.repository import Gtk, GObject
import os
import sys

UI_FILE = "data/ui/splash.ui"

class Splash(GObject.GObject):
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.logo = self.builder.get_object('image1')
		self.logo.set_from_file('./data/media/app-icon.png')

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.set_default_size(500,200)
		self.window.set_keep_above("false")
		#self.show_splash()

	def show_splash(self):
		self.window.show_all()

	def hide_splash(self):
		self.window.hide()

