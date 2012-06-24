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
	fw.main()
