#! /usr/bin/env python

from gi.repository import Gtk
from gi.repository.Gdk import Color
import os, sys
from xdg import BaseDirectory

UI_FILE = "data/ui/load_travel.ui"

class LoadTravelPlan:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('window1')
		self.window.set_position(Gtk.WindowPosition.CENTER)
		self.window.connect("delete-event", self.hide_window2)
		self.window.set_default_size(500,400)

		favourite_toolbar = self.builder.get_object('toolbar1')
		fav_context = favourite_toolbar.get_style_context()
		fav_context.add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)

		self.load = self.builder.get_object('toolbutton6')
		self.load.connect("clicked", self.setplandetails)

		self.fav_store = Gtk.ListStore(str, int)
		self.fav_tree = self.builder.get_object('treeview1')
		self.fav_tree.set_model(self.fav_store)

		self.favcolumn = Gtk.TreeViewColumn("Favourites", Gtk.CellRendererText(), markup=0)
		self.favcolumn.set_expand(True)

		self.favnum = Gtk.TreeViewColumn("Favourites", Gtk.CellRendererText(), text=1)
		self.favnum.set_visible(False)

		self.fav_tree.append_column(self.favcolumn)
		self.fav_tree.append_column(self.favnum)

		for i in range(0,5):
			self.fav_store.append(["", 0])

		self.name_entry = self.builder.get_object('entry1')

	def loadplan(self):
		self.read_temp = []
		i = 0
		
		self.read_favourite_plan_file = open(BaseDirectory.xdg_config_dirs[0] + "/NSTrain/favourite_plans", "r")
		self.read_fav = self.read_favourite_plan_file.readlines()
		self.read_favourite_plan_file.close()

		#read_temp.append(read_fav[0].split('|')[0])

		for i in range(len(self.read_fav)):
			self.read_temp.append(self.read_fav[i].split('|'))

		for i in range(len(self.read_temp)):
			if self.read_temp[i][3] != "INIT":
				self.fav_store[i][0] = ('''<span weight="bold">%s</span>
%s to %s
via %s''' % (self.read_temp[i][0], self.read_temp[i][1], self.read_temp[i][2], self.read_temp[i][3]))
			else:
				self.fav_store[i][0] = ('''<span weight="bold">%s</span>
%s to %s''' % (self.read_temp[i][0], self.read_temp[i][1], self.read_temp[i][2]))
			self.fav_store[i][1] = i			

	def setplandetails(self, button):
		selection = self.fav_tree.get_selection()
		selection.set_mode(Gtk.SelectionMode.BROWSE)
		plan_model, plan_iter = selection.get_selected()

		if plan_iter != None:
			row_index = plan_model[plan_iter][1]
			self.fromentry.set_text(self.read_temp[row_index][1])
			self.toentry.set_text(self.read_temp[row_index][2])
			if self.read_temp[row_index][3] != "INIT":
				self.viaentry.set_text(self.read_temp[row_index][3])
		self.window.hide()

	# GTK functions to show and hide the window intelligently
	def show_window2(self, fromentry, toentry, viaentry):
		self.fromentry = fromentry
		self.toentry = toentry
		self.viaentry = viaentry
		self.loadplan()
		self.window.show_all()

	def show_window(self, button):
		self.loadplan()
		self.window.show_all()

	# Function used by close button
	def hide_window(self, button):
		self.window.hide()

	# Function used by window close (x) button
	def hide_window2(self, window, event):
		self.window.hide()
		return True