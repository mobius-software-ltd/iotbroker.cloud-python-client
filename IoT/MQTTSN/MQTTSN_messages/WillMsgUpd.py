from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class WillMsgUpd(object):
    def __init__(self, content):
        self.content = content

    def getLength(self):
        length = 2
        if self.content is not None and len(self.content) > 0:
            length += len(self.content)
        if len(self.content) > 253:
            length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_WILL_MSG_UPD.value[0]

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content