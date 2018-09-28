from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNUnsubscribe(object):
    def __init__(self, messageID, topic):
        self.messageID = messageID
        self.topic = topic

    def getLength(self):
        length = 5
        if self.topic is not None & len(self.topic)>0:
            length += len(self.topic)
        if len(self.content) > 250:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_UNSUBSCRIBE

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic