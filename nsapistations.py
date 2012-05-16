#! /usr/bin/env python

from gi.repository import Gtk
import os, sys
import urllib2
import xml.dom.minidom

from dialog import Dialog

class NsApiStations:
	def __init__(self):
		try:
			self.authenticate_developer_api()
		except Exception, e:
			print "[ERROR]: HTTP Error! NS API Stations Authentication failed!"
			show_dialog = Dialog()
			show_dialog.error_dialog("Oops!","HTTP Error 400", '''Unfortunately we have hit a snag. Either your internet or the website ns.nl seems
down. Please try again later. The program will now exit.

<span style="italic">Error Info: NS API Stations Access Error.</span>''')
			sys.exit(0)

		self.api_stations_xml_init()
		self.station_url = 'http://webservices.ns.nl/ns-api-stations'
		self.station_xml = self.get_station_xml(self.station_url)
		self.handle_station_xml(self.station_xml)

	# Function to authenticate the developer API
	def authenticate_developer_api(self):
		try:
			print "[INFO] : Retrieving Station List - Authentication iniatiated.."
			self.theurl = 'http://webservices.ns.nl'
			self.username = 'krnekhelesh@gmail.com'
			self.password = 'RaLy9GRBjePqDKTrVt76YmDBuw_r043HwXUe-P4i6xwXmRR8SYz1cg'

			passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		except:
			print "Fail Point 1"
		# this creates a password manager
		try:
			passman.add_password(None, self.theurl, self.username, self.password)
		except:
			print "Fail Point 2"
		# because we have put None at the start it will always
		# use this username/password combination for  urls
		# for which `theurl` is a super-url
		
		try:
			authhandler = urllib2.HTTPBasicAuthHandler(passman)
		except:
			print "Fail Point 3"
		# create the AuthHandler
		try:
			opener = urllib2.build_opener(authhandler)
		except: 
			print "Fail Point 4"

		try:
			urllib2.install_opener(opener)
		except:
			print "Fail Point 5"
		# All calls to urllib2.urlopen will now use our handler
		# Make sure not to include the protocol in with the URL, or
		# HTTPPasswordMgrWithDefaultRealm will be very confused.
		# You must (of course) use it when fetching the page though.

		pagehandle = urllib2.urlopen(self.theurl + '/ns-api-stations')
		# authentication is now handled automatically for us

	# Function to iniatilize xml related variables
	def api_stations_xml_init(self):
		self.list = []
		self.station_list = []
		
	# Function to get the xml file from the url
	def get_station_xml(self, url):
		print "[DEBUG]: url is %s" % (url)
		xmlfile = urllib2.urlopen(url)
		doc = xml.dom.minidom.parse(xmlfile)
		node = doc.documentElement
		return node
		
	# Function to handle the entire xml object
	def handle_station_xml(self, xml):
		try:
			stations = xml.getElementsByTagName("station")
			if stations == []:
				print "[ERROR]: API ERROR - Cannot retrieve stations (EMPTY)"
			else:
				self.handle_api_stations(stations)
		except:
			print "[ERROR]: API Error - Cannot retrieve stations"
	
	# Function to read through every api station object
	def handle_api_stations(self, stations):
		for station in stations:
			self.handle_api_station(station)
			self.list = []

	# Function to extract information from every api station object
	def handle_api_station(self, train):
		api_flag = 0
		try:
			station_name = self.getElement(train.getElementsByTagName("name")[0])
			self.list.append(station_name)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve station names"
			api_flag = 1
		
		try:
			station_code = self.getElement(train.getElementsByTagName("code")[0])
			self.list.append(station_code)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve station codes"
			api_flag = 1

		if api_flag == 0:
			self.station_list.append(self.list)
		
	# Function to convert a xml object into a text which can be used
	def getElement(self, element):
		return self.getText(element.childNodes)

	def getText(self, nodelist):
		rc = ""
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc = rc + node.data
		return rc
