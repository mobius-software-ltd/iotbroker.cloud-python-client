from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *
from venv.IoT.MQTTSN.MQTTSN_classes.ReturnCode import *
from venv.IoT.Classes.QoS import *

class SNSuback(object):
    def __init__(self, topicID, code, qos, messageID):
        self.topicID = topicID
        self.code = ReturnCode(code)
        self.qos = QoS(qos)
        self.messageID = messageID

    def getLength(self):
        return 8

    def getType(self):
        return MQTTSN_messageType.SN_SUBACK

    def getTopicID(self):
        return self.topicID

    def setTopicID(self, topicID):
        self.topicID = topicID

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = ReturnCode(code)

    def getQoS(self):
        return self.qos

    def setQoS(self, qos):
        self.qos = qos

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID