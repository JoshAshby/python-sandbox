import gevent
from gevent_zeromq import zmq
import signal

context = zmq.Context()
zmqSock = context.socket(zmq.PUB)
zmqSock.connect("tcp://127.0.0.1:5000")

def client():
	for i in range(1, 101):
		zmqSock.send(str(i))

if __name__ == '__main__':
	gevent.signal(signal.SIGQUIT, gevent.shutdown)
	cli = gevent.spawn(client)
	cli.join()
