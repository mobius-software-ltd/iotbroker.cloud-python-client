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
        self.transport.write(self.message)
        #print("was sended: " + str(self.message))

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
        print
        'Started to connect.'

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        #reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - reconnect!")
        #connector.connect()
        #reactor.stop()
