from iot.classes.ConnectionState import *
import tempfile
import ssl
from socket import socket, AF_INET, SOCK_DGRAM
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch
do_patch()

class pyDTLSClient:
    def __init__(self, host, port, certificate, client, loop):
        self.loop = loop
        self.host = host
        self.port = port
        self.certificate = certificate
        self.client = client
        self.transport = None
        self.on_con_lost = loop.create_future()

    def connection_made(self, transport):
        self.transport = transport
        print("connection to host %s port %d  was established" % (self.host, self.port))

    def datagram_received(self, data, addr):
        self.datagramReceived(data, addr)

    def datagramReceived(self, data, addr):
        print("received %r from %s:%d" % (data, self.host, self.port))
        self.client.dataReceived(data)

    def sendMessage(self, message):
        print("we send: " + str(message))
        addr = (self.host, self.port)
        self.transport.sendto(bytes(message), addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Connection closed")
        #self.loop.stop()
        self.on_con_lost.set_result(True)