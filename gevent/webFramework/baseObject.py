#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys, os

try:
	from config import *
except:
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
	from config import *


class baseObject(object):
	def __init__(self, env, members):
		self.env = env
		self.members = members
	
	def response(self):
		status = "200 OK"

		headers = [
			("Content-type", "text/html"),
			]

		return status, headers

	def GET(self):
		pass

	def POST(self):
		pass

	def PUT(self):
		pass

	def DELETE(self):
		pass

	def endPolling(self):
		return ''



