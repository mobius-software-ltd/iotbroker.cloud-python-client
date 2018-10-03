from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class SNPingresp(object):
    def __init__(self):
        pass

    def getLength(self):
        return 2

    def getType(self):
        return MQTTSN_messageType.SN_PINGRESP.value[0]