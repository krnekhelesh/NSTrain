#! /usr/bin/env python

from gi.repository import Gtk
import os,sys

UI_FILE = "preference.ui"

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
		self.hispeed = self.builder.get_object('switch1')
		self.inform = self.builder.get_object('label6')
		self.inform.set_label("")

		self.pref_station_completion = self.builder.get_object('entrycompletion1')
		self.pref_station_completion.set_model(station_store)
		self.pref_station_completion.set_text_column(0)
		self.station_entry.set_completion(self.pref_station_completion)
		self.station_entry.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FIND)

		self.applybutton = self.builder.get_object('button3')
		self.applybutton.connect("clicked", self.apply_button_clicked)

		self.okbutton = self.builder.get_object('button1')
		self.okbutton.connect("clicked", self.ok_button_clicked)

		self.cancelbutton = self.builder.get_object('button2')
		self.cancelbutton.connect("clicked", self.hide_window)

		self.initial_read()

	def initial_read(self):
		if os.path.isfile("user_info"):
			open_user_pref = open("user_info", "r")
			pref_temp = open_user_pref.readlines()
			self.name_entry.set_text(pref_temp[0].split('\n')[0])
			self.station_entry.set_text(pref_temp[1].split('\n')[0])
			try:
				if pref_temp[2].split('\n')[0]:
					self.hispeed.set_active("true")
				else:
					self.hispeed.set_active("false")
			except:
				pass
			open_user_pref.close()
		else:
			print "[ERROR]: User Preference File not found...aborting"

	def apply_button_clicked(self, widget):
		open_user_pref = open("user_info", "w")
		open_user_pref.write(self.name_entry.get_text() + '\n')
		open_user_pref.write(self.station_entry.get_text() + '\n')
		if self.hispeed.get_active():
			open_user_pref.write("true" + '\n')
		else:
			open_user_pref.write("false" + '\n')
		open_user_pref.close()
		self.inform.set_label("The settings will be applied on restart!")

	def ok_button_clicked(self, widget):
		open_user_pref = open("user_info", "w")
		open_user_pref.write(self.name_entry.get_text() + '\n')
		open_user_pref.write(self.station_entry.get_text() + '\n')
		if self.hispeed.get_active():
			open_user_pref.write("true" + '\n')
		else:
			open_user_pref.write("false" + '\n')
		open_user_pref.close()
		self.window.hide()
		self.inform.set_label("")

	# GTK functions to show and hide the window intelligently
	def show_window(self, widget):
		self.window.show_all()

	def hide_window(self, button):
		self.window.hide()
		self.inform.set_label("")

	def hide_window2(self, window, event):
		self.window.hide()
		return True
