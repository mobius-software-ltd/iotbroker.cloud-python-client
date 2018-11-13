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
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

class TCPClient(Protocol):
    def __init__(self, message, client):
        self.message = message
        self.client = client

    def connectionMade(self):
        print("Server connected")
        try:
            self.transport.setTcpKeepAlive(1)
            self.sendMessage(self.message)
        except AttributeError:
            pass

    def dataReceived(self, data):
        #print("Server said:", data)
        self.client.dataReceived(data)

    def sendMessage(self, message):
        self.message = message
        try:
            self.transport.write(self.message)
            #print("was sended: " + str(self.message))
        except:
            print('TCPClient sending message ERROR')

    def connectionLost(self, reason):
        # connector.connect()
        print("connection lost")

    def connectionClose(self):
        reactor.stop()

    def getStatus(self):
        pass

class ClientFactory(ReconnectingClientFactory):
    def __init__(self, message, client):
        self.message = message
        self.client = client
        self.tcp = TCPClient(self.message, self.client)

    def send(self, message):
        self.message = message
        self.tcp.sendMessage(self.message)

    def buildProtocol(self, addr):
        print
        'Connected.'
        print
        'Resetting reconnection delay'
        #self.resetDelay()
        return self.tcp

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        #reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - reconnect!")
        #connector.connect()
        #reactor.stop()
