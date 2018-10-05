from venv.iot.mqttsn.mqttsn_messages.SNConnect import *
from venv.iot.network.UDPClient import *
from venv.iot.mqttsn.SNParser import *
from twisted.internet import reactor
import socket

host = socket.gethostbyname('broker.iotbroker.cloud')
udpClient = UDPClient(host,1883,None)
connector = reactor.listenUDP(0, udpClient)

parser = SNParser(None)
willPresent = True
cleanSession = False
duration = 128
clientID = 'mobius'
message = SNConnect(willPresent, cleanSession, duration, clientID)
parser.setMessage(message)
data = parser.encode()

udpClient.send(data)

reactor.run()