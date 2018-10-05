from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class WillMsgReq(object):
    def __init__(self):
        pass

    def getLength(self):
        return 2

    def getType(self):
        return MQTTSN_messageType.SN_WILL_MSG_REQ.value[0]