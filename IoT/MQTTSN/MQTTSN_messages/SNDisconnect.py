from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNDisonnect(object):
    def __init__(self, duration):
        self.duration = duration

    def getLength(self):
        length = 2
        if self.duration > 0:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_DISCONNECT.value[0]

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration