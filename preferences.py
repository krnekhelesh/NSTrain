#! /usr/bin/env python

from gi.repository import Gtk
import os,sys

UI_FILE = "preference.ui"

class Preferences:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("destroy", self.destroy)
		self.window.show_all()

		self.name_entry = self.builder.get_object('entry1')
		self.station_entry = self.builder.get_object('entry2')

		self.applybutton = self.builder.get_object('button3')
		self.applybutton.connect("clicked", self.apply_button_clicked)

		self.okbutton = self.builder.get_object('button1')
		self.okbutton.connect("clicked", self.ok_button_clicked)

		self.cancelbutton = self.builder.get_object('button2')
		self.cancelbutton.connect("clicked", self.destroy)

		self.initial_read()

	def initial_read(self):
		print "Initial read"
		if os.path.isfile("user_info"):
			print "File exists...proceed"
			self.open_user_pref = open("user_info", "r")
			pref_temp = self.open_user_pref.readlines()
			self.name_entry.set_text(pref_temp[0].split('\n')[0])
			self.station_entry.set_text(pref_temp[1])

	def apply_button_clicked(self, widget):
		print "You pressed apply"

	def ok_button_clicked(self, widget):
		print "You pressed ok"

	def destroy(self, window):
		Gtk.main_quit()

def main():
	app = Preferences()
	Gtk.main()
	
if __name__ == "__main__":
	main()

