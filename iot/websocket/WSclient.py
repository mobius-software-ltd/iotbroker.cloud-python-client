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
from venv.iot.mqtt.mqtt_classes.MQConnackCode import *
from venv.iot.mqtt.mqtt_classes.MQSubackCode import *
from venv.iot.mqtt.mqtt_classes.Will import *
from venv.iot.mqtt.mqtt_classes.MQTopic import *
from venv.iot.network.WebSocket import *
from autobahn.twisted.websocket import connectWS
from venv.iot.classes.IoTClient import *
from venv.iot.mqtt.MQParser import MQParser
from venv.iot.timers.TimersMap import *
import base64
from twisted.internet import reactor

class WSclient(IoTClient):
    def __init__(self, account, client):
        self.account = account
        self.clientGUI = client
        self.resendperiod = 3000
        self.connectionState = None
        self.data = None
        self.timers = TimersMap(self)
        self.publishPackets = {}

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            self.clientFactory.sendPacket(message)
        else:
            return False

    def dataReceived(self, data):
        message = json.loads(data.decode())
        process_messageType_method(self, message['packet'], message)

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)
        if self.account.willTopic and len(self.account.willTopic)>0 is not None:
            will = {"topic": {"name": self.account.willTopic, "qos": self.account.qos},
                    "content": base64.b64encode(self.account.will.encode()).decode("utf-8"),
                    "retain": self.account.isRetain}
            willFlag = True
        else:
            will = None
            willFlag = False

        url = 'ws://' + str(self.account.serverHost) + ':' + str(self.account.port) + '/ws'
        self.clientFactory = WSSocketClientFactory(url, self)
        connectWS(self.clientFactory)

        if self.account.username is not None and len(self.account.username)>0:
            usernameFlag = True
        else:
            usernameFlag = False

        if self.account.password is not None and len(self.account.password)>0:
            passwordFlag = True
        else:
            passwordFlag = False

        connect = {"packet": 1, "protocolLevel": 4, "username": self.account.username, "password": self.account.password,
             "clientID": self.account.clientID, "cleanSession": self.account.cleanSession, "keepalive": self.account.keepAlive, "will": will, "willFlag": willFlag,
             "passwordFlag": passwordFlag, "usernameFlag": usernameFlag, "protocolName": "MQTT"}

        if self.timers is not None:
            self.timers.stopAllTimers()

        self.timers.goConnectTimer(connect)

    def publish(self, name, qos, content, retain, dup):
        publish = {
            "packet": 3,
            "packetID": None,
            "topic": {
                "name": name,
                "qos": qos
            },
            "content": base64.b64encode(content.encode()).decode("utf-8"),
            "retain": retain,
            "dup": dup
        }

        if (qos == 0):
            self.send(publish)
        else:
            if (qos in [1, 2]):
                self.timers.goMessageTimer(publish);

    def unsubscribeFrom(self, topicName):
        listTopics = []
        listTopics.append(topicName)
        unsubscribe = {
            "packet": 10,
            "packetID": None,
            "topics": [
                topicName
            ],
        }
        self.timers.goMessageTimer(unsubscribe)

    def subscribeTo(self, name, qos):
        topic = MQTopic(name, qos)
        listMQTopics = [topic]
        subscribe = {
            "packet": 8,
            "packetID": None,
            "topics": [
                {
                    "name": name,
                    "qos": qos
                }
            ]
        }

        self.timers.goMessageTimer(subscribe)

    def pingreq(self):
        ping = {"packet": 12}
        self.send(ping)

    def disconnectWith(self, duration):
        disconnect = {"packet": 14}
        self.send(disconnect)
        self.timers.stopAllTimers()

    def timeoutMethod(self):
        self.timers.stopAllTimers()
        self.clientGUI.timeout()

    def PacketReceived(self,ProtocolMessage):
        ProtocolMessage.processBy()

    def ConnectionLost(self):
        if self.isClean == True:
            self.clearAccountTopics()
        if self.timers != None:
            self.timers.stopAllTimers()
        if self.client != None:
            self.client.stop()
            self.setState(ConnectionState.CONNECTION_LOST)

    def connected(self):
        self.setState(ConnectionState.CHANNEL_ESTABLISHED)

    def connectFailed(self):
        self.setState(ConnectionState.CHANNEL_FAILED)

#__________________________________________________________________________________________

def processConnack(self,message):
    self.timers.stopConnectTimer()
    ping = {"packet":12}
    self.timers.goPingTimer(ping, self.account.keepAlive)

    if message['returnCode'] == 0: #MQ_ACCEPTED
        self.setState(ConnectionState.CONNECTION_ESTABLISHED)
        self.clientGUI.connackReceived(message['returnCode'])

def processSuback(self,message):
    subscribe = self.timers.removeTimer(message['packetID'])
    if subscribe is not None:
        name = subscribe['topics'][0]['name']
        qos = QoS(subscribe['topics'][0]['qos'])
        topic = MQTopic(name, qos)
        self.clientGUI.subackReceived(topic, qos, 0)

def processUnsuback(self,message):
    unsubscribe = self.timers.removeTimer(message['packetID'])
    if unsubscribe is not None:
      self.clientGUI.unsubackReceived(unsubscribe['topics'])

def processPublish(self,message):
    publisherQoS = message['topic']['qos']

    name = message['topic']['name']
    qos = QoS(message['topic']['qos'])
    topic = MQTopic(name, qos)

    if publisherQoS == 0:
        self.clientGUI.publishReceived(topic, qos, base64.b64decode(message['content']).decode("utf-8"), message['dup'], message['retain'])
    if publisherQoS == 1:  #AT_LEAST_ONCE
        puback = {"packet": 4,"packetID": message['packetID']}
        self.send(puback)
        self.clientGUI.publishReceived(topic, qos, base64.b64decode(message['content']).decode("utf-8"), message['dup'], message['retain'])
    if publisherQoS == 2:  #EXACTLY_ONCE
        pubrec = {"packet": 5, "packetID": message['packetID']}
        self.send(pubrec)
        self.publishPackets[message['packetID']] = message

def processPuback(self,message):
    publish = self.timers.removeTimer(message['packetID'])
    if publish is not None:
        name = publish['topic']['name']
        qos = QoS(publish['topic']['qos'])
        topic = MQTopic(name, qos)
        self.clientGUI.pubackReceived(topic, qos, base64.b64decode(publish['content']).decode("utf-8"), publish['dup'], publish['retain'], 0)

def processPubrec(self, message):
    publish = self.timers.removeTimer(message['packetID'])
    if publish is not None:
        pubrel = {"packet": 6, "packetID": message['packetID']}
        self.timers.goMessageTimer(pubrel)
        self.publishPackets[publish['packetID']] = publish

def processPubrel(self,message):
    pubrec = self.timers.removeTimer(message['packetID'])
    if pubrec is not None:
        publish = self.publishPackets.get(message['packetID'])
        name = publish['topic']['name']
        qos = QoS(publish['topic']['qos'])
        topic = MQTopic(name, qos)

        self.clientGUI.publishReceived(topic, qos, base64.b64decode(publish['content']).decode("utf-8"), publish['dup'], publish['retain'])
        pubcomp = {"packet": 7, "packetID": message['packetID']}
        self.send(pubcomp)

def processPubcomp(self,message):
    pubrel = self.timers.removeTimer(message['packetID'])
    if pubrel is not None:
        publish = self.publishPackets.get(message['packetID'])
        name = publish['topic']['name']
        qos = QoS(publish['topic']['qos'])
        topic = MQTopic(name, qos)

        self.clientGUI.pubackReceived(topic, qos, base64.b64decode(publish['content']).decode("utf-8"), publish['dup'], publish['retain'],0)

def processPingresp(self,message):
    self.clientGUI.pingrespReceived(False)

def processSubscribe(self,message):
    self.clientGUI.errorReceived('received invalid message subscribe')

def processConnect(self,message):
    self.clientGUI.errorReceived('received invalid message connect')

def processPingreq(self,message):
    self.clientGUI.errorReceived('received invalid message pingreq')

def processDisconnect(self,message):
    self.timers.stopAllTimers()
    self.clientGUI.disconnectReceived()

def processUnsubscribe(self,message):
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
