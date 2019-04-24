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
from iot.network.UDPClient import *
from iot.network.pyDTLSClient import *
from iot.classes.IoTClient import *
from iot.coap.CoapParser import *
from iot.coap.options.CoapOptionType import *
from iot.coap.options.OptionParser import *
from iot.timers.TimersMap import *
from iot.coap.tlv.CoapTopic import *
from twisted.internet import reactor

import asyncio
import tempfile
import ssl
from socket import socket, AF_INET, SOCK_DGRAM
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch, wrapper
do_patch()
from threading import Thread

class CoapClient(IoTClient):
    def __init__(self, account, client):
        self.account = account
        self.clientGUI = client
        self.parser = CoapParser()
        self.parserOption = OptionParser()
        self.resendperiod = 3000
        self.connectionState = None
        self.data = None
        self.udpClient = None
        self.timers = TimersMap(self)
        self.Version = 1
        self.forPublish = {}
        self.forSubscribe = {}
        self.forUnsubscribe = {}
        self.pingNum = 0
        self.udpThread = None

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)

        duration = self.account.keepAlive

        if self.timers is not None:
            self.timers.stopAllTimers()

        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options = []
        options.append(option)
        message = CoapMessage(self.Version,CoapType.CONFIRMABLE,CoapCode.PUT,0,None,options,None)

        if self.account.isSecure:
            self.loop = asyncio.get_event_loop()

            fp = tempfile.NamedTemporaryFile()
            fp.write(bytes(self.account.certificate, 'utf-8'))
            fp.seek(0)
            sock_wrapped = wrapper.wrap_client(socket(AF_INET, SOCK_DGRAM), keyfile=fp.name, certfile=fp.name,
                                               ca_certs=fp.name)
            addr = (self.account.serverHost, self.account.port)
            sock_wrapped.connect(addr)
            connect = self.loop.create_datagram_endpoint(
                lambda: pyDTLSClient(self.account.serverHost, self.account.port, self.account.certificate, self,
                                     self.loop), sock=sock_wrapped)
            fp.close()
            transport, protocol = self.loop.run_until_complete(connect)
            self.udpClient = protocol
            self.setState(ConnectionState.CONNECTION_ESTABLISHED)
        else:
            self.udpClient = UDPClient(self.account.serverHost, self.account.port, self)
            reactor.listenUDP(0, self.udpClient)

        if self.account.isSecure:
            self.udpThread = Thread(target=self.loop.run_forever)
            self.udpThread.daemon = True
            self.udpThread.start()
        self.timers.goPingTimer(message, duration)

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            message = self.parser.encode(message)
            self.udpClient.sendMessage(message)
        else:
            return False

    def dataReceived(self, data):
        message = self.parser.decode(data)
        type = message.getType()
        code = message.getCode()
        if (code == CoapCode.POST or code == CoapCode.PUT) and type != CoapType.ACKNOWLEDGEMENT:
            topic = None
            qosValue = None
            for option in message.getOptionsDecode():
                if isinstance(option, CoapOption):
                    if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                        topic = self.parserOption.decode(CoapOptionType(option.getType()),option)
                        break
            for option in message.getOptionsDecode():
                if isinstance(option, CoapOption):
                    if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                        qosValue = self.parserOption.decode(CoapOptionType(option.getType()),option)
                        break
            if len(topic) > 0:
                content = message.getPayload()
                qos = QoS(qosValue)
                topicResult = CoapTopic(topic, qos)
                reactor.callFromThread(self.clientGUI.publishReceived, topicResult, qos, content, False, False)
            else:
                textFormat = "text/plain"
                options = []
                option = self.parserOption.encode(CoapOptionType.CONTENT_FORMAT, textFormat)
                options.append(option)
                option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
                options.append(option)
                ack = CoapMessage(self.Version,CoapType.ACKNOWLEDGEMENT,CoapCode.BAD_OPTION,message.getPacketID(),message.getToken(),options,None)
                self.send(ack)
        process_messageType_method(self, message.getType().value, message)

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def getConnectionState(self):
        return self.connectionState

    def publish(self, topicName, qosValue, content, retain, dup):
        options = []
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, qosValue)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.PUT, 0, '0', options, content)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forPublish[packetID] = message

    def subscribeTo(self,topicName, qosValue):
        options = []
        option = self.parserOption.encode(CoapOptionType.OBSERVE, 0)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, qosValue)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.GET, 0, '0', options, None)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forSubscribe[packetID] = message

    def unsubscribeFrom(self, topicName):
        options = []
        option = self.parserOption.encode(CoapOptionType.OBSERVE, 1)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, 0)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.GET, 0, '0', options, None)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forUnsubscribe[packetID] = message

    def pingreq(self):
        reactor.callFromThread(self.clientGUI.connackReceived, None)

    def disconnectWith(self, duration):
        self.timers.stopAllTimers()

    def timeoutMethod(self):
        self.timers.stopAllTimers()
        reactor.callFromThread(self.clientGUI.timeout)

    def ConnectionLost(self):
        self.setState(ConnectionState.CONNECTION_LOST)

    def connected(self):
        self.setState(ConnectionState.CHANNEL_ESTABLISHED)

    def connectFailed(self):
        self.setState(ConnectionState.CHANNEL_FAILED)

#__________________________________________________________________________________________

def CONFIRMABLE(self,message):
    if isinstance(message,CoapMessage):
        options = []
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        ack = CoapMessage(self.Version,CoapType.ACKNOWLEDGEMENT,message.getCode(),message.getPacketID(),message.getToken(),options,None)
        self.send(ack)

def NONCONFIRMABLE(self,message):
    if isinstance(message, CoapMessage):
        self.timers.removeTimer(int(message.getToken()))

def ACKNOWLEDGEMENT(self,message):
    if isinstance(message, CoapMessage):
        ack = None
        topic = None
        qosValue = None
        if message.getToken() is not None:
            ack = self.timers.removeTimer(int(message.getToken()))
            if message.getCode() == CoapCode.CONTENT:
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                            topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                            qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                if len(topic) > 0:
                    content = message.getPayload()
                    qos = QoS(qosValue)
                    topicResult = CoapTopic(topic, qos)
                    reactor.callFromThread(self.clientGUI.publishReceived, topicResult, qos, content, False, False)
        if ack is not None:
            if isinstance(ack,CoapMessage):
                if ack.getCode() == CoapCode.GET:
                    observeValue = None
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.OBSERVE:
                                observeValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                                topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                                qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    if observeValue == 0:
                        qos = QoS(qosValue)
                        reactor.callFromThread(self.clientGUI.subackReceived, topic, qos, 0)
                    elif observeValue == 1:
                        list = []
                        list.append(topic)
                        reactor.callFromThread(self.clientGUI.unsubackReceived, list)
                elif ack.getCode() == CoapCode.PUT:
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                                topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                                qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    content = ack.getPayload()
                    qos = QoS(qosValue)
                    topicResult = CoapTopic(topic, qos)
                    reactor.callFromThread(self.clientGUI.pubackReceived, topicResult, qos, content, False, False, 0)
        else:
            if self.pingNum == 0:
                self.pingNum +=1
                reactor.callFromThread(self.clientGUI.pingrespReceived, True)

def RESET(self,message):
    if isinstance(message, CoapMessage):
        self.timers.removeTimer(int(message.getToken()))

switcherProcess = {
    0: CONFIRMABLE,
    1: NONCONFIRMABLE,
    2: ACKNOWLEDGEMENT,
    3: RESET
}

def process_messageType_method(self, argument, message):
    return switcherProcess[argument].__call__(self, message)


