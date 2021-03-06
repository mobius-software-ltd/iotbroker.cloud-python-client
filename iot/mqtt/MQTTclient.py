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

from iot.classes.IoTClient import *
from iot.mqtt.MQParser import MQParser
from iot.mqtt.mqtt_classes.MQConnackCode import *
from iot.mqtt.mqtt_classes.MQTopic import *
from iot.mqtt.mqtt_classes.Will import *
from iot.mqtt.mqtt_messages.MQConnect import *
from iot.mqtt.mqtt_messages.MQDisconnect import *
from iot.mqtt.mqtt_messages.MQPuback import *
from iot.mqtt.mqtt_messages.MQPubcomp import *
from iot.mqtt.mqtt_messages.MQPubrec import *
from iot.mqtt.mqtt_messages.MQPubrel import *
from iot.mqtt.mqtt_messages.MQSubscribe import *
from iot.mqtt.mqtt_messages.MQUnsubscribe import *
from iot.network.TCPClient import *
from iot.timers.TimersMap import *


class MQTTclient(IoTClient):
    def __init__(self, account, client):
        self.account = account
        self.clientGUI = client
        self.parser = MQParser(None)
        self.resendperiod = 3000
        self.connectionState = None
        self.data = None
        self.timers = TimersMap(self)
        self.publishPackets = {}
        self.can_connect = True

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            self.parser.setMessage(message)
            message = self.parser.encode()
            self.clientFactory.send(message)
        else:
            return False

    def dataReceived(self, data):
        messages = []
        index = 1
        while len(data) - index > 0:
            length = self.parser.next(data, index)
            if length < 0:
                break
            part = data[index - 1:index + length]
            message = self.parser.decode(part)
            messages.append(message)
            index += length

        for message in messages:
            process_messageType_method(self, message.getType(), message)

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def isConnected(self):
        return self.connectionState == ConnectionState.CONNECTION_ESTABLISHED

    def closeChannel(self):
        if self.client is not None:
            self.client.stop()

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)
        if self.account.willTopic is not None:
            topic = MQTopic(self.account.willTopic, self.account.qos)
            will = Will(topic, self.account.will, self.account.isRetain)
        else:
            will = None

        connect = MQConnect(self.account.username, self.account.password, self.account.clientID, self.account.cleanSession, self.account.keepAlive, will)
        if self.timers is not None:
            self.timers.stopAllTimers()
        self.timers.goConnectTimer(connect)
        self.parser.setMessage(connect)
        self.clientFactory = ClientFactory(self.parser.encode(), self)
        if self.account.isSecure:
            ctx = CtxFactory(self.account.certificate, self.account.certPasw)
            self.connector = reactor.connectSSL(self.account.serverHost, self.account.port, self.clientFactory, ctx)
        else:
            self.connector = reactor.connectTCP(self.account.serverHost, self.account.port, self.clientFactory)

    def publish(self, name, qos, content, retain, dup):
        topic = MQTopic(name, qos)
        publish = MQPublish(0, topic, content, retain, dup)
        if (qos == 0):
            self.send(publish)
        else:
            if (qos in [1, 2]):
                self.timers.goMessageTimer(publish)

    def unsubscribeFrom(self, topicName):
        listTopics = []
        listTopics.append(topicName)
        unsubscribe = MQUnsubscribe(0, listTopics)
        self.timers.goMessageTimer(unsubscribe)

    def subscribeTo(self, name, qos):
        topic = MQTopic(name, qos)
        listMQTopics = [topic]
        subscribe = MQSubscribe(0, listMQTopics)
        self.timers.goMessageTimer(subscribe)

    def pingreq(self):
        self.send(MQPingreq())

    def disconnectWith(self, duration):
        self.send(MQDisconnect())
        self.timers.stopAllTimers()
        self.clientFactory.client_close_connection()

    def timeoutMethod(self):
        if self.can_connect:
            self.can_connect = False
            self.timers.stopAllTimers()
            reactor.callFromThread(self.clientGUI.timeout)

    def connectTimeoutMethod(self):
        if self.can_connect:
            self.can_connect = False
            self.timers.stopAllTimers()
            reactor.callFromThread(self.clientGUI.show_error_message, "Connect Error", "Connection timeout")
            reactor.callFromThread(self.clientGUI.timeout)

    def ConnectionLost(self):
        if self.can_connect:
            self.can_connect = False
            if self.timers is not None:
                self.timers.stopAllTimers()

            self.connector.disconnect()
            reactor.callFromThread(self.clientGUI.errorReceived)


# _____________________________________________________________________________________

def processConnack(self, message):
    self.timers.stopConnectTimer()
    if message.returnCode == 0:  # MQ_ACCEPTED
        self.setState(ConnectionState.CONNECTION_ESTABLISHED)
        self.timers.goPingTimer(MQPingreq(), self.account.keepAlive)
        self.clientGUI.connackReceived(message.returnCode)
    else:
        messagebox.showinfo("Connect error", MQConnackCode(message.returnCode).readable_name())
        self.clientGUI.errorReceived()


def processSuback(self, message):
    subscribe = self.timers.removeTimer(message.packetID)
    if subscribe is not None:
        size = len(subscribe.listMQTopics)
        topic = subscribe.listMQTopics[size - 1]
        qos = topic.getQoS()
        self.clientGUI.subackReceived(topic, qos, 0)


def processUnsuback(self, message):
    unsubscribe = self.timers.removeTimer(message.packetID)
    if unsubscribe is not None:
        self.clientGUI.unsubackReceived(unsubscribe.listTopics)


def processPublish(self, message):
    publisherQoS = message.topic.qos.getValue()
    if publisherQoS.getValue() == 0:
        self.clientGUI.publishReceived(message.topic, publisherQoS, message.content, message.dup, message.retain)
    if publisherQoS.getValue() == 1:  # AT_LEAST_ONCE
        puback = MQPuback(message.packetID)
        self.send(puback)
        self.clientGUI.publishReceived(message.topic, publisherQoS, message.content, message.dup, message.retain)
    if publisherQoS.getValue() == 2:  # EXACTLY_ONCE
        pubrec = MQPubrec(message.packetID)
        self.send(pubrec)
        self.publishPackets[message.packetID] = message


def processPuback(self, message):
    publish = self.timers.removeTimer(message.packetID)
    if publish is not None:
        self.clientGUI.pubackReceived(publish.topic, publish.topic.getQoS(), publish.content, publish.dup, publish.retain, 0)


def processPubrec(self, message):
    publish = self.timers.removeTimer(message.packetID)
    if publish is not None:
        self.timers.goMessageTimer(MQPubrel(publish.packetID))
        self.publishPackets[publish.packetID] = publish


def processPubrel(self, message):
    publish = self.publishPackets.get(message.packetID)
    if publish is not None:
        self.clientGUI.publishReceived(publish.topic, publish.topic.getQoS().getValue(), publish.content, publish.dup, publish.retain)
    self.send(MQPubcomp(message.packetID))


def processPubcomp(self, message):
    pubrel = self.timers.removeTimer(message.packetID)
    if pubrel is not None:
        publish = self.publishPackets.get(message.packetID)
        self.clientGUI.pubackReceived(publish.topic, publish.topic.getQoS(), publish.content, publish.dup, publish.retain, 0)


def processPingresp(self, message):
    self.clientGUI.pingrespReceived(False)


def processSubscribe(self, message):
    self.clientGUI.errorReceived('received invalid message subscribe')


def processConnect(self, message):
    self.clientGUI.errorReceived('received invalid message connect')


def processPingreq(self, message):
    self.clientGUI.errorReceived('received invalid message pingreq')


def processDisconnect(self, message):
    self.timers.stopAllTimers()
    self.clientGUI.disconnectReceived()


def processUnsubscribe(self, message):
    raise ValueError('received invalid message unsubscribe')


switcherProcess = {
    1: processConnect,
    2: processConnack,
    3: processPublish,
    4: processPuback,
    5: processPubrec,
    6: processPubrel,
    7: processPubcomp,
    8: processSubscribe,
    9: processSuback,
    10: processUnsubscribe,
    11: processUnsuback,
    12: processPingreq,
    13: processPingresp,
    14: processDisconnect,
}


def process_messageType_method(self, argument, message):
    return switcherProcess[argument].__call__(self, message)
