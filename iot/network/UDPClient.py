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
from iot.classes.ConnectionState import *
from twisted.internet.protocol import DatagramProtocol
import socket
from OpenSSL import SSL
from twisted.internet import ssl

class UDPClient(DatagramProtocol):
    def __init__(self, host, port, client):
        try:
            socket.inet_aton(host)
            self.host = host
        except socket.error:
            self.host = socket.gethostbyname(host)
        self.port = port
        self.client = client

    def startProtocol(self):
        self.transport.connect(self.host, self.port)
        print("connection to host %s port %d  was established" % (self.host, self.port))
        self.client.setState(ConnectionState.CONNECTION_ESTABLISHED)

    def sendMessage(self, message):
        print("we send: " + str(message))
        self.transport.write(message)

    def datagramReceived(self, data, addr):
        print("received %r from %s:%d" % (data, self.host, self.port))
        self.client.dataReceived(data)

    def connectionRefused(self):
        print("No one listening on this port")
