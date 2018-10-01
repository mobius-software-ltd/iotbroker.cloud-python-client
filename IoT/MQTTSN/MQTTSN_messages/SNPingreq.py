from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPingreq(object):
    def __init__(self, clientID):
        self.clientID = clientID

    def getLength(self):
        length = 2
        if self.clientID is not None and len(self.clientID) > 0:
            length += len(self.clientID)
        return length

    def getType(self):
        return MQTTSN_messageType.SN_PINGREQ.value[0]

    def getClientID(self):
        return self.clientID

    def setClientID(self, clientID):
        self.clientID = clientID