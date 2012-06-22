import gevent
import signal
import urlparse
import re
from gevent.pywsgi import WSGIServer

urls = {}

def route(routeURL):
	routeURL = re.compile("^" + routeURL + "$")
	def wrapper(HTTPObject):
		global urls
		urls.update({routeURL: HTTPObject})

		return HTTPObject
	return wrapper


def app(env, start_response):
	for url in urls:
		matched = url.match(env["PATH_INFO"])
		if matched:
			status = '200 OK'

			headers = [
				('Content-Type', 'text/html')
			]

			start_response(status, headers)

			newHTTPObject =  urls[url](env, start_response, matched.groups())
			routes = {
				"GET": newHTTPObject.GET(),
				"POST": newHTTPObject.POST(),
				"PUT": newHTTPObject.PUT(),
				"DELETE": newHTTPObject.DELETE()
				}

			yield routes[env["REQUEST_METHOD"]]
			break
		else:
			status = "404 NOT FOUND"

			headers = [
				('Content-Type', 'text/html')
			]

			start_response(status, headers)

class baseObject(object):
	def __init__(self, env, start_response, matched):
		self.env = env
		self.start_response = start_response
		self.members = matched

	def GET(self):
		pass

	def POST(self):
		pass

	def PUT(self):
		pass

	def DELETE(self):
		pass


@route("/")
class test(baseObject):
	def GET(self):
		self.data = ''

		for bit in self.env:
			self.data += ("%s : %s<br>" % (str(bit), str(self.env[bit])))

		return self.data


@route("/josh/")
class test(baseObject):
	def GET(self):
		self.data = ''

		for bit in self.env:
			self.data += ("%s : %s" % (str(bit), str(self.env[bit])))

		return self.data


@route("/josh/(.*)/")
class test(baseObject):
	def GET(self):
		self.data = ''

		for member in self.members:
			self.data += ("<h1>%s</h1>" % str(member))

		for bit in self.env:
			self.data += ("%s : %s" % (str(bit), str(self.env[bit])))

		return self.data


if __name__ == '__main__':
	gevent.signal(signal.SIGQUIT, gevent.shutdown)
	try:
		WSGIServer(('', 8000), app).serve_forever()
	except KeyboardInterrupt:
		gevent.shutdown
