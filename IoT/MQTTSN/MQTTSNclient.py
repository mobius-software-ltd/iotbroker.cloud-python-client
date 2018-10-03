from venv.IoT.Classes.ConnectionState import *
from venv.IoT.Network.UDPClient import *
from venv.IoT.Classes.IoTClient import *
from venv.IoT.MQTTSN.SNParser import *
from venv.IoT.Timers.TimersMap import *

#import t.i.reactor only after installing wxreactor
from twisted.internet import reactor

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
        self.registerID = 0
        self.publishPackets = {}
        self.topics = {}

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            self.parser.setMessage(message)
            message = self.parser.encode()
            self.udpClient.send(message)
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

        if self.account.will is not None and len(self.account.will)> 0:
            willPresent = True
        else:
            willPresent = False

        cleanSession = self.account.cleanSession
        duration = self.account.keepAlive
        clientID = self.account.clientID
        connect = SNConnect(willPresent, cleanSession, duration, clientID)

        if self.timers is not None:
            self.timers.stopAllTimers()
        self.timers.goConnectTimer(connect)

        self.parser.setMessage(connect)
        message = self.parser.encode()
        self.udpClient = UDPClient(self.account.serverHost, self.account.port, self)
        reactor.listenUDP(0, self.udpClient)
        self.udpClient.send(message)

    def publish(self, topicName, qosValue, content, retain, dup):
        qos = QoS(qosValue)
        topic = FullTopic(topicName, qos)
        register = Register(0,0,topicName)
        publish = SNPublish(0,topic,content,dup,retain)
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
        unsubscribe = SNUnsubscribe(0,topic)
        self.timers.goMessageTimer(unsubscribe)

    def pingreq(self):
        self.send(SNPingreq(self.account.clientID))

    def disconnectWith(self, duration):
        if duration is not None and duration > 0:
            self.send(SNDisonnect(duration))
        else:
            self.send(SNDisonnect(0))
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
def processADVERTISE(self,message):
    raise ValueError('Packet Advertise did receive')

def processSEARCHGW(self,message):
    raise ValueError('Packet Search did receive')

def processGWINFO(self,message):
    raise ValueError('Packet GWInfo did receive')

def processCONNECT(self,message):
    raise ValueError('Packet Connect did receive')

def processCONNACK(self,message):
    self.setState(ConnectionState.CONNECTION_ESTABLISHED)
    self.timers.stopConnectTimer()
    self.timers.goPingTimer(SNPingreq(self.account.clientID), self.account.keepAlive)
    self.clientGUI.connackReceived(message.getCode())

def processWILL_TOPIC_REQ(self,message):
    qos = QoS(self.account.qos)
    topic = FullTopic(self.account.willTopic, qos)
    retain = self.account.isRetain
    willTopic = WillTopic(retain, topic)
    self.send(willTopic)

def processPINGRESP(self,message):
    print('Ping resp was received')

def processWILL_TOPIC(self,message):
    raise ValueError('Packet Will topic did receive')

def processWILL_MSG_REQ(self,message):
    willMessage = WillMsg(self.account.will)
    self.send(willMessage)

def processWILL_MSG(self,message):
    raise ValueError('Packet Will msg did receive')

def processREGISTER(self,message):
    if isinstance(message, Register):
        regack = Regack(message.getTopicID(), message.getPacketID(), ReturnCode.ACCEPTED.value[0])
        self.send(regack)

def processREGACK(self,message):
    self.timers.stopTimer(self.registerID) #stop registerTimer
    if isinstance(message, Regack):
        if message.getCode() == ReturnCode.ACCEPTED.value[0]:
            publish = self.forPublish[message.getPacketID()]
            if publish is not None:
                self.topics[message.getTopicID()] = publish.getTopic().getValue()
                topic = IdentifierTopic(message.getTopicID(),publish.getTopic().getQoS())
                publish.setPacketID(message.getPacketID())
                publish.setTopic(topic)
                if publish.getTopic().getQoS().getValue() ==  QoSType.AT_MOST_ONCE.value[0]:
                    self.send(publish)
                else:
                    self.timers.goMessageTimer(publish)

def processPUBLISH(self,message):
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
    self.clientGUI.publishReceived(topicResult,qos,message.getContent(),message.isDup(),message.isRetain())

def processPUBACK(self, message):
    publish = self.timers.removeTimer(message.getPacketID())
    if publish is not None and isinstance(publish, SNPublish):
        topic = publish.getTopic()
        qos = topic.getQoS()
        topicName = self.topics[int(topic.getValue())]
        topicResult = FullTopic(topicName, qos)
        self.clientGUI.pubackReceived(topicResult,qos,publish.getContent(),publish.isDup(),publish.isRetain(),0)
        self.publishPackets[publish.getPacketID()] = None

def processPUBCOMP(self, message):
    pubcomp = self.timers.removeTimer(message.getPacketID())
    if pubcomp is not None and isinstance(pubcomp, SNPubcomp):
        publish = self.publishPackets.get(message.getPacketID())
        if publish is not None and isinstance(publish, SNPublish):
            topic = publish.getTopic()
            qos = QoS(topic.getQoS())
            topicName = self.topics[int(topic.getValue())]
            topicResult = FullTopic(topicName, qos)
            self.clientGUI.pubackReceived(topicResult,qos,publish.getContent(),publish.isDup(),publish.isRetain(),0)
            self.publishPackets[pubcomp.getPacketID()] = None

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
            self.clientGUI.pubackReceived(topicResult,qos,publish.getContent(),publish.isDup(),publish.isRetain(),0)

def processSUBSCRIBE(self, message):
    raise ValueError('Packet Subscribe did receive')

def processSUBACK(self, message):
    if isinstance(message, SNSuback):
        subscribe = self.timers.removeTimer(message.getPacketID())
        if subscribe is not None and isinstance(subscribe, SNSubscribe):
            self.topics[message.getPacketID()] = subscribe.getTopic().getValue()
            self.clientGUI.subackReceived(subscribe.getTopic().getValue(), subscribe.getTopic().getQoS(), 0)

def processUNSUBSCRIBE(self, message):
    raise ValueError('Packet Unsubscribe did receive')

def processUNSUBACK(self, message):
    if isinstance(message, SNUnsuback):
        unsubscribe = self.timers.removeTimer(message.getPacketID())
        if unsubscribe is not None and isinstance(unsubscribe, SNUnsubscribe):
            list = []
            list.append(unsubscribe.getTopic().getValue())
            self.clientGUI.unsubackReceived(list)

def processPINGREQ(self, message):
    raise ValueError('Packet Pingreq did receive')

def processDISCONNECT(self, message):
    self.timers.stopAllTimers()
    self.clientGUI.disconnectReceived()

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


