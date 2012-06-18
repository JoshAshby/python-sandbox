import zmq
import json

context = zmq.Context()
zmqSock = context.socket(zmq.PUB)
zmqSock.connect("tcp://127.0.0.1:5000")

data = [{"one": "test", 2: "test", "3": 6}]

msg = json.dumps(data)

for i in range(100):
	zmqSock.send("0" + msg)
