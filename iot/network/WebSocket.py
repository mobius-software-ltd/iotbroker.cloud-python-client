"""
 # Mobius Software LTD
 # Copyright 2015-2018, Mobius Software LTD
 #
 # This is free software; you can redistribute it and/or modify it
 # under the terms of the GNU Lesser General Public License as
 # published by the Free Software Foundation; either version 2.1 of
 # the License, or (at your option) any later version.
 #
 # This software is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this software; if not, write to the Free
 # Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 # 02110-1301 USA, or see the FSF site: http://www.fsf.org.
"""
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