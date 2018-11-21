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
from venv.iot.classes.ConnectionState import *
import socket
import OpenSSL
from OpenSSL import SSL
from OpenSSL._util import (
    ffi as _ffi,
    lib as _lib)


class DTLSClient(object):
    def __init__(self, host, port, path, client):
        try:
            socket.inet_aton(host)
            self.host = host
        except socket.error:
            self.host = socket.gethostbyname(host)
        self.port = port
        self.client = client
        self.path = path
        self.sock = None

    def startProtocol(self):
        DTLSv1_METHOD = 7
        #DTLSv1_2_METHOD = 8
        SSL.Context._methods[DTLSv1_METHOD] = getattr(_lib, "DTLSv1_client_method")
        ctx = SSL.Context(DTLSv1_METHOD)
        ctx.set_cipher_list('ALL:COMPLEMENTOFALL')

        if self.path != '':
            ctx.use_certificate_chain_file(self.path)
            ctx.use_privatekey_file(self.path)
        self.sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        addr = (self.host, self.port)
        self.sock.connect(addr)

        try:
            self.sock.do_handshake()
        except OpenSSL.SSL.WantReadError:
            print("HANDSHAKE ERROR")

        print("connection to host %s port %d  was established" % (self.host, self.port))
        self.client.setState(ConnectionState.CONNECTION_ESTABLISHED)

        while 1:
            print('in while loop')
            data = self.sock.recv(4048)
            if data and len(data)>0:
                self.datagramReceived(data, addr)

        self.connectionClosed()


    def send(self, message):
        print("we send: " + str(message))
        self.sock.send(bytes(message))  # no need for address

    def datagramReceived(self, data, addr):
        print("received %r from %s:%d" % (data, self.host, self.port))
        self.client.dataReceived(data)

    def connectionClosed(self):
        print("Connection closed")
        self.sock.close()
