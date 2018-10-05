from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class SNConnack(object):
    def __init__(self, code):
        self.code = code

    def getLength(self):
        return 3

    def getType(self):
        return 5 #MQTTSN_messageType.SN_CONNACK

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code