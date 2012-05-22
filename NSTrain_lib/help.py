#! /usr/bin/env python
import os

def get_help_uri(page=None):
	# help_uri from source tree - default language
	here = os.path.dirname(__file__)
	help_uri = os.path.abspath(os.path.join(here, '..','help', 'C'))
	if not os.path.exists(help_uri):
		print "[ERROR]: Help File not found"

	# unspecified page is the index.page
	if page is not None:
		help_uri = '%s#%s' % (help_uri, page)
	return help_uri

def show_uri(parent, link):
	from gi.repository import Gtk # pylint: disable=E0611
	Gtk.show_uri(None, link, 0)

# Dead Code
	#cmd = "yelp ghelp:/home/krnekhelesh/Python\ Apps/GitHub/NSTrain/help/C"
	#subprocess.Popen(cmd, shell=True) 
	#Gtk.show_uri(screen, link, Gtk.get_current_event_time())
