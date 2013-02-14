#! /usr/bin/env python

from gi.repository import Gtk
from gi.repository.Gdk import Color
import os
import sys
import urllib2
import xml.dom.minidom
from datetime import datetime, timedelta
from xdg import BaseDirectory

from nstrain.dialog import Dialog
from nstrain.traveldetails import TravelDetails

class TravelPlanner:
	def __init__(self, builder, station_store, station_list, favouriteplan, loadplan):
		self.travelplanner_xml_init()
		self.travel = TravelDetails()

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

		self.viastation_entry = builder.get_object('entry3')
		self.viastation_entry.set_completion(station_completion3)

		self.tostation_entry = builder.get_object('entry4')
		self.tostation_entry.set_completion(station_completion4)
		self.tostation_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "mail-send-receive-symbolic")
		self.tostation_entry.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)
		self.tostation_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Swap from and to stations")
		self.tostation_entry.connect("icon-press", self.transfer_station)

		self.traveltime_store = Gtk.ListStore(str)
		self.traveltime_store.append(["Departure"])
		self.traveltime_store.append(["Arrival"])
		self.traveltime = builder.get_object('comboboxtext1')
		self.traveltime.set_model(self.traveltime_store)
		self.traveltime.set_active(0)

		self.date_store = Gtk.ListStore(str)
		self.date_store.append(["Today"])
		self.date_store.append(["Tomorrow"])
		self.date = builder.get_object('comboboxtext2')
		self.date.set_entry_text_column(0)		
		self.date.set_model(self.date_store)
		self.date.set_active(0)

		self.time_store = Gtk.ListStore(str)
		self.time_store.append(["Now"])
		self.time_store.append(["+ 15 minutes"])
		self.time_store.append(["+ 30 minutes"])
		self.time_store.append(["+ 1 hour"])
		self.time = builder.get_object('comboboxtext3')
		self.time.set_model(self.time_store)
		self.time.set_active(0)

		self.statustext = builder.get_object('label26')

		self.searchbutton = builder.get_object('button3')
		self.searchbutton.connect("clicked", self.on_search_clicked, station_list)

		self.loadtravelplan_button = builder.get_object('button6')
		self.loadtravelplan_button.connect('clicked', self.loadtravelplan, loadplan)

		self.savetravelplan_button = builder.get_object('button5')
		self.savetravelplan_button.connect('clicked', self.savetravelplan, favouriteplan, station_list)

	def transfer_station(self, entry, position, user_data):
		self.temp_name = self.fromstation_entry.get_text()
		self.fromstation_entry.set_text(self.tostation_entry.get_text())
		self.tostation_entry.set_text(self.temp_name)

	def loadtravelplan(self, button, loadplan):
		loadplan.show_window2(self.fromstation_entry, self.tostation_entry, self.viastation_entry)

	def savetravelplan(self, button, favouriteplan, station_list):
		self.saveplan_flag = self.check_travel_planner(station_list)

		fromstation_name_entry = self.fromstation_entry.get_text()
		viastation_name_entry = self.viastation_entry.get_text()
		tostation_name_entry = self.tostation_entry.get_text()

		if self.saveplan_flag == 1:
			favouriteplan.show_window(fromstation_name_entry, tostation_name_entry, viastation_name_entry)

	# Function to check if the input fields are filled appropriately and only then expose the plan my travel button
	def check_travel_planner(self, station_list):
		self.fromcheck = 0
		self.tocheck = 0

		COLOR_INVALID = Color(50000, 0, 0) # A dark red color
				
		self.fromstation_name_entry = self.fromstation_entry.get_text()
		self.tostation_name_entry = self.tostation_entry.get_text()
		
		for stationname in range(len(station_list)):
			if self.fromstation_name_entry == station_list[stationname][0]:
					self.fromcheck = 1
			if self.tostation_name_entry == station_list[stationname][0]:
					self.tocheck = 1
		
		if self.fromcheck != 1:
			self.fromstation_entry.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
			self.fromstation_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "emblem-important-symbolic")
			self.fromstation_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Incorrect station name")
			if self.fromstation_name_entry == "":
				self.fromstation_entry.set_text("Departure Station")
		else:
			self.fromstation_entry.modify_fg(Gtk.StateFlags.NORMAL, None)
			self.fromstation_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
			self.fromstation_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, None)

		if self.tocheck != 1:
			self.tostation_entry.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
			self.tostation_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "emblem-important-symbolic")
			self.tostation_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Incorrect station name")
			self.tostation_entry.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, False)
			if self.tostation_name_entry == "":
				self.tostation_entry.set_text("Arrival Station")
		else:
			self.tostation_entry.modify_fg(Gtk.StateFlags.NORMAL, None)
			self.tostation_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "mail-send-receive-symbolic")
			self.tostation_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Swap from and to stations")
			self.tostation_entry.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)

		if self.fromcheck == 1 and self.tocheck == 1:
			return 1
		else:
			return 0

	# Function to show the travel plans when the search button is clicked. (first get the inputs, processes it into a url and then get the travel plans)
	def on_search_clicked(self, widget, station_list):
		self.travel_flag = self.check_travel_planner(station_list)

		if self.travel_flag == 1:
			flag = 0
			date_list = []
			time_list = []

			fromstation_name_entry = self.fromstation_entry.get_text()
			viastation_name_entry = self.viastation_entry.get_text()
			tostation_name_entry = self.tostation_entry.get_text()

			date_tree_iter = self.date.get_active_iter()
			if date_tree_iter != None:
				model = self.date.get_model()
				date_entry = model[date_tree_iter][0]
				# print date_entry
			else:
				entry = self.date.get_child()
				date_entry = entry.get_text()
				# print "Entered Date: %s" % date_entry

			d = datetime.date(datetime.now())
			if date_entry == "Today":				
				day_name_entry = d.day
				month_name_entry = d.month
				year_name_entry = d.year				
			elif date_entry == "Tomorrow":
				d_new = d + timedelta(days=1)
				day_name_entry = d_new.day
				month_name_entry = d_new.month
				year_name_entry = d_new.year			
			else:
				date_list = date_entry.split('-')
				year_name_entry = int(date_list[0])
				month_name_entry = int(date_list[1])
				day_name_entry = int(date_list[2])

			# print "Precieved Date: %s-%s-%s" % (year_name_entry, month_name_entry, day_name_entry)

			time_tree_iter = self.time.get_active_iter()
			if time_tree_iter != None:
				model = self.time.get_model()
				time_entry = model[time_tree_iter][0]
				# print time_entry
			else:
				entry = self.time.get_child()
				time_entry = entry.get_text()
				# print "Entered Time: %s" % date_entry

			t = datetime.time(datetime.now())
			t_temp = datetime(year_name_entry, month_name_entry, day_name_entry, t.hour, t.minute)
			if time_entry == "Now":				
				time_hour_name_entry = t.hour
				time_minute_name_entry = t.minute
			elif time_entry == "+ 15 minutes":
				t_new = t_temp + timedelta(minutes=15)
				time_hour_name_entry = t_new.hour
				time_minute_name_entry = t_new.minute
			elif time_entry == "+ 30 minutes":
				t_new = t_temp + timedelta(minutes=30)
				time_hour_name_entry = t_new.hour
				time_minute_name_entry = t_new.minute
			elif time_entry == "+ 1 hour":
				t_new = t_temp + timedelta(hours=1)
				time_hour_name_entry = t_new.hour
				time_minute_name_entry = t_new.minute
			else:
				time_list = time_entry.split(':')
				time_hour_name_entry = int(time_list[0])
				time_minute_name_entry = int(time_list[1])

			# print "Preceived Time: %s:%s" % (time_hour_name_entry, time_minute_name_entry)

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

			url = url + '&' + 'previousAdvices=0'

			traveltime_tree_iter = self.traveltime.get_active_iter()
			model = self.traveltime.get_model()
			traveltime_type = model[traveltime_tree_iter][0]
			# print traveltime_type

			if traveltime_type == "Departure":
				url = url + '&' + 'departure=true'
			else:
				url = url + '&' + 'departure=false'

			url = url + '&' + 'dateTime=%s-%s-%sT%s:%s' % (year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry)
			
			# url = url + '&' + 'hslAllowed=true'

			print "[DEBUG]: search url is %s" % url

			# ensuring that these two inputs are valid since they are required for the API call
			if fromstation_code != "INIT" and tostation_code != "INIT":
				try:
					travelplanner_xml = self.get_travelplanner_xml(url)
					self.handle_travelplanner_xml(travelplanner_xml)
					flag = 2
				except:
					print "[ERROR]: Wierd website API error...excuse me"
					flag = 1

			# If and only when the data is gathered properly, then proceed to show them to the user
			if flag == 2:
				self.travel.final_traveloption(self.travelplanner_list, fromstation_name_entry, tostation_name_entry, year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry)

		else:
			pass		

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
