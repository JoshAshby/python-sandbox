import zmq
import redis
import json

context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.bind("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "0")

redisServer = redis.Redis("localhost")

i = 0

while True:
	reply = zmqSock.recv()
	keys = redisServer.keys()
	if keys != []:
		for i in range(len(keys)):
			keys[i] = int(keys[i])
		i = max(keys) + 1
	else:
		i = 0
	reply = json.loads(reply[1:])
	reply.append(i)
	reply = json.dumps(reply)
	redisServer.set(i, reply)
