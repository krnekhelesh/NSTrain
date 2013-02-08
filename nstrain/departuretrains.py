#! /usr/bin/env python

from gi.repository import Gtk
import os, sys
import urllib2
import xml.dom.minidom

class DepartureTrains:
	# Iniatialising Function (first authenticate, get ui objects, load user config)
	def __init__(self, builder, station_list, user_station, station_completion):
		self.departure_xml_init()
		self.departure_url = 'http://webservices.ns.nl/ns-api-avt?station=UT'
		departure_xml = self.get_departure_xml(self.departure_url)
		self.handle_departure_xml(departure_xml)

		if self.train_list == []:
			print "[ERROR]: Empty departure train list %s" % self.train_list

		self.station_entry = builder.get_object('entry1')
		self.station_entry.set_completion(station_completion)
		self.station_entry.connect("activate", self.get_departure_station_entry, station_list)

		self.deptrain_store = Gtk.ListStore(str, str, str)		
		self.deptrain_tree = builder.get_object('treeview1')		
		self.deptrain_tree.set_model(self.deptrain_store)

		self.timecolumn = Gtk.TreeViewColumn("Time", Gtk.CellRendererText(), markup=0)
		self.timecolumn.set_expand(True)
		self.timecolumn.set_alignment(0.5)

		self.tocolumn = Gtk.TreeViewColumn("To", Gtk.CellRendererText(), markup=1)
		self.tocolumn.set_expand(True)
		self.tocolumn.set_alignment(0.5)		
		
		self.trackcolumn = Gtk.TreeViewColumn("Track", Gtk.CellRendererText(), text=2)
		self.trackcolumn.set_expand(True)
		self.trackcolumn.set_alignment(0.5)

		self.deptrain_tree.append_column(self.timecolumn)
		self.deptrain_tree.append_column(self.tocolumn)
		self.deptrain_tree.append_column(self.trackcolumn)

		for i in range(0, 5):
			self.deptrain_store.append(["Time","Train","Track"])
			#print "deptrain store appending with Time, Train, Track..."
		
		self.next_deptrain_button = builder.get_object('toolbutton5')
		self.prev_deptrain_button = builder.get_object('toolbutton4')
		self.next_deptrain_button.connect("clicked", self.next_departure)
		self.prev_deptrain_button.connect("clicked", self.prev_departure)

		self.pagelabel = builder.get_object('label20')

		try:
			print "[INFO] : Trying to load user departure station trains"
			self.station_entry.set_text("%s" % user_station) 
			for stationname in range(len(station_list)):
				if user_station == station_list[stationname][0]:
					user_station_code = station_list[stationname][1]

			self.user_search_url = 'http://webservices.ns.nl/ns-api-avt?station=%s' % user_station_code
			user_departure_xml = self.get_departure_xml(self.user_search_url)
			self.handle_departure_xml(user_departure_xml)

			self.start = 0
			self.end = 5
			self.startpage = 1
			self.endpage = len(self.train_list)/5
			self.pagelabel.set_text("%s of %s" % (self.startpage, self.endpage))
			self.get_departure_time()
			self.get_departure_train()
			self.get_departure_track()
			print "[INFO] : Loaded trains departing from user departure station: %s,  %s" % (user_station, user_station_code)
		except:
			print "[ERROR]: Invalid user station name!"
			print "[DEBUG]: User Departure Station Name: %s" % user_station

	# Function to get the departure input from the entry box and display results properly
	def get_departure_station_entry(self, entry, station_list):
		try:
			station_name_entry = self.station_entry.get_text()
			print " "
			print "[DEBUG]: Departure Station Name: %s" % station_name_entry

			for stationname in range(len(station_list)):
				if station_name_entry == station_list[stationname][0]:
					station_code_entry = station_list[stationname][1]
					print "[DEBUG]: Departure Station Code: %s" % station_code_entry
					
			self.search_url = 'http://webservices.ns.nl/ns-api-avt?station=%s' % station_code_entry
			departure_xml = self.get_departure_xml(self.search_url)
			self.handle_departure_xml(departure_xml)

			self.start = 0
			self.end = 5
			self.startpage = 1
			self.endpage = len(self.train_list)/5
			self.pagelabel.set_text("%s of %s" % (self.startpage, self.endpage))
			self.get_departure_time()
			self.get_departure_train()
			self.get_departure_track()
		except:
			print "[ERROR]: Invalid station name!"

	# Function to manipulate the time string
	def get_departure_time(self):
		self.time_value1 = [] 
		self.time_value2 = []
		self.time_actualvalue = []
		for time in range(0, 5):
			self.time_value1.append(self.train_list[self.start+time][1].split('T'))
			self.time_value2.append(self.time_value1[time][1].split('+'))
			if self.train_list[self.start+time][6] != "0":
				#self.time_actualvalue.append(self.time_value2[time][0] + "\n" + self.train_list[self.start+time][6])
				self.time_actualvalue.append('''%s 
<span foreground="red">%s</span>''' % (self.time_value2[time][0], self.train_list[self.start+time][6]))
			else:
				self.time_actualvalue.append('''%s''' % (self.time_value2[time][0]))

		for i in range(0, 5):
			self.deptrain_store[i][0] = self.time_actualvalue[i]

	# Function to manipulate the train string
	def get_departure_train(self):
		self.deptrain_value = []
		for train in range(self.start, self.end):
			#self.deptrain_value.append(self.train_list[train][2] + "\n" + self.train_list[train][3] + "\n" + self.train_list[train][7])
			self.deptrain_value.append('''<span weight="bold">%s</span>
%s
%s''' % (self.train_list[train][2],self.train_list[train][3],self.train_list[train][7]))
			#print deptrain_value[train]

		for i in range(0, 5):
			self.deptrain_store[i][1] = self.deptrain_value[i]

	# Function to manipulate the track string
	def get_departure_track(self):
		self.track_value = []
		for track in range(self.start, self.end):
			self.track_value.append(self.train_list[track][4])

		for i in range(0, 5):
			self.deptrain_store[i][2] = self.track_value[i]

	# Function to display more results 
	def next_departure(self, button):
		if self.end+5 <= len(self.train_list):
			self.start = self.start + 5
			self.end = self.end + 5
			self.startpage = self.startpage + 1
			self.pagelabel.set_text("%s of %s" % (self.startpage, self.endpage))
			self.get_departure_train()
			self.get_departure_time()
			self.get_departure_track()
		else:
			print "[ERROR]: Exceeded maximum length of train_list"

	# Function to display previous results
	def prev_departure(self, button):
		if self.start-5 >= 0:
			self.start = self.start - 5
			self.end = self.end - 5
			self.startpage = self.startpage - 1
			self.pagelabel.set_text("%s of %s" % (self.startpage, self.endpage))
			self.get_departure_train()
			self.get_departure_time()
			self.get_departure_track()
		else:
			print "[ERROR]: Below zero index..."

	# Function to iniatilize xml related variables
	def departure_xml_init(self):
		self.list = []
		self.train_list = []

	# Function to get the xml file from the url
	def get_departure_xml(self, url):
		xmlfile = urllib2.urlopen(url)
		doc = xml.dom.minidom.parse(xmlfile)
		node = doc.documentElement
		return node

	# Function to handle the entire xml object
	def handle_departure_xml(self, xml):
		api_flag = 0
		try:
			trains = xml.getElementsByTagName("VertrekkendeTrein")
			if trains == []:
				print "[ERROR]: API ERROR - Cannot retrieve departure trains (EMPTY)"
				api_flag = 1
			else:
				self.handle_departure_trains(trains)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve departure trains"
			api_flag = 1

		if api_flag == 1:
			print "[ERROR]: API Error..failed at handle_departure_xml exception"

	# Function to read through every departing train object
	def handle_departure_trains(self, trains):
		self.train_list = []
		self.trainnumber_flag = 0
		self.traintype_flag = 0
		self.carrier_flag = 0
		for train in trains:
			self.handle_departure_train(train)
			self.list = []

	# Function to extract information from every departing train object
	def handle_departure_train(self, train):
		severe_api_flag = 0

		try:
			train_number = self.getElement(train.getElementsByTagName("RitNummer")[0])
			self.list.append(train_number)
		except:
			if self.trainnumber_flag == 0:
				print "[ERROR]: API ERROR - Cannot retrieve departure train number"
				self.trainnumber_flag = 1
			train_number = " "
			self.list.append(train_number)

		try:
			departure_time = self.getElement(train.getElementsByTagName("VertrekTijd")[0])
			self.list.append(departure_time)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve departure train time"
			severe_api_flag = 1
			departure_time = " "
			self.list.append(departure_time)

		try:
			final_destination = self.getElement(train.getElementsByTagName("EindBestemming")[0])
			self.list.append(final_destination)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve departure train final destination"
			severe_api_flag = 1
			final_destination = " "
			self.list.append(final_destination)
			
		try:
			train_type = self.getElement(train.getElementsByTagName("TreinSoort")[0])
			self.list.append(train_type)
		except:
			if self.traintype_flag == 0:
				print "[ERROR]: API ERROR - Cannot retrieve departure train train type"
				self.traintype_flag = 1
			train_type = " "
			self.list.append(train_type)
			
		try:
			train_platform = self.getElement(train.getElementsByTagName("VertrekSpoor")[0])
			self.list.append(train_platform)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve departure train platform"
			severe_api_flag = 1
			train_platform = " "
			self.list.append(train_platform)
			
		try:
			carrier = self.getElement(train.getElementsByTagName("Vervoerder")[0])
			self.list.append(carrier)
		except:
			if carrier_flag == 0:
				print "[ERROR]: API ERROR - Cannot retrieve departure train carrier"
				carrier_flag = 1
			carrier = " "
			self.list.append(carrier)

		try:
			delay_time = self.getElement(train.getElementsByTagName("VertrekVertragingTekst")[0])
			self.list.append(delay_time)
		except Exception, e:
			delay_time = "0"
			self.list.append(delay_time)

		try:
			via_station = self.getElement(train.getElementsByTagName("RouteTekst")[0])
			self.list.append(via_station)
		except Exception, e:
			via_station = "Information Not Available"
			self.list.append(via_station)

		try:
			tip = self.getElement(train.getElementsByTagName("ReisTip")[0])
			self.list.append(tip)
		except Exception, e:
			tip = "No Tip Available"
			self.list.append(tip)

		if severe_api_flag == 0:
			self.train_list.append(self.list)

	# Function to convert a xml object into a text which can be used
	def getElement(self, element):
		return self.getText(element.childNodes)

	def getText(self, nodelist):
		rc = ""
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc = rc + node.data
		return rc
