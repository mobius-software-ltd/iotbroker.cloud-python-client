from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class SNConnect(object):
    def __init__(self, willPresent, cleanSession, duration, clientID):
        self.willPresent = willPresent
        self.cleanSession = cleanSession
        self.duration = duration
        self.clientID = clientID
        self.protocolID = 1

    def getLength(self):
        if self.clientID is None or len(self.clientID) == 0:
            raise ValueError('SNConnect.getLength() must contain a valid clientID')
        length = 6 + len(self.clientID)
        return length

    def getType(self):
        return MQTTSN_messageType.SN_CONNECT.value[0]

    def getWillPresent(self):
        return self.willPresent

    def setWillPresent(self, willPresent):
        self.willPresent = willPresent

    def getCleanSession(self):
        return self.cleanSession

    def setCleanSession(self, cleanSession):
        self.cleanSession = cleanSession

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration

    def getClientID(self):
        return self.clientID

    def setClientID(self, clientID):
        self.clientID = clientID

    def getProtocolID(self):
        return self.protocolID