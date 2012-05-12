#! /usr/bin/env python

from gi.repository import Gtk

class Dialog(Gtk.Window):
	def error_dialog(self, dialog_title, dialog_text, dialog_secondary_text):
		errordialog = dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, dialog_text)
		errordialog.format_secondary_markup(dialog_secondary_text)
		errordialog.set_title("NSTrain - " + dialog_title)
		response = errordialog.run()
		if response == Gtk.ResponseType.CLOSE:
			errordialog.destroy()
		
	def info_dialog(self, dialog_title, dialog_text, dialog_secondary_text):
		infodialog = dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, dialog_text)
		infodialog.format_secondary_markup(dialog_secondary_text)
		infodialog.set_title("NSTrain - " + dialog_title)
		response = infodialog.run()
		if response == Gtk.ResponseType.CLOSE:
			infodialog.destroy()
