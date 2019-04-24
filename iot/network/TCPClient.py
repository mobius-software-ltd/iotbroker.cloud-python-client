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
try:
    import Tkinter.messagebox as messagebox
except:
    import tkinter.messagebox as messagebox

from OpenSSL import SSL
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import OpenSSL.crypto
import tempfile

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
            self.transport.write(bytes(self.message))
            #print("was sended: " + str(bytes(self.message)))
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
        print('Connected.')
        #self.resetDelay()
        return self.tcp

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionFailed(self, connector, reason):
        messagebox.showinfo("Warning", 'TCP connection failed')
        print("TCP connection failed - goodbye!")
        self.client.ConnectionLost()

    def clientConnectionLost(self, connector, reason):
        print("TCP connection lost - reconnect!")

        #self.client.ConnectionLost()
        #connector.connect()

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
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), self.password.encode("utf-8"))
            else:
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read())
            ctx.use_privatekey(key)
            fp.close()
        return ctx