from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class SearchGW(object):
    def __init__(self, radius):
        self.radius = radius

    def getLength(self):
        return 3

    def getType(self):
        return MQTTSN_messageType.SN_SEARCHGW.value[0]

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = radius