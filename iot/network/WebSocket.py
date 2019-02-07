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
from OpenSSL import SSL
from twisted.internet import ssl
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from iot.classes.ConnectionState import *
import OpenSSL.crypto
import tempfile

class WebSocket(WebSocketClientProtocol):
   def __init__(self,factory,client):
        self.factory = factory
        self.client = client
        self.closeFlag = True

   def onConnect(self, response):
       print("Server connected")
       self.client.setState(ConnectionState.CONNECTION_ESTABLISHED)

   def onMessage(self, msg, binary):
      print("WebSocket Got echo: " + str(msg))
      self.client.dataReceived(msg)

   def sendPacket(self, message):
       print('WebSocket sendPacket ' + str(message))
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

class CtxFactory(ssl.ClientContextFactory):
    def __init__(self, certificate, password):
        self.certificate = certificate
        if password is not None and len(password)>0:
            self.password = password
        else:
            self.password = None

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        if self.certificate != '':
            fp = tempfile.NamedTemporaryFile()
            fp.write(bytes(self.certificate,'utf-8'))
            fp.seek(0)
            ctx.use_certificate_chain_file(fp.name)
            fp.seek(0)
            if self.password is not None:
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), self.password)
            else:
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read())
            ctx.use_privatekey(key)
            fp.close()
        return ctx