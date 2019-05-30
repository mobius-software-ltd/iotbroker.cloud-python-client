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
import asyncio

from OpenSSL.crypto import X509
from twisted.internet import reactor

from iot.classes.IoTClient import *
from iot.mqttsn.SNParser import *
from iot.mqttsn.mqttsn_classes.ReturnCode import *
from iot.network.UDPClient import *
from iot.network.pyDTLSClient import *
from iot.timers.TimersMap import *

basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch, wrapper

do_patch()
import tkinter.messagebox as messagebox
from threading import Thread
import socket
from socket import socket

import OpenSSL.crypto


class MQTTSNclient(IoTClient):
    def __init__(self, account, client):
        self.account = account
        self.clientGUI = client
        self.parser = SNParser(None)
        self.resendperiod = 3000
        self.connectionState = None
        self.data = None
        self.udpClient = None
        self.timers = TimersMap(self)
        self.forPublish = {}
        self.registerID = 1
        self.publishPackets = {}
        self.topics = {}
        self.loop = None
        self.udpThread = None

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            self.parser.setMessage(message)
            message = self.parser.encode()
            self.udpClient.sendMessage(message)
        else:
            return False

    def dataReceived(self, data):
        message = self.parser.decode(data)
        process_messageType_method(self, message.getType(), message)

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def getConnectionState(self):
        return self.connectionState

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)

        if self.account.will is not None and len(self.account.will) > 0:
            willPresent = True
        else:
            willPresent = False

        cleanSession = self.account.cleanSession
        duration = self.account.keepAlive
        clientID = self.account.clientID
        connect = SNConnect(willPresent, cleanSession, duration, clientID)

        if self.timers is not None:
            self.timers.stopAllTimers()

        self.parser.setMessage(connect)
        message = self.parser.encode()

        if self.account.isSecure:
            self.loop = asyncio.get_event_loop()

            addr = (self.account.serverHost, self.account.port)
            if self.account.certificate and len(self.account.certificate) > 0:
                fp = self.get_certificate_file(self.account.certificate, self.account.certPasw)

                sock_wrapped = wrapper.wrap_client(socket(AF_INET, SOCK_DGRAM), keyfile=fp.name, certfile=fp.name, ca_certs=fp.name)
                sock_wrapped.connect(addr)
            else:
                sock_wrapped = wrapper.wrap_client(socket(AF_INET, SOCK_DGRAM))
                sock_wrapped.connect(addr)

            datagram = self.loop.create_datagram_endpoint(
                lambda: pyDTLSClient(self.account.serverHost, self.account.port, self.account.certificate, self, self.loop), sock=sock_wrapped)

            transport, protocol = self.loop.run_until_complete(datagram)
            self.udpClient = protocol
            self.setState(ConnectionState.CONNECTION_ESTABLISHED)

            self.udpThread = Thread(target=self.loop.run_forever)
            self.udpThread.daemon = True
            self.udpThread.start()
        else:
            self.udpClient = UDPClient(self.account.serverHost, self.account.port, self)
            reactor.listenUDP(0, self.udpClient)

        self.timers.goConnectTimer(connect)

    def get_certificate_file(self, cert_body, cert_pwd):

        fp = tempfile.NamedTemporaryFile()
        fp.write(bytes(cert_body, 'utf-8'))
        fp.seek(0)

        if cert_pwd is not None and len(cert_pwd) > 0:
            try:
                cert: X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, fp.read())
                fp.seek(0)
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), cert_pwd.encode("utf-8"))
                fp1 = tempfile.NamedTemporaryFile()
                fp1.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))
                fp1.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
                fp1.seek(0)
            except Exception as err:
                fp.close()
                raise err

            return fp1
        else:
            return fp

    def publish(self, topicName, qosValue, content, retain, dup):
        qos = QoS(qosValue)
        topic = FullTopic(topicName, qos)
        register = Register(0, 0, topicName)
        publish = SNPublish(0, topic, content, dup, retain)
        self.registerID = self.timers.goMessageTimer(register)
        self.forPublish[self.registerID] = publish

    def subscribeTo(self, topicName, qosValue):
        qos = QoS(qosValue)
        topic = FullTopic(topicName, qos)
        subscribe = SNSubscribe(0, topic, False)
        self.timers.goMessageTimer(subscribe)

    def unsubscribeFrom(self, topicName):
        qos = QoS(0)
        topic = FullTopic(topicName, qos)
        unsubscribe = SNUnsubscribe(0, topic)
        self.timers.goMessageTimer(unsubscribe)

    def pingreq(self):
        self.send(SNPingreq(self.account.clientID))

    def disconnectWith(self, duration):
        if duration is not None and duration > 0:
            self.send(SNDisconnect(duration))
        else:
            self.send(SNDisconnect(0))
        self.timers.stopAllTimers()

    def timeoutMethod(self):
        self.timers.stopAllTimers()
        messagebox.showinfo("Warning", 'Timeout was reached. Try to reconnect')
        reactor.callFromThread(self.clientGUI.timeout)

    def connectTimeoutMethod(self):
        self.timers.stopAllTimers()
        self.clientGUI.show_error_message("Connect Error", "Connection Timeout")
        self.clientGUI.timeout()

    def PacketReceived(self, ProtocolMessage):
        ProtocolMessage.processBy()

    def ConnectionLost(self):
        if self.isClean == True:
            self.clearAccountTopics()
        if self.timers != None:
            self.timers.stopAllTimers()
        if self.client != None:
            self.client.stop()
            self.setState(ConnectionState.CONNECTION_LOST)
        self.loop.close()
        if self.account.isSecure:
            self.udpThread.join()

    def connected(self):
        self.setState(ConnectionState.CHANNEL_ESTABLISHED)

    def connectFailed(self):
        self.setState(ConnectionState.CHANNEL_FAILED)
        self.loop.close()
        if self.account.isSecure:
            self.udpThread.join()


# __________________________________________________________________________________________
def processADVERTISE(self, message):
    raise ValueError('Packet Advertise did receive')


def processSEARCHGW(self, message):
    raise ValueError('Packet Search did receive')


def processGWINFO(self, message):
    raise ValueError('Packet GWInfo did receive')


def processCONNECT(self, message):
    raise ValueError('Packet Connect did receive')


def processCONNACK(self, message):
    self.setState(ConnectionState.CONNECTION_ESTABLISHED)
    self.timers.stopConnectTimer()
    if message.getCode() == 0:
        reactor.callFromThread(self.clientGUI.connackReceived, message.getCode())
        reactor.callFromThread(self.timers.goPingTimer, SNPingreq(self.account.clientID), self.account.keepAlive)
    else:
        reactor.callFromThread(self.clientGUI.show_error_message, "Connect Error", "ReturnCode: " + str(ReturnCode(message.getCode()).name))
        reactor.callFromThread(self.clientGUI.errorReceived)

def processWILL_TOPIC_REQ(self, message):
    qos = QoS(self.account.qos)
    topic = FullTopic(self.account.willTopic, qos)
    retain = self.account.isRetain
    willTopic = WillTopic(retain, topic)
    self.send(willTopic)


def processPINGRESP(self, message):
    print('Ping resp was received')


def processWILL_TOPIC(self, message):
    raise ValueError('Packet Will topic did receive')


def processWILL_MSG_REQ(self, message):
    willMessage = WillMsg(self.account.will)
    self.send(willMessage)


def processWILL_MSG(self, message):
    raise ValueError('Packet Will msg did receive')


def processREGISTER(self, message):
    if isinstance(message, Register):
        self.topics[message.getTopicID()] = message.getTopicName()
        regack = Regack(message.getTopicID(), message.getPacketID(), ReturnCode.ACCEPTED.value[0])
        self.send(regack)


def processREGACK(self, message):
    self.timers.stopTimer(self.registerID)  # stop registerTimer
    if isinstance(message, Regack):
        if message.getCode() == ReturnCode.ACCEPTED.value[0]:
            publish = self.forPublish[message.getPacketID()]
            if publish is not None:
                self.topics[message.getTopicID()] = publish.getTopic().getValue()
                topic = IdentifierTopic(message.getTopicID(), publish.getTopic().getQoS())
                publish.setPacketID(message.getPacketID())
                publish.setTopic(topic)
                if publish.getTopic().getQoS().getValue() == QoSType.AT_MOST_ONCE.value[0]:
                    self.send(publish)
                else:
                    self.timers.goMessageTimer(publish)


def processPUBLISH(self, message):
    if isinstance(message, SNPublish):
        if message.getTopic().getQoS() == QoSType.AT_LEAST_ONCE.value[0]:
            topicID = int(message.getTopic().getValue())
            puback = SNPuback(topicID, message.getPacketID(), ReturnCode.ACCEPTED.value[0])
            self.send(puback)
        elif message.getTopic().getQoS() == QoSType.EXACTLY_ONCE.value[0]:
            pubrec = SNPubrec(message.getPacketID())
            self.publishPackets[message.getPacketID()] = message
            self.timers.goMessageTimer(pubrec)
    topic = message.getTopic()
    qos = QoS(topic.getQoS())
    topicName = self.topics[int(topic.getValue())]
    topicResult = FullTopic(topicName, qos)
    reactor.callFromThread(self.clientGUI.publishReceived, topicResult, qos, message.getContent(), message.isDup(), message.isRetain())


def processPUBACK(self, message):
    publish = self.timers.removeTimer(message.getPacketID())
    if publish is not None and isinstance(publish, SNPublish):
        topic = publish.getTopic()
        qos = topic.getQoS()
        topicName = self.topics[int(topic.getValue())]
        topicResult = FullTopic(topicName, qos)
        reactor.callFromThread(self.clientGUI.pubackReceived, topicResult, qos, publish.getContent(), publish.isDup(), publish.isRetain(), 0)
        self.publishPackets[publish.getPacketID()] = None


def processPUBCOMP(self, message):
    pubrel = self.timers.removeTimer(message.getPacketID())
    if pubrel is not None and isinstance(message, SNPubcomp):
        publish = self.publishPackets.get(message.getPacketID())
        if publish is not None and isinstance(publish, SNPublish):
            topic = publish.getTopic()
            qos = QoS(topic.getQoS())
            topicName = self.topics[int(topic.getValue())]
            topicResult = FullTopic(topicName, qos)
            reactor.callFromThread(self.clientGUI.pubackReceived, topicResult, qos.getValue(), publish.getContent(), publish.isDup(), publish.isRetain(), 0)
            self.publishPackets[message.getPacketID()] = None


def processPUBREC(self, message):
    if isinstance(message, SNPubrec):
        publish = self.timers.removeTimer(message.getPacketID())
        if publish is not None:
            self.publishPackets[message.getPacketID()] = publish
            pubrel = SNPubrel(message.getPacketID())
            self.timers.goMessageTimer(pubrel)


def processPUBREL(self, message):
    if isinstance(message, SNPubrel):
        self.timers.removeTimer(message.getPacketID())
        publish = self.publishPackets[message.getPacketID()]
        if publish is not None and isinstance(publish, SNPublish):
            pubComp = SNPubcomp(message.getPacketID())
            self.send(pubComp)
            topic = publish.getTopic()
            qos = QoS(topic.getQoS())
            topicName = self.topics[int(topic.getValue())]
            topicResult = FullTopic(topicName, qos)
            reactor.callFromThread(self.clientGUI.pubackReceived, topicResult, qos, publish.getContent(), publish.isDup(), publish.isRetain(), 0)


def processSUBSCRIBE(self, message):
    raise ValueError('Packet Subscribe did receive')


def processSUBACK(self, message):
    if isinstance(message, SNSuback):
        subscribe = self.timers.removeTimer(message.getPacketID())
        if subscribe is not None and isinstance(subscribe, SNSubscribe):
            self.topics[message.getTopicID()] = subscribe.getTopic().getValue()
            reactor.callFromThread(self.clientGUI.subackReceived, subscribe.getTopic().getValue(), subscribe.getTopic().getQoS(), 0)


def processUNSUBSCRIBE(self, message):
    raise ValueError('Packet Unsubscribe did receive')


def processUNSUBACK(self, message):
    if isinstance(message, SNUnsuback):
        unsubscribe = self.timers.removeTimer(message.getPacketID())
        if unsubscribe is not None and isinstance(unsubscribe, SNUnsubscribe):
            list = []
            list.append(unsubscribe.getTopic().getValue())
            reactor.callFromThread(self.clientGUI.unsubackReceived, list)


def processPINGREQ(self, message):
    raise ValueError('Packet Pingreq did receive')


def processDISCONNECT(self, message):
    self.timers.stopAllTimers()
    reactor.callFromThread(self.clientGUI.disconnectReceived)
    if hasattr(self, "loop") and hasattr(self.loop, "stop"):
        self.loop.stop()

def processWILL_TOPIC_UPD(self, message):
    raise ValueError('Packet Will topic upd did receive')


def processWILL_TOPIC_RESP(self, message):
    raise ValueError('Packet Will topic resp did receive')


def processWILL_MSG_UPD(self, message):
    raise ValueError('Packet Will msg upd did receive')


def processWILL_MSG_RESP(self, message):
    raise ValueError('Packet Will msg resp did receive')


def processENCAPSULATED(self, message):
    raise ValueError('Packet Encapsulated did receive')


switcherProcess = {
    0: processADVERTISE,
    1: processSEARCHGW,
    2: processGWINFO,
    4: processCONNECT,
    5: processCONNACK,
    6: processWILL_TOPIC_REQ,
    7: processWILL_TOPIC,
    8: processWILL_MSG_REQ,
    9: processWILL_MSG,
    10: processREGISTER,
    11: processREGACK,
    12: processPUBLISH,
    13: processPUBACK,
    14: processPUBCOMP,
    15: processPUBREC,
    16: processPUBREL,
    18: processSUBSCRIBE,
    19: processSUBACK,
    20: processUNSUBSCRIBE,
    21: processUNSUBACK,
    22: processPINGREQ,
    23: processPINGRESP,
    24: processDISCONNECT,
    26: processWILL_TOPIC_UPD,
    27: processWILL_TOPIC_RESP,
    28: processWILL_MSG_UPD,
    29: processWILL_MSG_RESP,
    254: processENCAPSULATED
}


def process_messageType_method(self, argument, message):
    return switcherProcess[argument].__call__(self, message)
