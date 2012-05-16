#! /usr/bin/env python

from gi.repository import Gtk, GObject
import os
import sys

UI_FILE = "splash.ui"

class Splash(GObject.GObject):
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		
		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		#self.window.set_auto_startup_notification("FALSE")
		#self.window.connect("destroy", self.destroy)
		self.window.set_default_size(500,300)
		self.window.show_all()
		self.count = 1
		self.countdown()

	def destroy(self, window):
		Gtk.main_quit()

	def countdown(self):
		self.count = self.count + 1
		GObject.timeout_add(1000, self.countdown)
		#print "here"
		if self.count == 10:
			print "test"
			self.window.destroy()

def main():
	app = Splash()
	Gtk.main()
	
if __name__ == "__main__":
	main()

