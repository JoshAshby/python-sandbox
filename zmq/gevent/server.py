import gevent
from gevent_zeromq import zmq
import signal

context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.bind("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "")

def server():
	while True:
		reply = zmqSock.recv()
		print reply

if __name__ == '__main__':
	gevent.signal(signal.SIGQUIT, gevent.shutdown)
	ser = gevent.spawn(server)
	ser.join()
