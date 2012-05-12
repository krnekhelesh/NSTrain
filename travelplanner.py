#! /usr/bin/env python

import os, sys
import urllib2
import xml.dom.minidom

class TravelPlanner:
	def __init__(self):
		try:
			self.authenticate_developer_api()
		except Exception, e:
			print "[ERROR]: HTTP Error! Travel Planner Authentication failed!"
			
		self.travelplanner_xml_init()
		self.travelplanner_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=DT&toStation=UT'
		travelplanner_xml = self.get_travelplanner_xml(self.travelplanner_url)
		self.handle_departure_xml(travelplanner_xml)
		print self.travelplanner_list[0]

	def authenticate_developer_api(self):
		print "[INFO] : Retrieving Travel Planner - Authentication iniatiated.."
		self.theurl = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=DT&toStation=UT'
		self.username = 'krnekhelesh@gmail.com'
		self.password = 'RaLy9GRBjePqDKTrVt76YmDBuw_r043HwXUe-P4i6xwXmRR8SYz1cg'

		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		# this creates a password manager
		passman.add_password(None, self.theurl, self.username, self.password)
		# because we have put None at the start it will always
		# use this username/password combination for  urls
		# for which `theurl` is a super-url

		authhandler = urllib2.HTTPBasicAuthHandler(passman)
		# create the AuthHandler

		opener = urllib2.build_opener(authhandler)

		urllib2.install_opener(opener)
		# All calls to urllib2.urlopen will now use our handler
		# Make sure not to include the protocol in with the URL, or
		# HTTPPasswordMgrWithDefaultRealm will be very confused.
		# You must (of course) use it when fetching the page though.

		pagehandle = urllib2.urlopen(self.theurl)
		# authentication is now handled automatically for us

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
		print "[DEBUG]: url is %s" % (url)
		xmlfile = urllib2.urlopen(url)
		doc = xml.dom.minidom.parse(xmlfile)
		node = doc.documentElement
		return node

		# Function to handle the entire xml object
	def handle_departure_xml(self, xml):
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
			sys.exit(0)

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
			no_of_transfer = "0"
			self.list.append(no_of_transfers)

		try:
			planned_traveltime = self.getElement(traveloption.getElementsByTagName("GeplandeReisTijd")[0])
			self.list.append(planned_traveltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned travel time"
			planned_traveltime = "0"
			self.list.append(planned_traveltime)

		try:
			actual_traveltime = self.getElement(traveloption.getElementsByTagName("ActueleReisTijd")[0])
			self.list.append(actual_traveltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual travel time"
			actual_traveltime = "0"
			self.list.append(actual_traveltime)

		try:
			optimum = self.getElement(traveloption.getElementsByTagName("Optimaal")[0])
			self.list.append(optimum)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve optimum status"
			optimum = "0"
			self.list.append(optimum)

		try:
			planned_departuretime = self.getElement(traveloption.getElementsByTagName("GeplandeVertrekTijd")[0])
			self.list.append(planned_departuretime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned departure time"
			planned_departuretime = "0"
			self.list.append(planned_departuretime)

		try:
			actual_departuretime = self.getElement(traveloption.getElementsByTagName("ActueleVertrekTijd")[0])
			self.list.append(actual_departuretime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual departure time"
			actual_departuretime = "0"
			self.list.append(actual_departuretime)

		try:
			planned_arrivaltime = self.getElement(traveloption.getElementsByTagName("GeplandeAankomstTijd")[0])
			self.list.append(planned_arrivaltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve planned arrival time"
			planned_arrivaltime = "0"
			self.list.append(planned_arrivaltime)

		try:
			actual_arrivaltime = self.getElement(traveloption.getElementsByTagName("ActueleAankomstTijd")[0])
			self.list.append(actual_arrivaltime)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve actual arrival time"
			actual_arrivaltime = "0"
			self.list.append(actual_arrivaltime)

		try:
			status = self.getElement(traveloption.getElementsByTagName("Status")[0])
			self.list.append(status)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve status"
			status = "0"
			self.list.append(status)

		self.handle_travelplanner_travelsections(traveloption)
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
			print "I am so dead"

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
			melding_message = "0"
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
			train_carrier = "0"
			self.reisdeeltemp.append(train_carrier)

		try:
			train_type = self.getElement(travelsection.getElementsByTagName("VervoerType")[0])
			self.reisdeeltemp.append(train_type)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_type (REISDEEL)"
			train_type = "0"
			self.reisdeeltemp.append(train_type)

		try:
			train_number = self.getElement(travelsection.getElementsByTagName("RitNummer")[0])
			self.reisdeeltemp.append(train_number)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve train_number (REISDEEL)"
			train_number = "0"
			self.reisdeeltemp.append(train_number)

		try:
			trainstatus = self.getElement(travelsection.getElementsByTagName("Status")[0])
			self.reisdeeltemp.append(trainstatus)
		except:
			print "[ERROR]: API ERROR - Cannot retrieve status"
			trainstatus = "0"
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
			train_platform = "Not Available"
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
def main():
	app = TravelPlanner()
	#Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
