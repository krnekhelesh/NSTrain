#! /usr/bin/env python

from gi.repository import Gtk
import os,sys

class TravelDetails:
	def __init__(self, builder4):

		self.window = builder4.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)

		# Travel Options
		self.traveloption_departuretime = []
		self.traveloption_departuretime.append(builder4.get_object('label1'))
		self.traveloption_departuretime.append(builder4.get_object('label5'))
		self.traveloption_departuretime.append(builder4.get_object('label9'))
		self.traveloption_departuretime.append(builder4.get_object('label13'))
		self.traveloption_departuretime.append(builder4.get_object('label17'))

		self.traveloption_arrivaltime = []
		self.traveloption_arrivaltime.append(builder4.get_object('label2'))
		self.traveloption_arrivaltime.append(builder4.get_object('label6'))
		self.traveloption_arrivaltime.append(builder4.get_object('label10'))
		self.traveloption_arrivaltime.append(builder4.get_object('label14'))
		self.traveloption_arrivaltime.append(builder4.get_object('label18'))

		self.traveloption_stops = []
		self.traveloption_stops.append(builder4.get_object('label3'))
		self.traveloption_stops.append(builder4.get_object('label7'))
		self.traveloption_stops.append(builder4.get_object('label11'))
		self.traveloption_stops.append(builder4.get_object('label15'))
		self.traveloption_stops.append(builder4.get_object('label19'))

		self.traveloption_traveltime = []
		self.traveloption_traveltime.append(builder4.get_object('label4'))
		self.traveloption_traveltime.append(builder4.get_object('label8'))
		self.traveloption_traveltime.append(builder4.get_object('label12'))
		self.traveloption_traveltime.append(builder4.get_object('label16'))
		self.traveloption_traveltime.append(builder4.get_object('label20'))
		
		self.travelstop_time0 = builder4.get_object('label21')
		self.travelstop_time1 = builder4.get_object('label25')
		self.travelstop_time2 = builder4.get_object('label29')

		self.travelstop_station0 = builder4.get_object('label22')
		self.travelstop_station1 = builder4.get_object('label26')
		self.travelstop_station2 = builder4.get_object('label30')

		self.travelstop_platform0 = builder4.get_object('label23')
		self.travelstop_platform1 = builder4.get_object('label27')
		self.travelstop_platform2 = builder4.get_object('label31')

		self.travelstop_traintype0 = builder4.get_object('label24')
		self.travelstop_traintype1 = builder4.get_object('label28')
		self.travelstop_traintype2 = builder4.get_object('label32')

		self.travelstop_warning = builder4.get_object('label38')

		self.size = len(self.traveloption_departuretime)

		self.title1 = builder4.get_object('label60')
		self.title2 = builder4.get_object('label61')
		self.pagelabel = builder4.get_object('label36')

		self.closebutton = builder4.get_object('button10')
		self.closebutton.connect("clicked", self.hide_window)

	# Function to display the current 5 travel options (on the left) after a bit of formatting
	def get_traveloption(self, travelplanner_list, start, startpage, endpage):
		self.pagelabel.set_text("%s of %s" % (startpage, endpage))

		for i in range(self.size):
			time_value1 = travelplanner_list[i+start][5].split('T')
			time_value2 = time_value1[1].split('+')
			time_value3 = time_value2[0].split(':')
			time = "%s:%s" % (time_value3[0], time_value3[1])
			
			if travelplanner_list[i+start][11] == "0":
				delay_text = ""
			else:
				delay_text = "%s" % travelplanner_list[i+start][11]
			
			if travelplanner_list[i+start][4] == "true":
				self.traveloption_departuretime[i].set_markup('''<span foreground="#5c5ce6e61f1f">%s</span> <span foreground="red">%s</span>''' % (time, delay_text))
			else:
				self.traveloption_departuretime[i].set_markup('''%s <span foreground="red">%s</span>''' % (time, delay_text))

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
				self.traveloption_arrivaltime[i].set_markup('''<span foreground="#5c5ce6e61f1f">%s</span> <span foreground="red">%s</span>''' % (time, delay_text))
			else:
				self.traveloption_arrivaltime[i].set_markup('''%s <span foreground="red">%s</span>''' % (time, delay_text))

		for i in range(self.size):
			if travelplanner_list[i+start][4] == "true":
				self.traveloption_traveltime[i].set_markup('''<span foreground="#5c5ce6e61f1f">%s</span>''' % travelplanner_list[i+start][2])
				self.traveloption_stops[i].set_markup('''<span foreground="#5c5ce6e61f1f">%s</span>''' % travelplanner_list[i+start][1])
			else:
				self.traveloption_traveltime[i].set_text(travelplanner_list[i+start][2])
				self.traveloption_stops[i].set_text(travelplanner_list[i+start][1])

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
			self.travelstop_time0.set_markup('''%s''' % time)
		else:
			delay_text = "%s" % travelplanner_list[index][11]
			self.travelstop_time0.set_markup('''%s <span foreground="red">%s</span>''' % (time, delay_text))

		time1_temp = travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][1].split('T')
		time2_temp = time1_temp[1].split('+')
		time3_temp = time2_temp[0].split(':')
		time = "%s:%s" % (time3_temp[0], time3_temp[1])
		if travelplanner_list[index][12] == "0":
			delay_text = ""
			self.travelstop_time2.set_markup('''%s''' % time)
		else:
			delay_text = "%s" % travelplanner_list[index][12]
			self.travelstop_time2.set_markup('''%s <span foreground="red">%s</span>''' % (time, delay_text))

		self.travelstop_station0.set_text(travelplanner_list[index][10][1][0][0])
		self.travelstop_station2.set_text(travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][0])

		self.travelstop_platform0.set_text(travelplanner_list[index][10][1][0][2])
		self.travelstop_platform2.set_text(travelplanner_list[index][10][reisdeel_size-1][len(travelplanner_list[index][10][reisdeel_size-1])-1][2])

		self.travelstop_traintype0.set_text(travelplanner_list[index][10][0][1])
		self.travelstop_traintype2.set_text(travelplanner_list[index][10][reisdeel_size-2][1])

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

		self.travelstop_station1.set_text(self.station1)
		self.travelstop_platform1.set_text(self.platform1)
		self.travelstop_time1.set_text(self.time1)
		self.travelstop_traintype1.set_text(self.traintype1)

	# Function to set the title, date and time which are shown at the top
	def set_traveloption_title(self, fromstation, tostation, year, month, day, hour, minute):
		self.title1.set_text(fromstation + ' -> ' + tostation)
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
