from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *
from venv.iot.mqttsn.mqttsn_classes.Radius import *

class Encapsulated(object):
    def __init__(self, radius, wirelessNodeID, message):
        self.radius = Radius(radius)
        self.wirelessNodeID = wirelessNodeID
        self.message = message

    def getLength(self):
        length = 3
        if self.wirelessNodeID is not None & len(self.wirelessNodeID)>0:
            length += len(self.wirelessNodeID)
        return length

    def getType(self):
        return MQTTSN_messageType.SN_ENCAPSULATED

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = Radius(radius)

    def getWirelessNodeID(self):
        return self.wirelessNodeID

    def setWirelessNodeID(self, wirelessNodeID):
        self.wirelessNodeID = wirelessNodeID

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message