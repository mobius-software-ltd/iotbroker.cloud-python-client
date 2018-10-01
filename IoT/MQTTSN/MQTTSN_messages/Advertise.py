from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class Advertise(object):
    def __init__(self, gwID, duration):
        self.gwID = gwID
        self.duration = duration

    def getLength(self):
        return 5

    def getType(self):
        return MQTTSN_messageType.SN_ADVERTISE.value[0]

    def getgwID(self):
        return self.gwID

    def setgwID(self, gwID):
        self.gwID = gwID

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration