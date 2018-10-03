from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPubcomp(object):
    def __init__(self, packetID):
        self.packetID = packetID

    def getLength(self):
        return 4

    def getType(self):
        return MQTTSN_messageType.SN_PUBCOMP.value[0]

    def getPacketID(self):
        return self.packetID

    def setPacketID(self, packetID):
        self.packetID = packetID