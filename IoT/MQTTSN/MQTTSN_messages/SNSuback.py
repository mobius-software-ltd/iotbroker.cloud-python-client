from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNSuback(object):
    def __init__(self, topicID, code, qos, packetID):
        self.topicID = topicID
        self.code = code
        self.qos = qos
        self.packetID = packetID

    def getLength(self):
        return 8

    def getType(self):
        return MQTTSN_messageType.SN_SUBACK.value[0]

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getQoS(self):
        return self.qos

    def setQoS(self, qos):
        self.qos = qos

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID