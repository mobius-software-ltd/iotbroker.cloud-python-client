from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *
from venv.IoT.MQTTSN.MQTTSN_classes.ReturnCode import *

class WillTopicResp(object):
    def __init__(self, code):
        self.code = ReturnCode(code)

    def getLength(self):
        return 3

    def getType(self):
        return MQTTSN_messageType.SN_WILL_TOPIC_RESP

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = ReturnCode(code)