import json
from twisted.internet import reactor
from iot.network.WebSocket import *
from autobahn.twisted.websocket import connectWS

url = 'ws://broker.iotbroker.cloud:18080/ws'

data = json.dumps({"packet":1,"protocolLevel":4,"username":"username","password":"password","clientID":"client1","cleanSession":True,"keepalive":30,"will":None,"willFlag":False,"passwordFlag":True,"usernameFlag":True,"protocolName":"MQTT","retain":True,"content":"dsfgdjnksd"})
print('encoded message= ' + str(data))

factory = WSSocketClientFactory(url, None)
connectWS(factory)

reactor.run()
