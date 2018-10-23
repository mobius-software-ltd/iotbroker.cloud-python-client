import json
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from venv.iot.classes.ConnectionState import *

class WebSocket(WebSocketClientProtocol):
   def __init__(self,factory,client):
        self.factory = factory
        self.client = client
        self.closeFlag = True

   def onConnect(self, response):
       print("Server connected")
       self.client.setState(ConnectionState.CONNECTION_ESTABLISHED)

   def onMessage(self, msg, binary):
      #print("Got echo: " + str(msg))
      self.client.dataReceived(msg)

   def sendPacket(self, message):
       #print('HERE sendPacket ' + str(message))
       self.sendMessage(bytes(json.dumps(message),'utf-8'))

   def connectionLost(self, reason):
        self.client.setState(ConnectionState.CONNECTION_LOST)
        if self.closeFlag:
            self.client.goConnect()

class WSSocketClientFactory(WebSocketClientFactory):

    def __init__(self,url,client):
        WebSocketClientFactory.__init__(self,url)
        self.client = client
        self.ws = WebSocket(self, self.client)

    def buildProtocol(self, addr):
        return self.ws

    def sendPacket(self, packet):
        self.ws.sendPacket(packet)