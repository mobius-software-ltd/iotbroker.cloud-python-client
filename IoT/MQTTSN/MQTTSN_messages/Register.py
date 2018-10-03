from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class Register(object):
    def __init__(self, topicID, packetID, topicName):
        self.topicID = topicID
        self.packetID = packetID
        self.topicName = topicName

    def getLength(self):
        if self.topicName is None or len(self.topicName) == 0:
            raise ValueError('Register.getLength() must contain a valid topic name')
        length = 6 + len(self.topicName)
        if len(self.topicName) > 249:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_REGISTER.value[0]

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID

    def getTopicName(self):
        return self.topicName

    def setTopicName(self, topicName):
        self.topicName = topicName