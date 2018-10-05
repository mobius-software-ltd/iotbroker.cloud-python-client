from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class SNUnsubscribe(object):
    def __init__(self, packetID, topic):
        self.packetID = packetID
        self.topic = topic

    def getLength(self):
        length = 5
        if self.topic is not None and self.topic.getLength() > 0:
            length += self.topic.getLength()
        if self.topic.getLength() > 250:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_UNSUBSCRIBE.value[0]

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic