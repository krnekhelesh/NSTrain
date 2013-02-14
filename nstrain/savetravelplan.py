#! /usr/bin/env python

from gi.repository import Gtk
from gi.repository.Gdk import Color
import os, sys
from xdg import BaseDirectory

UI_FILE = "data/ui/save_travel.ui"

class SaveTravelPlan:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)
		self.window.set_default_size(400,-1)

		self.name_entry = self.builder.get_object('entry1')

		self.closebutton = self.builder.get_object('button2')
		self.closebutton.connect("clicked", self.hide_window)

		self.savebutton = self.builder.get_object('button1')
		self.savebutton.connect("clicked", self.saveplan)

	# GTK functions to show and hide the window intelligently
	def show_window(self, fromstation, tostation, viastation):
		self.fromstation = fromstation
		self.tostation = tostation
		self.viastation = viastation
		self.window.show_all()

	# Function to gather the entry inputs from the user and save the travel plan to the file
	def saveplan(self, button):
		self.name = self.name_entry.get_text()
		if self.viastation == "":
			self.viastation = "INIT"
		write_favourite_plan_file = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/favourite_plans", "a")
		write_favourite_plan_file.write("%s|%s|%s|%s|\n" % (self.name, self.fromstation, self.tostation, self.viastation))
		write_favourite_plan_file.close()
		self.window.hide()

	# Function used by close button
	def hide_window(self, button):
		self.window.hide()

	# Function used by window close (x) button
	def hide_window2(self, window, event):
		self.window.hide()
		return True