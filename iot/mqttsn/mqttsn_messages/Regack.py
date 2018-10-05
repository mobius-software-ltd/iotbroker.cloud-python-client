from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class Regack(object):
    def __init__(self, topicID, packetID, code):
        self.topicID = topicID
        self.packetID = packetID
        self.code = code

    def getLength(self):
        return 7

    def getType(self):
        return MQTTSN_messageType.SN_REGACK.value[0]

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code