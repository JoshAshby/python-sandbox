#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main framework app

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
if serverType is "fastcgi":
	from gevent_fastcgi.server import WSGIServer
else:
	from gevent.pywsgi import WSGIServer
import signal


def app(env, start_response):
	global urls
	for url in urls:
		if serverType is "fastcgi":
			matched = url["regex"].match(env["REQUEST_URI"][4:].split("?")[0])
		else:
			matched = url["regex"].match(env["PATH_INFO"])
		if matched:
			newHTTPObject = url["object"](env, matched.groups())

			status, headers = newHTTPObject.response()

			start_response(status, headers)

			routes = {
				"GET": newHTTPObject.GET(),
				"POST": newHTTPObject.POST(),
				"PUT": newHTTPObject.PUT(),
				"DELETE": newHTTPObject.DELETE()
				}

			for data in routes[env["REQUEST_METHOD"]]:
				yield data
			break

		else:
			status = "404 NOT FOUND"

			headers = [
				("Content-Type", "text/html"),
			]

			try:
				start_response(status, headers)
			except AssertionError:
				pass

			yield "404 Resource Not Found"
			break


def main():
	gevent.signal(signal.SIGQUIT, gevent.shutdown)
	global port
	global address
	if port and type(port) is str:
		port = int(port)
	if not address:
		address = "127.0.0.1"
	try:
		server = WSGIServer((address, port), app)

		if serverType is "fastcgi":
			print ("Now serving py as a fastcgi server at %s:%i" % (address, port))
		else:
			print ("Now serving py at %s:%i" % (address, port))
		print "Press Ctrl+c or send SIGQUIT to stop"

		print "\r\nHeres some fancy URLs also:\n\r"

		print "  Url : Class Name"
		print "  -------------------------"
		for url in urls:
			print ("  %s : %s" % (url['url'], url["object"].__name__))
		
		if serverType is "fastcgi":
			print "\r\n\r\nNo logging of requests done here."
			print "Check your server logs instead."
		else:
			print "\r\n\r\nNow logging requests:"
			print "  Remote IP - - [YYYY-MM-DD HH:MM:SS] \"METHOD url HTTP/version\" Status code Something Request timing"
			print "------------------------------------------------------------------------------------------------------"

		server.serve_forever()
	except KeyboardInterrupt:
		gevent.shutdown
