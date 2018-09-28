from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class GWInfo(object):
    def __init__(self, gwID, gwAddress):
        self.gwID = gwID
        self.gwAddress = gwAddress

    def getLength(self):
        length = 3
        if self.gwAddress is not None & len(self.gwAddress)>0:
            length += len(self.gwAddress)
        return length

    def getType(self):
        return MQTTSN_messageType.SN_GWINFO

    def getgwID(self):
        return self.gwID

    def setgwID(self, gwID):
        self.gwID = gwID

    def getgwAddress(self):
        return self.gwAddress

    def setgwAddress(self, gwAddress):
        self.gwAddress = gwAddress