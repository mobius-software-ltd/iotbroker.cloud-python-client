from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPubrec(object):
    def __init__(self, messageID):
        self.messageID = messageID

    def getLength(self):
        return 4

    def getType(self):
        return MQTTSN_messageType.SN_PUBREC.value[0]

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID