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


def app(env, start_response):
	global urls
	for url in urls:
		matched = url['regex'].match(env["PATH_INFO"])
		if matched:
			status = '200 OK'

			headers = [
				('Content-Type', 'text/html')
			]

			start_response(status, headers)

			newHTTPObject = url["object"](env, start_response, matched.groups())
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
				('Content-Type', 'text/html')
			]

			start_response(status, headers)


