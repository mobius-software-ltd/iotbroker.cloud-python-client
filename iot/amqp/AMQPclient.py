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
from iot.amqp.header.impl.AMQPProtoHeader import *
from iot.amqp.header.impl.AMQPPing import *
from iot.amqp.header.impl.AMQPOpen import *
from iot.amqp.header.impl.SASLMechanisms import *
from iot.amqp.header.impl.SASLInit import *
from iot.amqp.header.impl.SASLOutcome import *
from iot.amqp.header.impl.AMQPBegin import *
from iot.amqp.header.impl.AMQPEnd import *
from iot.amqp.header.impl.AMQPClose import *
from iot.amqp.header.impl.AMQPTransfer import *
from iot.amqp.header.impl.AMQPAttach import *
from iot.amqp.header.impl.AMQPDisposition import *
from iot.amqp.header.impl.AMQPDetach import *
from iot.amqp.sections.AMQPData import *
from iot.amqp.terminus.AMQPSource import *
from iot.amqp.wrappers.AMQPMessageFormat import *
from iot.amqp.avps.OutcomeCode import *
from iot.classes.NumericUtil import NumericUtil as util
from iot.classes.ConnectionState import *
from iot.mqtt.mqtt_classes.MQConnackCode import *
from iot.mqtt.mqtt_classes.MQSubackCode import *
from iot.mqtt.mqtt_classes.Will import *
from iot.mqtt.mqtt_classes.MQTopic import *
from iot.network.TCPClient import *
from iot.classes.IoTClient import *
from iot.amqp.AMQPParser import AMQPParser
from iot.timers.TimersMap import *
# import t.i.reactor only after installing wxreactor
from twisted.internet import ssl, reactor
import numpy as np
from database import TopicEntity

class AMQPclient(IoTClient):
    def __init__(self, account, client, topics):
        self.account = account
        self.clientGUI = client
        self.parser = AMQPParser()
        self.nextHandle = 1
        self.connectionState = None
        self.channel = 0
        self.isSASLConfirm = False
        self.timers = TimersMap(self)
        self.usedIncomingMappings = {}
        self.usedOutgoingMappings = {}
        self.usedMappings = {}
        self.pendingMessages = []
        self.timeout = 0
        self.pending_topics = {}
        for topic in topics:
            self.pending_topics[topic.topicName] = topic
        self.outstanding_attach_topics = {}

    def send(self, header):

        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            message = self.parser.encode(header)
            self.clientFactory.send(message)
        else:
            return False

    def dataReceived(self, data):

        received = bytearray()
        messages = []

        while len(received) < len(data):
            index = 0
            part = self.parser.next(data, index)
            message = self.parser.decode(part)
            messages.append(message)
            index += len(part)
            received += part
            data = data[index:]

        for message in messages:
            process_messageType_method(self, message.getCode().value, message)

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)
        header = AMQPProtoHeader(3)  # SASL = 3
        self.clientFactory = ClientFactory(self.parser.encode(header), self)

        if self.account.isSecure:
            ctx = CtxFactory(self.account.certificate, self.account.certPasw)
            reactor.connectSSL(self.account.serverHost, self.account.port, self.clientFactory, ctx)
        else:
            connector = reactor.connectTCP(self.account.serverHost, self.account.port, self.clientFactory)

        self.setState(ConnectionState.CONNECTION_ESTABLISHED)

    def publish(self, name, qos, content, retain, dup):

        messageFormat = AMQPMessageFormat(0, None, None)
        transfer = AMQPTransfer(None, None, None, self.channel, None, None, None, messageFormat, True, False, None, None, None, None, None, None)

        data = AMQPData(bytes(content, encoding='utf_8'))
        sections = {}
        sections[SectionCode.DATA] = data
        transfer.setSections(sections)

        if name in self.usedOutgoingMappings:
            handle = self.usedOutgoingMappings[name]
            transfer.setHandle(np.int64(handle))
            self.timers.goMessageTimer(transfer)
            if transfer.getSettled() is not None:
                settled = transfer.getSettled()
                if settled:
                    if transfer.getDeliveryId() is not None:
                        self.timers.removeTimer(transfer.getDeliveryId())
        else:
            currentHandler = self.nextHandle
            self.nextHandle += 1
            self.usedOutgoingMappings[name] = currentHandler
            self.usedMappings[currentHandler] = name
            transfer.setHandle(np.int64(currentHandler))
            self.pendingMessages.append(transfer)

            attach = AMQPAttach(None, None, None, self.channel, str(name), np.int64(currentHandler), RoleCode.SENDER, None, np.int16(ReceiveCode.FIRST.value), None, None, None, None, np.int64(0),
                                None, None, None, None)
            source = AMQPSource(str(name), np.int64(TerminusDurability.NONE.value), None, np.int64(0), False, None, None, None, None, None, None)
            attach.setSource(source)
            self.send(attach)

    def subscribeTo(self, name, qos):
        if name in self.usedIncomingMappings:
            currentHandler = self.usedIncomingMappings[name]
        else:
            currentHandler = self.nextHandle
            self.nextHandle += 1
            self.usedIncomingMappings[name] = currentHandler
            self.usedMappings[currentHandler] = name

        attach = AMQPAttach(None, None, None, self.channel, str(name), np.int64(currentHandler), RoleCode.RECEIVER, np.int16(SendCode.MIXED.value), None, None, None, None, None, None, None, None,
                            None, None)
        target = AMQPTarget(str(name), np.int64(TerminusDurability.NONE.value), None, np.int64(0), False, None, None)
        attach.setTarget(target)

        self.outstanding_attach_topics[attach.handle] = name

        self.send(attach)

    def unsubscribeFrom(self, topicName):
        if topicName in self.usedIncomingMappings:
            detach = AMQPDetach(None, None, None, self.channel, np.int64(self.usedIncomingMappings[topicName]), True, None)
            self.send(detach)
        else:
            listTopics = []
            listTopics.append(topicName)
            self.clientGUI.unsubackReceived(listTopics)

    def pingreq(self):
        ping = AMQPPing()
        self.send(ping)

    def disconnectWith(self, duration):
        self.timers.stopAllTimers()
        end = AMQPEnd(None, None, None, self.channel, None)
        self.send(end)

    def getPingreqMessage(self):
        return AMQPPing()

    def timeoutMethod(self):
        self.timers.stopAllTimers()
        self.clientGUI.timeout()

    def setTopics(self, topics):
        pass

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def ConnectionLost(self):
        if self.timers != None:
            self.timers.stopAllTimers()
        self.clientGUI.errorReceived()


# __________________________________________________________________________________________

def processProto(self, message):
    if isinstance(message, AMQPProtoHeader):
        if self.isSASLConfirm and message.getProtocolId() == 0:
            open = AMQPOpen(None, None, None, message.getChannel(), self.account.clientID, self.account.serverHost, None, None, np.int64(50 * 1000), None, None, None, None, None)
            self.send(open)


def processMechanisms(self, message):
    if isinstance(message, SASLMechanisms):
        plainMech = None
        mechanisms = message.getMechanisms()

        for mechanism in mechanisms:
            if isinstance(mechanism, AMQPSymbol):
                if mechanism.getValue() == 'PLAIN':
                    plainMech = mechanism
                    plainMech.setValue(mechanism.getValue())
                    break

    if plainMech is None:
        self.timers.stopAllTimers()
        return

    challenge = bytearray()
    challenge = util.addString(challenge, self.account.username)
    challenge = util.addByte(challenge, 0)
    challenge = util.addString(challenge, self.account.username)
    challenge = util.addByte(challenge, 0)
    challenge = util.addString(challenge, self.account.password)

    init = SASLInit(None, None, message.getType(), message.getChannel(), plainMech, challenge, None)
    self.send(init)


def processOutcome(self, message):
    if isinstance(message, SASLOutcome):
        if message.getOutcomeCode() == OutcomeCode.OK.value:
            self.isSASLConfirm = True
            header = AMQPProtoHeader(0)
            self.send(header)
        else:
            if message.getOutcomeCode() == OutcomeCode.AUTH.value:
                messagebox.showinfo("Connect Error", "Authentication failed")
            else:
                messagebox.showinfo("Connect Error", "errorCode=" + str(message.getOutcomeCode()))

            self.clientGUI.errorReceived()


def processOpen(self, message):
    self.timeout = message.getIdleTimeout()
    if isinstance(message, AMQPOpen):
        begin = AMQPBegin(None, None, None, self.channel, None, np.int64(0), np.int64(2147483647), np.int64(0), None, None, None, None)
        self.send(begin)


def processBegin(self, message):
    self.clientGUI.connackReceived(0)
    ping = AMQPPing()
    if self.timeout is None:
        self.timers.goPingTimer(ping, 50)
    else:
        self.timers.goPingTimer(ping, self.timeout / 1000)

    for key, value in self.pending_topics.items():
        self.subscribeTo(key, value.qos)


def processEnd(self, message):
    close = AMQPClose(None, None, None, self.channel, None)
    self.send(close)


def processClose(self, message):
    self.timers.stopAllTimers()
    self.isSASLConfirm = False
    self.connectionState == ConnectionState.CONNECTION_LOST

    if message.error is not None and message.error.description is not None:
        messagebox.showinfo("Connect Error", message.error.description)
        self.clientGUI.errorReceived()


def processAttach(self, message):
    if isinstance(message, AMQPAttach):
        if message.getRole() == RoleCode.RECEIVER:
            for pending in self.pendingMessages:
                if isinstance(pending, AMQPTransfer):
                    h1 = pending.getHandle()
                    h2 = message.getHandle()
                if h1 == h2:
                    self.pendingMessages.remove(pending)
                    self.timers.goMessageTimer(pending)
                    if pending.getSettled() is not None:
                        settled = pending.getSettled()
                        if settled:
                            if pending.getDeliveryId() is not None:
                                id = pending.getDeliveryId()
                                self.timers.removeTimer(id)
        else:
            handle = message.getHandle()
            self.usedIncomingMappings[message.getName()] = handle
            self.usedMappings[handle] = message.getName()

            try:
                if self.outstanding_attach_topics.pop(handle) == message.getName():
                    if self.pending_topics.pop(message.getName(), None) is None:
                        topic = MQTopic(message.getName(), 1)
                        qos = topic.getQoS()
                        self.clientGUI.subackReceived(topic, qos, 0)
            except:
                pass


def processTransfer(self, message):
    if isinstance(message, AMQPTransfer):

        qos = QoS(1)
        if message.getSettled() is not None and message.getSettled():
            qos = QoS(0)
            print("qos 0")
        else:
            state = AMQPAccepted()
            disposition = AMQPDisposition(None, None, None, self.channel, RoleCode.RECEIVER, np.int64(message.getDeliveryId()), np.int64(message.getDeliveryId()), True, AMQPAccepted(), None)
            print("sending disposition")
            self.send(disposition)
            print("disposition sent")

        handle = message.getHandle()
        if handle is not None and (handle in self.usedMappings):
            topic = self.usedMappings[handle]
            self.clientGUI.publishReceived(topic, qos, message.getData().getData(), False, False)


def processDetach(self, message):
    if isinstance(message, AMQPDetach):
        handle = message.getHandle()
        if handle in self.usedMappings:
            topicName = self.usedMappings[handle]
            self.usedMappings.pop(handle)
            if topicName in self.usedOutgoingMappings:
                self.usedOutgoingMappings.pop(topicName)

            listTopics = []
            listTopics.append(topicName)
            self.clientGUI.unsubackReceived(listTopics)


def processDisposition(self, message):
    if isinstance(message, AMQPDisposition):
        if message.getFirst() is not None:
            first = message.getFirst()
            if message.getLast() is not None:
                last = message.getLast()
                for i in range(first, last - 1):
                    self.timers.removeTimer(i)
            else:
                transfer = self.timers.removeTimer(first)
                if transfer is not None:
                    handle = transfer.getHandle()
                    topic = self.usedMappings[handle]
                    qos = QoS(1)
                    self.clientGUI.pubackReceived(topic, qos, transfer.getData().getData(), False, False)


def processFlow(self, message):
    pass


def processInit(self, message):
    raise ValueError("received invalid message init")


def processChallenge(self, message):
    raise ValueError("received invalid message challenge")


def processResponse(self, message):
    raise ValueError("received invalid message response")


def processPing(self, message):
    pass


switcherProcess = {
    16: processOpen,
    17: processBegin,
    18: processAttach,
    19: processFlow,
    20: processTransfer,
    21: processDisposition,
    22: processDetach,
    23: processEnd,
    24: processClose,
    64: processMechanisms,
    65: processInit,
    66: processChallenge,
    67: processResponse,
    68: processOutcome,
    254: processProto,
    255: processPing,
}


def process_messageType_method(self, argument, message):
    return switcherProcess[argument].__call__(self, message)
