#! /usr/bin/env python

from gi.repository import Gtk
import os,sys
from xdg import BaseDirectory

UI_FILE = "data/ui/preference.ui"

class Preferences:
	def __init__(self, station_store):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)

		self.name_entry = self.builder.get_object('entry1')
		self.station_entry = self.builder.get_object('entry2')
		# self.hispeed = self.builder.get_object('switch1')

		self.pref_station_completion = self.builder.get_object('entrycompletion1')
		self.pref_station_completion.set_model(station_store)
		self.pref_station_completion.set_text_column(0)
		self.station_entry.set_completion(self.pref_station_completion)

		self.cancelbutton = self.builder.get_object('button2')
		self.cancelbutton.connect("clicked", self.hide_window)
		self.initial_read()

	def initial_read(self):
		if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "r")
			pref_temp = open_user_pref.readlines()
			self.name_entry.set_text(pref_temp[0].split('\n')[0])
			self.station_entry.set_text(pref_temp[1].split('\n')[0])
			# try:
			# 	if pref_temp[2].split('\n')[0] == "true":
			# 		print "[DEBUG]: setting hispeed to true"
			# 		self.hispeed.set_active(TRUE)
			# 	else:
			# 		print "[DEBUG]: setting hispeed to false"
			# 		self.hispeed.set_active(FALSE)
			# except:
			# 	pass
			open_user_pref.close()
		else:
			print "[ERROR]: User Preference File not found...aborting initial preference reading"

	def apply_button_clicked(self, widget):
		open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "w")
		open_user_pref.write(self.name_entry.get_text() + '\n')
		open_user_pref.write(self.station_entry.get_text() + '\n')
		# if self.hispeed.get_active():
		# 	open_user_pref.write("true" + '\n')
		# else:
		# 	open_user_pref.write("false" + '\n')
		open_user_pref.close()

	def ok_button_clicked(self, widget):
		open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "w")
		open_user_pref.write(self.name_entry.get_text() + '\n')
		open_user_pref.write(self.station_entry.get_text() + '\n')
		# if self.hispeed.get_active():
		# 	open_user_pref.write("true" + '\n')
		# else:
		# 	open_user_pref.write("false" + '\n')
		open_user_pref.close()
		self.window.hide()

	# GTK functions to show and hide the window intelligently
	def show_window(self, widget):
		self.initial_read()
		self.window.show_all()

	def hide_window(self, button):
		self.window.hide()

	def hide_window2(self, window, event):
		self.window.hide()
		return True
