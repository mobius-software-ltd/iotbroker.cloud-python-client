from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class WillTopicReq(object):
    def __init__(self):
        pass

    def getLength(self):
        return 2

    def getType(self):
        return MQTTSN_messageType.SN_WILL_TOPIC_REQ.value[0]