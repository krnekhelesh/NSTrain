#! /usr/bin/env python

from gi.repository import Gtk
import os,sys

TRAVEL_DETAILS_UI_FILE = "data/ui/traveldetails.ui"

class TravelDetails:
	def __init__(self):

		self.builder4 = Gtk.Builder()
		self.builder4.add_from_file(TRAVEL_DETAILS_UI_FILE)
		self.builder4.connect_signals(self)

		self.window = self.builder4.get_object('window1')
		self.window.set_size_request(850, 325)
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)

		toolbar = self.builder4.get_object('toolbar1')
		context = toolbar.get_style_context()
		context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

		self.start = 0
		self.end = 5
		self.startpage = 1
		self.endpage = 10
		self.local_travelplanner_list = []

		# Travel Option Store
		self.traveloption_store = Gtk.ListStore(str, str, str, str, int)		
		self.traveloption_tree = self.builder4.get_object('treeview2')		
		self.traveloption_tree.set_model(self.traveloption_store)

		self.departuretimecolumn = Gtk.TreeViewColumn(" Departure Time", Gtk.CellRendererText(), markup=0)
		self.departuretimecolumn.set_expand(True)
		self.departuretimecolumn.set_alignment(0.5)

		self.arrivaltimecolumn = Gtk.TreeViewColumn(" Arrival Time", Gtk.CellRendererText(), markup=1)
		self.arrivaltimecolumn.set_expand(True)
		self.arrivaltimecolumn.set_alignment(0.5)

		self.transfercolumn = Gtk.TreeViewColumn(" Transfers Time", Gtk.CellRendererText(), markup=2)
		self.transfercolumn.set_expand(True)
		self.transfercolumn.set_alignment(0.5)

		self.traveltimecolumn = Gtk.TreeViewColumn(" Travel Time", Gtk.CellRendererText(), markup=3)
		self.traveltimecolumn.set_expand(True)
		self.traveltimecolumn.set_alignment(0.5)

		self.rowcolumn = Gtk.TreeViewColumn(" Row Index ", Gtk.CellRendererText(), text=4)
		self.rowcolumn.set_visible(False)

		self.traveloption_tree.append_column(self.departuretimecolumn)
		self.traveloption_tree.append_column(self.arrivaltimecolumn)
		self.traveloption_tree.append_column(self.transfercolumn)
		self.traveloption_tree.append_column(self.traveltimecolumn)
		self.traveloption_tree.append_column(self.rowcolumn)

		for i in range(0, 5):
			self.traveloption_store.append(["Dep", "Arrival", "Transfer", "Travel", 0])
		
		# Travel Stop Store
		self.travelstop_store = Gtk.ListStore(str, str, str, str)
		self.travelstop_tree = self.builder4.get_object('treeview3')
		self.travelstop_tree.set_model(self.travelstop_store)

		self.timecolumn = Gtk.TreeViewColumn("Time", Gtk.CellRendererText(), markup=0)
		self.timecolumn.set_expand(True)
		self.timecolumn.set_alignment(0.5)

		self.stationcolumn = Gtk.TreeViewColumn("Station", Gtk.CellRendererText(), markup=1)
		self.stationcolumn.set_expand(True)
		self.stationcolumn.set_alignment(0.5)

		self.platformcolumn = Gtk.TreeViewColumn("Platform", Gtk.CellRendererText(), markup=2)
		self.platformcolumn.set_expand(True)
		self.platformcolumn.set_alignment(0.5)

		self.traintypecolumn = Gtk.TreeViewColumn("Train Type", Gtk.CellRendererText(), markup=3)
		self.traintypecolumn.set_expand(True)
		self.traintypecolumn.set_alignment(0.5)

		self.travelstop_tree.append_column(self.timecolumn)
		self.travelstop_tree.append_column(self.stationcolumn)
		self.travelstop_tree.append_column(self.platformcolumn)
		self.travelstop_tree.append_column(self.traintypecolumn)

		self.travelstop_selection = self.travelstop_tree.get_selection()
		self.travelstop_selection.set_mode(Gtk.SelectionMode.NONE)

		for i in range(0, 3):
			self.travelstop_store.append(["Time", "Station", "Platform", "TrainType"])

		self.travelstop_warning = self.builder4.get_object('label38')

		#self.size = len(self.traveloption_departuretime)
		self.size = 5

		self.title1 = self.builder4.get_object('label60')
		self.title2 = self.builder4.get_object('label61')
		self.pagelabel = self.builder4.get_object('label36')

		self.next_traveloption_button = self.builder4.get_object('toolbutton4')
		self.next_traveloption_button.connect("clicked", self.next_traveloption)
		self.prev_traveloption_button = self.builder4.get_object('toolbutton3')
		self.prev_traveloption_button.connect("clicked", self.prev_traveloption)

		self.closebutton = self.builder4.get_object('button10')
		self.closebutton.connect("clicked", self.hide_window)

	def final_traveloption(self, travelplanner_list, fromstation_name_entry, tostation_name_entry, year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry):
		self.start = 0
		self.end = 5
		self.startpage = 1
		self.local_travelplanner_list = list(travelplanner_list)
		self.endpage = len(self.local_travelplanner_list)/5
		self.set_traveloption_title(fromstation_name_entry, tostation_name_entry, year_name_entry, month_name_entry, day_name_entry, time_hour_name_entry, time_minute_name_entry)
		self.get_traveloption(self.local_travelplanner_list, self.start, self.startpage, self.endpage)
		self.show_window()

	# Function to display the currently chosen travel option
	def choose_traveloption(self, widget):
		selection = self.traveloption_tree.get_selection()
		selection.set_mode(Gtk.SelectionMode.BROWSE)
		traveloption_model, traveloption_iter = selection.get_selected()
		if traveloption_iter != None:
			button_number = traveloption_model[traveloption_iter][4]
			index  = button_number + self.start
			print "Option:%d Index:%d " % (button_number, index)
			self.get_travelstop(self.local_travelplanner_list, index)

	# Function to display the next 5 travel options
	def next_traveloption(self, button):
		if self.end+5 <= len(self.local_travelplanner_list):
			self.start = self.start + 5
			self.end = self.end + 5
			self.startpage = self.startpage + 1
			self.get_traveloption(self.local_travelplanner_list, self.start, self.startpage, self.endpage)
		else:
			print "[ERROR]: Exceeded maximum length of traveloption_list"

	# Function to display the previous 5 travel options
	def prev_traveloption(self, button):
		if self.start-5 >= 0:
			self.start = self.start - 5
			self.end = self.end - 5
			self.startpage = self.startpage - 1
			self.get_traveloption(self.local_travelplanner_list, self.start, self.startpage, self.endpage)
		else:
			print "[ERROR]: Below zero index..."

	# Function to display the current 5 travel options (on the left) after a bit of formatting
	def get_traveloption(self, travelplanner_list, start, startpage, endpage):
		self.pagelabel.set_text("%s of %s" % (startpage, endpage))

		for i in range(self.size):
			self.traveloption_store[i][4] = i
			time_value1 = travelplanner_list[i+start][5].split('T')
			time_value2 = time_value1[1].split('+')
			time_value3 = time_value2[0].split(':')
			time = "%s:%s" % (time_value3[0], time_value3[1])
			
			if travelplanner_list[i+start][11] == "0":
				delay_text = ""
			else:
				delay_text = "%s" % travelplanner_list[i+start][11]
			
			if travelplanner_list[i+start][4] == "true":
				self.traveloption_store[i][0] = '''<span foreground="#5c5ce6e61f1f">%s</span> <span foreground="red">%s</span>''' % (time, delay_text)
			else:
				self.traveloption_store[i][0] = '''%s <span foreground="red">%s</span>''' % (time, delay_text)

		for i in range(self.size):
			time_value1 = travelplanner_list[i+start][7].split('T')
			time_value2 = time_value1[1].split('+')
			time_value3 = time_value2[0].split(':')
			time = "%s:%s" % (time_value3[0], time_value3[1])
			
			if travelplanner_list[i+start][12] == "0":
				delay_text = ""
			else:
				delay_text = "%s" % travelplanner_list[i+start][12]
			
			if travelplanner_list[i+start][4] == "true":
				self.traveloption_store[i][1] = '''<span foreground="#5c5ce6e61f1f">%s</span> <span foreground="red">%s</span>''' % (time, delay_text)
			else:
				self.traveloption_store[i][1] = '''%s <span foreground="red">%s</span>''' % (time, delay_text)

		for i in range(self.size):
			if travelplanner_list[i+start][4] == "true":
				self.traveloption_store[i][3] = '''<span foreground="#5c5ce6e61f1f">%s</span>''' % travelplanner_list[i+start][2]
				self.traveloption_store[i][2] = '''<span foreground="#5c5ce6e61f1f">%s</span>''' % travelplanner_list[i+start][1]
			else:
				self.traveloption_store[i][3] = travelplanner_list[i+start][2]
				self.traveloption_store[i][2] = travelplanner_list[i+start][1]

	# Function to display the travel stosp of the current travel option after a bit of formatting
	def get_travelstop(self, travelplanner_list, index):
		reisdeel_size = len(travelplanner_list[index][10])
		self.station1 = ""
		self.platform1 = ""
		self.time1 = ""
		self.traintype1 = ""

		if travelplanner_list[index][0] != []:
			self.travelstop_warning.set_text(travelplanner_list[index][0][0][2])
		else:
			self.travelstop_warning.set_text("")

		time1_temp = travelplanner_list[index][10][1][0][1].split('T')
		time2_temp = time1_temp[1].split('+')
		time3_temp = time2_temp[0].split(':')
		time = "%s:%s" % (time3_temp[0], time3_temp[1])
		if travelplanner_list[index][11] == "0":
			delay_text = ""
			self.travelstop_store[0][0] = '''%s''' % time
		else:
			delay_text = "%s" % travelplanner_list[index][11]
			self.travelstop_store[0][0] = '''%s <span foreground="red">%s</span>''' % (time, delay_text)

		time1_temp = travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][1].split('T')
		time2_temp = time1_temp[1].split('+')
		time3_temp = time2_temp[0].split(':')
		time = "%s:%s" % (time3_temp[0], time3_temp[1])
		if travelplanner_list[index][12] == "0":
			delay_text = ""
			self.travelstop_store[2][0] = '''%s''' % time
		else:
			delay_text = "%s" % travelplanner_list[index][12]
			self.travelstop_store[2][0] = '''%s <span foreground="red">%s</span>''' % (time, delay_text)

		self.travelstop_store[0][1] = travelplanner_list[index][10][1][0][0]
		self.travelstop_store[2][1] = travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][0]

		self.travelstop_store[0][2] = travelplanner_list[index][10][1][0][2]
		self.travelstop_store[2][2] = travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][2]

		self.travelstop_store[0][3] = travelplanner_list[index][10][0][1]
		self.travelstop_store[2][3] = travelplanner_list[index][10][reisdeel_size-2][1]

		for i in range(reisdeel_size):
			if i % 2 == 1:
				for j in range(len(travelplanner_list[index][10][i])):
					if i == 1 and j == 0:
						pass
					else:
						if i == reisdeel_size-1 and j == len(travelplanner_list[index][10][reisdeel_size-1])-1:
							pass
						else:
							self.station1 = self.station1 + "\n" + travelplanner_list[index][10][i][j][0] + "\n"
							self.platform1 = self.platform1 + "\n" + travelplanner_list[index][10][i][j][2] + "\n"
							time1_temp = travelplanner_list[index][10][i][j][1].split('T')
							time2_temp = time1_temp[1].split('+')
							time3_temp = time2_temp[0].split(':')
							time = "%s:%s" % (time3_temp[0], time3_temp[1])
							self.time1 = self.time1 + "\n" + time + "\n"
							self.traintype1 = self.traintype1 + "\n" + "\n"
			else:
				if i == 0:
					pass
				else:
					self.traintype1 = self.traintype1 + travelplanner_list[index][10][i][1]
		
		self.travelstop_store[1][1] = self.station1
		self.travelstop_store[1][2] = self.platform1
		self.travelstop_store[1][0] = self.time1
		self.travelstop_store[1][3] = self.traintype1

	# Function to set the title, date and time which are shown at the top
	def set_traveloption_title(self, fromstation, tostation, year, month, day, hour, minute):
		self.title1.set_text(fromstation + " to " + tostation)
		if hour < 10:
			hour = "0%s" % hour
		if minute < 10:
			minute = "0%s" % minute
		self.title2.set_text("%s-%s-%s, %s:%s" % (year, month, day, hour, minute))

	# GTK functions to show and hide the window intelligently
	def show_window(self):
		self.window.show_all()

	def hide_window(self, button):
		self.window.hide()

	def hide_window2(self, window, event):
		self.window.hide()
		return True
