from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPuback(object):
    def __init__(self, topicID, messageID, code):
        self.topicID = topicID
        self.messageID = messageID
        self.code = code

    def getLength(self):
        return 7

    def getType(self):
        return MQTTSN_messageType.SN_PUBACK.value[0]

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code