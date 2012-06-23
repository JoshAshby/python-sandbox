#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main index file.

For more information, see: https://github.com/JoshAshby/

**WARNING**
Make sure you look through and change things in config.py
before running this file, to be sure it runs the way you want it to

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

import gevent
from gevent.pywsgi import WSGIServer
import signal
import framework as fw
import baseObject as bo
from route import *


@route("/")
class index(bo.baseObject):
	def GET(self):
		for i in range(1,101):
			yield ("%i<br>" % i)

		yield self.endPolling()


@route("/josh/")
class josh(bo.baseObject):
	def GET(self):
		self.data = ''

		for bit in self.env:
			self.data += ("%s : %s<br>" % (str(bit), str(self.env[bit])))

		yield self.data
		yield self.endPolling()


@route("/josh/(.*)/")
class joshMember(bo.baseObject):
	def GET(self):
		self.data = ''

		for member in self.members:
			self.data += ("<h1>%s</h1>" % str(member))

		for bit in self.env:
			self.data += ("%s : %s" % (str(bit), str(self.env[bit])))

		yield self.data
		yield self.endPolling()


if __name__ == '__main__':
	gevent.signal(signal.SIGQUIT, gevent.shutdown)
	if type(port) is str:
		port = int(port)
	if not address:
		address = '127.0.0.1'
	try:
		server = WSGIServer((address, port), fw.app)

		print ("Now serving py at %s:%i" % (address, port))
		print "Press Ctrl+c or send SIGQUIT to stop"

		print "\r\nHeres some fancy URLs also:\n\r"

		print "  Url : Class Name"
		print "  -------------------------"
		for url in urls:
			print ("  %s : %s" % (url['url'], url["object"].__name__))

		print "\r\n\r\nNow logging requests:"
		print "  Remote IP - - [YYYY-MM-DD HH:MM:SS] \"METHOD url HTTP/version\" Status code Something Request timing"
		print "------------------------------------------------------------------------------------------------------"

		server.serve_forever()
	except KeyboardInterrupt:
		gevent.shutdown
