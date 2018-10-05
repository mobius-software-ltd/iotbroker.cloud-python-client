from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class WillTopicResp(object):
    def __init__(self, code):
        self.code = code

    def getLength(self):
        return 3

    def getType(self):
        return MQTTSN_messageType.SN_WILL_TOPIC_RESP.value[0]

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code