#! /usr/bin/env python

from gi.repository import Gtk
import os
import sys
import urllib2
import xml.dom.minidom
from datetime import datetime
from xdg import BaseDirectory

from NSTrain_lib.dialog import Dialog
from NSTrain_lib.traveldetails import TravelDetails

TRAVEL_DETAILS_UI_FILE = "data/ui/traveldetails.ui"

class TravelPlanner:
	def __init__(self, builder, station_store, station_list, splashwindow):
		self.travelplanner_xml_init()
		self.travelplanner_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=DT&toStation=UT'
		travelplanner_xml = self.get_travelplanner_xml(self.travelplanner_url)
		self.handle_travelplanner_xml(travelplanner_xml)

		self.builder4 = Gtk.Builder()
		self.builder4.add_from_file(TRAVEL_DETAILS_UI_FILE)
		self.builder4.connect_signals(self)

		self.next_traveloption_button = self.builder4.get_object('toolbutton4')
		self.next_traveloption_button.connect("clicked", self.next_traveloption)
		self.prev_traveloption_button = self.builder4.get_object('toolbutton3')
		self.prev_traveloption_button.connect("clicked", self.prev_traveloption)

		# self.choose_traveloption_button = []
		# self.choose_traveloption_button.append(self.builder4.get_object('button1'))
		# self.choose_traveloption_button.append(self.builder4.get_object('button2'))
		# self.choose_traveloption_button.append(self.builder4.get_object('button3'))
		# self.choose_traveloption_button.append(self.builder4.get_object('button4'))
		# self.choose_traveloption_button.append(self.builder4.get_object('button5'))
		
		# for i in range(len(self.choose_traveloption_button)):
		# 	self.choose_traveloption_button[i].connect("clicked", self.choose_traveloption, i)

		self.statustext = builder.get_object('label26')
		self.statusflag = 0

		self.travel = TravelDetails(self.builder4)

		#for i in range(len(self.travelplanner_list)):
		#	print "[Meldings] %s" % self.travelplanner_list[i][0]

		self.searchbutton = builder.get_object('button3')
		self.searchbutton.set_sensitive( False )
		self.searchbutton.connect("clicked", self.on_search_clicked, station_list)

		if self.travelplanner_list == []:
			splashwindow.hide_splash()
			print "[ERROR]: API Error, empty travel_planner list %s" % self.travelplanner_list
			show_dialog7 = Dialog()
			show_dialog7.error_dialog("Oops!","API Error", '''It seems that the website ns.nl has changed the API required to access the data.
This should either be resolved online or by a new version update of NSTrain. 

Hang in there for us please.

<span style="italic">Error Info: Empty Travel Planner List %s</span>''' % self.travelplanner_list)
			self.statustext.set_markup('''<span foreground="red" weight="bold">Please note that the travel planner is temporarily unavailable. Please try again later</span>''')
			self.statusflag = 1
			self.searchbutton.set_label("Search Disabled!")

		station_completion2 = builder.get_object('completion2')
		station_completion2.set_model(station_store)
		station_completion2.set_text_column(0)

		station_completion3 = builder.get_object('completion3')
		station_completion3.set_model(station_store)
		station_completion3.set_text_column(0)

		station_completion4 = builder.get_object('completion4')
		station_completion4.set_model(station_store)
		station_completion4.set_text_column(0)

		self.fromstation_entry = builder.get_object('entry2')
		self.fromstation_entry.set_completion(station_completion2)
		self.fromstation_entry.connect("changed", self.check_travel_planner, station_list)

		self.viastation_entry = builder.get_object('entry3')
		self.viastation_entry.set_completion(station_completion3)

		self.tostation_entry = builder.get_object('entry4')
		self.tostation_entry.set_completion(station_completion4)
		self.tostation_entry.connect("changed", self.check_travel_planner, station_list)

		t = datetime.time(datetime.now())
		self.time_hour_entry = builder.get_object('spinbutton1')
		self.time_hour_entry.set_value(t.hour)
		
		self.time_minute_entry = builder.get_object('spinbutton2')
		self.time_minute_entry.set_value(t.minute)

		d = datetime.date(datetime.now())
		self.year_entry = builder.get_object('spinbutton3')
		self.year_entry.set_value(d.year)

		self.month_entry = builder.get_object('spinbutton4')
		self.month_entry.set_value(d.month)

		self.date_entry = builder.get_object('spinbutton5')
		self.date_entry.set_value(d.day)

		self.departure_time_chosen = builder.get_object('radiobutton1')
		self.arrival_time_chosen = builder.get_object('radiobutton2')

	# Function to check if the input fields are filled appropriately and only then expose the plan my travel button
	def check_travel_planner(self, widget, station_list):
		self.fromcheck = 0
		self.tocheck = 0

		self.fromstation_name_entry = self.fromstation_entry.get_text()
		self.tostation_name_entry = self.tostation_entry.get_text()
		
		for stationname in range(len(station_list)):
			if self.fromstation_name_entry == station_list[stationname][0]:
					self.fromcheck = 1
			if self.tostation_name_entry == station_list[stationname][0]:
					self.tocheck = 1
		
		if self.fromcheck == 1 and self.tocheck == 1:
			self.searchbutton.set_sensitive( True );
		elif self.fromcheck != 1:
			self.fromcheck = 0
			self.searchbutton.set_sensitive( False );
		else:
			self.tocheck = 0
			self.searchbutton.set_sensitive( False );

	# Function to show the travel plans when the search button is clicked. (first get the inputs, processes it into a url and then get the travel plans)
	def on_search_clicked(self, widget, station_list):
		flag = 0

		fromstation_name_entry = self.fromstation_entry.get_text()
		viastation_name_entry = self.viastation_entry.get_text()
		tostation_name_entry = self.tostation_entry.get_text()
		time_hour_name_entry = self.time_hour_entry.get_value_as_int()
		time_minute_name_entry = self.time_minute_entry.get_value_as_int()
		year_name_entry = self.year_entry.get_value_as_int()
		month_name_entry = self.month_entry.get_value_as_int()
		day_name_entry = self.date_entry.get_value_as_int()

		fromstation_code = "INIT"
		tostation_code = "INIT"
		viastation_code = "INIT"

		for stationname in range(len(station_list)):
			if fromstation_name_entry == station_list[stationname][0]:
				fromstation_code = station_list[stationname][1]
			if tostation_name_entry == station_list[stationname][0]:
				tostation_code = station_list[stationname][1]
			if viastation_name_entry == station_list[stationname][0]:
				viastation_code = station_list[stationname][1]

		basic_url = 'http://webservices.ns.nl/ns-api-treinplanner?'
		url = basic_url

		if fromstation_code != "INIT":
			url = url + 'fromStation=%s' % fromstation_code

		if tostation_code != "INIT":
			url = url + '&' + 'toStation=%s'% tostation_code

		if viastation_code != "INIT":
			url = url + '&' + 'viaStation=%s' % viastation_code

		if self.departure_time_chosen.get_active():
			url = url + '&' + 'departure=true'
		else:
			url = url + '&' + 'departure=false'

		url = url + '&' + 'dateTime=%s-%s-%sT%s:%s' % (year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry)

		try:
			if os.path.isfile(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info"):
				open_user_pref = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/user_info")
				pref_temp = open_user_pref.readlines()
				hispeed = pref_temp[2].split('\n')[0]
				open_user_pref.close()
				if hispeed:
					url = url + '&' + 'hslAllowed=true'
		except:
			pass

		print "[DEBUG]: search url is %s" % url

		# ensuring that these two inputs are valid since they are required for the API call
		if fromstation_code != "INIT" and tostation_code != "INIT" and self.statusflag == 0:
			try:
				travelplanner_xml = self.get_travelplanner_xml(url)
				self.handle_travelplanner_xml(travelplanner_xml)
				flag = 2
			except:
				print "[ERROR]: Wierd website API error...excuse me"
				flag = 1

		# If and only when the data is gathered properly, then proceed to show them to the user
		if flag == 2:
			self.start = 0
			self.end = 5
			self.startpage = 1
			self.endpage = len(self.travelplanner_list)/5
			self.travel.set_traveloption_title(fromstation_name_entry, tostation_name_entry, year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry)
			self.travel.get_traveloption(self.travelplanner_list, self.start, self.startpage, self.endpage)
			self.travel.show_window()

	# Function to display the currently chosen travel option
	def choose_traveloption(self, button, button_number):
		index  = button_number + self.start
		self.travel.get_travelstop(self.travelplanner_list, index)

	# Function to display the next 5 travel options
	def next_traveloption(self, button):
		if self.end+5 <= len(self.travelplanner_list):
			self.start = self.start + 5
			self.end = self.end + 5
			self.startpage = self.startpage + 1
			self.travel.get_traveloption(self.travelplanner_list, self.start, self.startpage, self.endpage)
		else:
			print "[ERROR]: Exceeded maximum length of traveloption_list"

	# Function to display the previous 5 travel options
	def prev_traveloption(self, button):
		if self.start-5 >= 0:
			self.start = self.start - 5
			self.end = self.end - 5
			self.startpage = self.startpage - 1
			self.travel.get_traveloption(self.travelplanner_list, self.start, self.startpage, self.endpage)
		else:
			print "[ERROR]: Below zero index..."

	# Function to iniatilize xml related variables
	def travelplanner_xml_init(self):
		self.list = []
		self.travelplanner_list = []
		self.reisdeel = []
		self.reisdeeltemp = []
		self.reisstop = []
		self.reisstoptemp = []
		self.melding = []
		self.meldingtemp = []

	# Function to get the xml file from the url
	def get_travelplanner_xml(self, url):
		xmlfile = urllib2.urlopen(url)
		doc = xml.dom.minidom.parse(xmlfile)
		node = doc.documentElement
		return node

		# Function to handle the entire xml object
	def handle_travelplanner_xml(self, xml):
		api_flag = 0
		try:
			traveloptions = xml.getElementsByTagName("ReisMogelijkheid")
			if traveloptions == []:
				print "[ERROR]: API ERROR - Cannot retrieve travel planner (EMPTY)"
				api_flag = 1
			else:
				self.handle_travelplanner_traveloptions(traveloptions)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve travel planner"
			api_flag = 1

		if api_flag == 1:
			print "[ERROR]: API Error..failed at handle_travelplanner_xml"

	def handle_travelplanner_traveloptions(self, traveloptions):
		self.travelplanner_list = []
		for traveloption in traveloptions:
			self.handle_travelplanner_traveloption(traveloption)
			self.list = []

	def handle_travelplanner_traveloption(self, traveloption):
		self.handle_travelplanner_meldings(traveloption)

		try:
			no_of_transfers = self.getElement(traveloption.getElementsByTagName("AantalOverstappen")[0])
			self.list.append(no_of_transfers)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve no of transfers"
			no_of_transfers = "Error"
			self.list.append(no_of_transfers)

		try:
			planned_traveltime = self.getElement(traveloption.getElementsByTagName("GeplandeReisTijd")[0])
			self.list.append(planned_traveltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned travel time"
			planned_traveltime = "Error"
			self.list.append(planned_traveltime)

		try:
			actual_traveltime = self.getElement(traveloption.getElementsByTagName("ActueleReisTijd")[0])
			self.list.append(actual_traveltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual travel time"
			actual_traveltime = "Error"
			self.list.append(actual_traveltime)

		try:
			optimum = self.getElement(traveloption.getElementsByTagName("Optimaal")[0])
			self.list.append(optimum)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve optimum status"
			optimum = "Error"
			self.list.append(optimum)

		try:
			planned_departuretime = self.getElement(traveloption.getElementsByTagName("GeplandeVertrekTijd")[0])
			self.list.append(planned_departuretime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned departure time"
			planned_departuretime = "XXXX-XX-XXTXX:XX:XX"
			self.list.append(planned_departuretime)

		try:
			actual_departuretime = self.getElement(traveloption.getElementsByTagName("ActueleVertrekTijd")[0])
			self.list.append(actual_departuretime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual departure time"
			actual_departuretime = "XXXX-XX-XXTXX:XX:XX"
			self.list.append(actual_departuretime)

		try:
			planned_arrivaltime = self.getElement(traveloption.getElementsByTagName("GeplandeAankomstTijd")[0])
			self.list.append(planned_arrivaltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned arrival time"
			planned_arrivaltime = "XXXX-XX-XXTXX:XX:XX"
			self.list.append(planned_arrivaltime)

		try:
			actual_arrivaltime = self.getElement(traveloption.getElementsByTagName("ActueleAankomstTijd")[0])
			self.list.append(actual_arrivaltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual arrival time"
			actual_arrivaltime = "XXXX-XX-XXTXX:XX:XX"
			self.list.append(actual_arrivaltime)

		try:
			status = self.getElement(traveloption.getElementsByTagName("Status")[0])
			self.list.append(status)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve status"
			status = "0"
			self.list.append(status)

		self.handle_travelplanner_travelsections(traveloption)

		try:
			departure_delay = self.getElement(traveloption.getElementsByTagName("VertrekVertraging")[0])
			self.list.append(departure_delay)
		except:
			#print "[ERROR]: API ERROR - Cannot retrieve departure delay"
			departure_delay = "0"
			self.list.append(departure_delay)

		try:
			arrival_delay = self.getElement(traveloption.getElementsByTagName("AankomstVertraging")[0])
			self.list.append(arrival_delay)
		except:
			#print "[ERROR]: API ERROR - Cannot retrieve arrival delay"
			arrival_delay = "0"
			self.list.append(arrival_delay)

		self.travelplanner_list.append(self.list)

	def handle_travelplanner_meldings(self, traveloption):
		try:
			meldings = traveloption.getElementsByTagName("Melding")
			self.melding = []
			for melding in meldings:
				self.handle_travelplanner_melding(melding)
				self.meldingtemp = []
			self.list.append(self.melding)
		except:
			print "I am in exception"

	def handle_travelplanner_melding(self, melding):
		try:
			melding_id = self.getElement(melding.getElementsByTagName("Id")[0])
			self.meldingtemp.append(melding_id)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve melding_id (Melding)"
			melding_id = "0"
			self.meldingtemp.append(melding_id)

		try:
			melding_severity = self.getElement(melding.getElementsByTagName("Ernstig")[0])
			self.meldingtemp.append(melding_severity)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve melding_severity (Melding)"
			melding_severity = "0"
			self.meldingtemp.append(melding_severity)

		try:
			melding_message = self.getElement(melding.getElementsByTagName("Text")[0])
			self.meldingtemp.append(melding_message)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve melding_message (Melding)"
			melding_message = "Not Available"
			self.meldingtemp.append(melding_message)

		self.melding.append(self.meldingtemp)

	def handle_travelplanner_travelsections(self, traveloption):
		travelsections = traveloption.getElementsByTagName("ReisDeel")
		self.reisdeel = []
		for travelsection in travelsections:
			self.handle_travelplanner_travelsection(travelsection)
			self.reisdeeltemp = []
		self.list.append(self.reisdeel)
			
	def handle_travelplanner_travelsection(self, travelsection):
		try:
			train_carrier = self.getElement(travelsection.getElementsByTagName("Vervoerder")[0])
			self.reisdeeltemp.append(train_carrier)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_carrier (REISDEEL)"
			train_carrier = "Error"
			self.reisdeeltemp.append(train_carrier)

		try:
			train_type = self.getElement(travelsection.getElementsByTagName("VervoerType")[0])
			self.reisdeeltemp.append(train_type)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_type (REISDEEL)"
			train_type = "Error"
			self.reisdeeltemp.append(train_type)

		try:
			train_number = self.getElement(travelsection.getElementsByTagName("RitNummer")[0])
			self.reisdeeltemp.append(train_number)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_number (REISDEEL)"
			train_number = "Error"
			self.reisdeeltemp.append(train_number)

		try:
			trainstatus = self.getElement(travelsection.getElementsByTagName("Status")[0])
			self.reisdeeltemp.append(trainstatus)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve status"
			trainstatus = "Error"
			self.reisdeeltemp.append(trainstatus)

		self.reisdeel.append(self.reisdeeltemp)

		self.handle_travelplanner_travelstops(travelsection)

	def handle_travelplanner_travelstops(self, travelsection):
		travelstops = travelsection.getElementsByTagName("ReisStop")
		self.reisstop = []
		for travelstop in travelstops:
			#print travelstop
			self.handle_travelplanner_travelstop(travelstop)
			self.reisstoptemp = []
		self.reisdeel.append(self.reisstop)

	def handle_travelplanner_travelstop(self, travelstop):
		try:
			train_name = self.getElement(travelstop.getElementsByTagName("Naam")[0])
			self.reisstoptemp.append(train_name)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_name (REISSTOP)"
			train_name = "Not Available"
			self.reisstoptemp.append(train_name)

		try:
			train_time = self.getElement(travelstop.getElementsByTagName("Tijd")[0])
			self.reisstoptemp.append(train_time)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_type (REISSTOP)"
			train_time = "Not Available"
			self.reisstoptemp.append(train_time)

		try:
			train_platform = self.getElement(travelstop.getElementsByTagName("Spoor")[0])
			self.reisstoptemp.append(train_platform)
			#for name in travelstop.getElementsByTagName("Spoor")[0].attributes.items():
			#	print name[1]
		except:
			#print "[ERROR]: API ERROR - Cannot retrieve train_platform (REISSTOP)"
			train_platform = ""
			self.reisstoptemp.append(train_platform)

		self.reisstop.append(self.reisstoptemp)

	# Function to convert a xml object into a text which can be used
	def getElement(self, element):
		return self.getText(element.childNodes)

	def getText(self, nodelist):
		rc = ""
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc = rc + node.data
		return rc
