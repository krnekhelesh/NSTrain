#! /usr/bin/env python

# Imports
from gi.repository import Gtk
import os, sys
import urllib2
import xml.dom.minidom

from nsapistations import NsApiStations
from departuretrains import DepartureTrains
from travelplanner import TravelPlanner
from dialog import Dialog
from help import show_uri, get_help_uri

# Glade UI file paths
MAIN_UI_FILE = "main.ui"
ABOUT_UI_FILE = "about.ui"
START_WIZARD_UI_FILE = "startwizard.ui"

class nstrain:
	# Iniatialising Function
	def __init__(self):
		# Importing the Glade user interface files and their objects
		self.builder = Gtk.Builder()
		self.builder.add_from_file(MAIN_UI_FILE)
		self.builder.connect_signals(self)

		self.builder2 = Gtk.Builder()
		self.builder2.add_from_file(ABOUT_UI_FILE)
		self.builder2.connect_signals(self)

		self.builder3 = Gtk.Builder()
		self.builder3.add_from_file(START_WIZARD_UI_FILE)
		self.builder3.connect_signals(self)

		self.start_wizard = self.builder3.get_object('wizard')
		self.start_wizard.connect("destroy", self.destroy)
		self.name_entry = self.builder3.get_object('entry1')
		self.wizard_station_entry = self.builder3.get_object('entry2')
		self.about_dialog = self.builder2.get_object('aboutdialog')
		self.window = self.builder.get_object('window')
		self.username = self.builder.get_object('name')

		# Gathering Stations codes (after authentication) and populating the station_store (before the startup wizard)
		self.stat = NsApiStations()
		if self.stat.station_list == []:
			print "[ERROR]: Station list %s" % self.stat.station_list
			show_dialog = Dialog()
			show_dialog.error_dialog("Oops!","API Error", '''It seems that the website ns.nl has changed the API required to access the data.
This should either be resolved online or by a new version update of NSTrain. 

Hang in there for us please. The program will now quit.

<span style="italic">Error Info: Empty Station List %s</span>''' % self.stat.station_list)
			sys.exit(0)
		else:
			self.station_model_populate()

			self.station_completion = self.builder.get_object('completion1')
			self.station_completion.set_model(self.station_store)
			self.station_completion.set_text_column(0)

			self.wizard_station_entry.set_completion(self.station_completion)
			self.wizard_station_entry.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FIND)

			# Check for user_info configuration file. If not present then show the start wizard
			if os.path.isfile("user_info"):
				print 
				print "[INFO] : Start Wizard complete"
				print
				self.open_user_info = open("user_info")
				self.readname = self.open_user_info.readline()
				self.readname = self.readname.strip('\n')
				self.readstation = self.open_user_info.readline()
				self.readstartion = self.readstation.strip('\n')
				self.username.set_markup('''Welcome, <b>%s</b>''' % self.readname)
				try:
					self.deptrain = DepartureTrains(self.builder, self.stat.station_list, self.readstation, self.station_completion)
				except:
					print "[ERROR]: Departure failed"
				try:
					self.travelplanner = TravelPlanner(self.builder, self.station_store, self.stat.station_list)
				except:
					print "[ERROR]: Travel planner failed"
				self.window.show_all()
			else:
				print 
				print "[INFO] : Start Wizard starting"
				print
				self.start_wizard.show_all()

	# Function to collect start wizard data, write data into a file and close the wizard
	def finish_start_wizard(self, button):
		self.writename = self.name_entry.get_text()
		self.writestation = self.wizard_station_entry.get_text()
		self.user_info = open("user_info", "w")
		self.user_info.write(self.writename + '\n' + self.writestation)
		self.user_info.close()
		self.start_wizard.hide()
		try:
			self.deptrain = DepartureTrains(self.builder, self.stat.station_list, self.writestation, self.station_completion)
		except:
			print "[ERROR]: Departure failed"
		try:
			self.travelplanner = TravelPlanner(self.builder, self.station_store, self.stat.station_list)
		except:
			print "[ERROR]: Travel planner failed"
		self.username.set_markup('''Welcome, <b>%s</b>''' % self.writename)
		self.window.show_all()

	# Function to populate station model
	def station_model_populate(self):
		self.station_store = Gtk.ListStore(str, str)
		for stationname in range(len(self.stat.station_list)):
			self.station_store.append([self.stat.station_list[stationname][0], self.stat.station_list[stationname][1]])

	# Function to display the about dialog
	def about_function(self, window):
		self.about_dialog.run()
		self.about_dialog.hide()

	# Function to display the help dialog
	def help_function(self, button):
		show_uri(self, "ghelp:%s" % get_help_uri())

	# Function to destroy the parent window
	def destroy(self, window):
		Gtk.main_quit()

def main():
	app = nstrain()
	Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
