from venv.IoT.Classes.ConnectionState import *
from twisted.internet.protocol import DatagramProtocol
import socket

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

    def send(self, message):
        #print("we send: " + str(message))
        self.transport.write(message)  # no need for address

    def datagramReceived(self, data, addr):
        #print("received %r from %s:%d" % (data, self.host, self.port))
        self.client.dataReceived(data)

    def connectionRefused(self):
        print("No one listening on this port")