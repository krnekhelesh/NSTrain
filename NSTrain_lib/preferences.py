#! /usr/bin/env python

from gi.repository import Gtk
import os,sys
from xdg import BaseDirectory

UI_FILE = "data/ui/preference.ui"

class Preferences:
	def __init__(self, station_store, station_list):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)

		self.name_entry = self.builder.get_object('entry1')
		self.station_entry = self.builder.get_object('entry2')
		self.station_entry.connect("changed", self.station_entry_otf, station_list)
		self.hispeed = self.builder.get_object('checkbutton1')

		self.pref_station_completion = self.builder.get_object('entrycompletion1')
		self.pref_station_completion.set_model(station_store)
		self.pref_station_completion.set_text_column(0)
		self.station_entry.set_completion(self.pref_station_completion)

		self.cancelbutton = self.builder.get_object('button2')
		self.cancelbutton.connect("clicked", self.hide_window)
		self.initial_read()

	# Function to read the user preference when the preference dialog is open and at program start.
	def initial_read(self):
		if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "r")
			pref_temp = open_user_pref.readlines()
			self.name_entry.set_text(pref_temp[0].split('\n')[0])
			self.station_entry.set_text(pref_temp[1].split('\n')[0])
			try:
				if pref_temp[2].split('\n')[0] == "true":
					print "[DEBUG]: setting hispeed to true"
					self.hispeed.set_active( True )
				else:
					print "[DEBUG]: setting hispeed to false"
					self.hispeed.set_active( False )
			except:
				pass
			open_user_pref.close()
		else:
			print "[ERROR]: User Preference File not found...aborting initial preference reading"

	# Function to write the user name preference on the fly i.e as it is inputted by the user. It reads
	# the file and then writes only the new name while still writing the other old fields.
	def name_entry_otf(self, entry):
		if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "r")
			pref_temp = open_user_pref.readlines()
			open_user_pref.close()

			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "w")
			open_user_pref.write(self.name_entry.get_text() + '\n')
			open_user_pref.write(pref_temp[1].split('\n')[0] + '\n')
			try:
				if pref_temp[2].split('\n')[0] == "true":
					open_user_pref.write("true" + '\n')
				else:
					open_user_pref.write("false" + '\n')
			except:
				pass
			open_user_pref.close()
		else:
			print "[ERROR]: User Preference File not found...aborting name entry write"

	# Function to write the station name preference on the fly i.e as it is inputted by the user.
	# However before reading or writing into the file, it checks the validity of the station input
	# given by the user to avoid unnecessary file operations.
	def station_entry_otf(self, entry, station_list):
		self.check = 0
		self.writestation = self.station_entry.get_text()
		for stationname in range(len(station_list)):
			if self.writestation == station_list[stationname][0]:
					self.check = 1
		if self.check == 1:
			if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
				open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "r")
				pref_temp = open_user_pref.readlines()
				open_user_pref.close()

				open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "w")
				open_user_pref.write(pref_temp[0].split('\n')[0] + '\n')
				open_user_pref.write(self.station_entry.get_text() + '\n')
				try:
					if pref_temp[2].split('\n')[0] == "true":
						open_user_pref.write("true" + '\n')
					else:
						open_user_pref.write("false" + '\n')
				except:
					pass
				open_user_pref.close()
			else:
				print "[ERROR]: User Preference File not found...aborting station name entry write"
		else:
			self.check = 0

	# Function to write the hispeed toggle option on the fly i.e as it is changed by the user.
	def hispeed_check_button_toggled(self, widget):
		if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "r")
			pref_temp = open_user_pref.readlines()
			self.name_entry.set_text(pref_temp[0].split('\n')[0])
			self.station_entry.set_text(pref_temp[1].split('\n')[0])
			open_user_pref.close()

			open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info", "w")
			open_user_pref.write(self.name_entry.get_text() + '\n')
			open_user_pref.write(self.station_entry.get_text() + '\n')
			if self.hispeed.get_active():
				open_user_pref.write("true" + '\n')
			else:
				open_user_pref.write("false" + '\n')
			open_user_pref.close()
		else:
			print "[ERROR]: User Preference File not found...aborting hispeed toggle write"

	# GTK functions to show and hide the window intelligently
	def show_window(self, widget):
		self.initial_read()
		self.window.show_all()

	def hide_window(self, button):
		self.window.hide()

	def hide_window2(self, window, event):
		self.window.hide()
		return True
