from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNSubscribe(object):
    def __init__(self, messageID, topic, dup):
        self.messageID = messageID
        self.topic = topic
        self.dup = dup

    def getLength(self):
        length = 5
        if self.topic is not None and self.topic.getLength() > 0:
            length += self.topic.getLength()
        if self.topic.getLength() > 250:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_SUBSCRIBE.value[0]

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic

    def isDup(self):
        return self.dup

    def setDup(self, dup):
        self.dup = dup