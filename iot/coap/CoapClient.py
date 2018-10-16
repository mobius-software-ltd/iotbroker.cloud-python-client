from venv.iot.classes.ConnectionState import *
from venv.iot.network.UDPClient import *
from venv.iot.classes.IoTClient import *
from venv.iot.coap.CoapParser import *
from venv.iot.coap.options.CoapOptionType import *
from venv.iot.coap.options.OptionParser import *
from venv.iot.timers.TimersMap import *
from venv.iot.coap.tlv.CoapTopic import *
#import t.i.reactor only after installing wxreactor
from twisted.internet import reactor

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

    def goConnect(self):
        #print('CoapClient.goConnect')
        self.setState(ConnectionState.CONNECTING)

        duration = self.account.keepAlive

        if self.timers is not None:
            self.timers.stopAllTimers()

        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options = []
        options.append(option)
        message = CoapMessage(self.Version,CoapType.CONFIRMABLE,CoapCode.PUT,0,None,options,None)
        self.udpClient = UDPClient(self.account.serverHost, self.account.port, self)
        reactor.listenUDP(0, self.udpClient)
        self.timers.goPingTimer(message,duration)

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            message = self.parser.encode(message)
            #print('Send ' + str(message))
            self.udpClient.send(message)
        else:
            return False

    def dataReceived(self, data):
        message = self.parser.decode(data)
        type = message.getType()
        code = message.getCode()
        #print('CoapClient.dataReceived ' + str(type) + ' code=' + str(code))
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
                self.clientGUI.publishReceived(topicResult,qos,content,False,False)
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
        self.clientGUI.connackReceived(None)

    def disconnectWith(self,duration):
        self.timers.stopAllTimers()

    def timeoutMethod(self):
        self.timers.stopAllTimers()
        self.clientGUI.timeout()

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
                    self.clientGUI.publishReceived(topicResult, qos, content, False, False)
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
                        self.clientGUI.subackReceived(topic, qos, 0)
                    elif observeValue == 1:
                        list = []
                        list.append(topic)
                        self.clientGUI.unsubackReceived(list)
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
                    self.clientGUI.pubackReceived(topicResult,qos,content,False,False,0)
        else:
            if self.pingNum == 0:
                self.pingNum +=1
                self.clientGUI.pingrespReceived()

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


